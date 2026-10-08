"""Test cases for Sign Up, Sign In, Forgot / Reset / Change Password."""
import pytest

from src import auth, db

Q = auth.SECURITY_QUESTIONS[0]


def make_user(username="rahul", password="Secret123", email="rahul@example.com"):
    return auth.register(username, password, password, Q, "Poddar School", full_name="Rahul", email=email)


# ------------------------------------------------------------------ hashing
def test_password_is_hashed_not_plain(empty_db):
    make_user()
    row = db._one("SELECT password_hash, security_answer_hash FROM users WHERE username='rahul'")
    assert "Secret123" not in row["password_hash"]
    assert row["password_hash"].startswith("pbkdf2_sha256$")
    assert "poddar" not in row["security_answer_hash"].lower()


def test_same_password_gives_different_hashes():
    assert auth.hash_secret("Secret123") != auth.hash_secret("Secret123")  # random salt


def test_verify_secret():
    h = auth.hash_secret("Secret123")
    assert auth.verify_secret("Secret123", h)
    assert not auth.verify_secret("secret123", h)
    assert not auth.verify_secret("x", None)


# ------------------------------------------------------------------ sign up
def test_register_success(empty_db):
    u = make_user()
    assert u["username"] == "rahul" and u["role"] == "user"
    assert "password_hash" not in u  # hashes never leak to the UI / API


@pytest.mark.parametrize("password,msg", [
    ("short1", "at least 8 characters"),
    ("onlyletters", "a digit"),
    ("12345678", "a letter"),
])
def test_register_weak_password(empty_db, password, msg):
    with pytest.raises(auth.AuthError, match=msg):
        auth.register("rahul", password, password, Q, "ans")


def test_register_password_mismatch(empty_db):
    with pytest.raises(auth.AuthError, match="do not match"):
        auth.register("rahul", "Secret123", "Secret124", Q, "ans")


@pytest.mark.parametrize("username", ["ab", "has space", "bad!char", "x" * 31])
def test_register_invalid_username(empty_db, username):
    with pytest.raises(auth.AuthError, match="Username"):
        auth.register(username, "Secret123", "Secret123", Q, "ans")


def test_register_invalid_email(empty_db):
    with pytest.raises(auth.AuthError, match="email"):
        auth.register("rahul", "Secret123", "Secret123", Q, "ans", email="not-an-email")


def test_register_duplicate_username_case_insensitive(empty_db):
    make_user()
    with pytest.raises(auth.AuthError, match="already registered"):
        make_user(username="RAHUL", email="other@example.com")


def test_register_duplicate_email(empty_db):
    make_user()
    with pytest.raises(auth.AuthError, match="already registered"):
        make_user(username="someone_else")


def test_register_requires_security_answer(empty_db):
    with pytest.raises(auth.AuthError, match="security question"):
        auth.register("rahul", "Secret123", "Secret123", Q, " ")


# ------------------------------------------------------------------ sign in
def test_login_with_username_and_email(empty_db):
    make_user()
    assert auth.login("rahul", "Secret123")["username"] == "rahul"
    assert auth.login("RAHUL@example.com", "Secret123")["username"] == "rahul"
    assert db._one("SELECT last_login FROM users WHERE username='rahul'")["last_login"]


def test_login_wrong_password(empty_db):
    make_user()
    with pytest.raises(auth.AuthError, match="Invalid username or password"):
        auth.login("rahul", "Wrong1234")


def test_login_unknown_user_same_message(empty_db):
    with pytest.raises(auth.AuthError, match="Invalid username or password"):
        auth.login("ghost", "Secret123")


def test_account_locks_after_5_failures(empty_db):
    make_user()
    for _ in range(auth.MAX_FAILED_ATTEMPTS - 1):
        with pytest.raises(auth.AuthError, match="attempt"):
            auth.login("rahul", "Wrong1234")
    with pytest.raises(auth.AuthError, match="locked"):
        auth.login("rahul", "Wrong1234")
    with pytest.raises(auth.AuthError, match="locked"):  # even the right password is refused now
        auth.login("rahul", "Secret123")


def test_successful_login_resets_failed_attempts(empty_db):
    make_user()
    with pytest.raises(auth.AuthError):
        auth.login("rahul", "Wrong1234")
    auth.login("rahul", "Secret123")
    assert db._one("SELECT failed_attempts FROM users WHERE username='rahul'")["failed_attempts"] == 0


# ---------------------------------------------------------- forgot password
def test_forgot_password_flow(empty_db):
    make_user()
    assert auth.get_security_question("rahul") == Q
    auth.reset_password_with_answer("rahul", "  poddar   SCHOOL ", "NewPass456", "NewPass456")
    assert auth.login("rahul", "NewPass456")
    with pytest.raises(auth.AuthError):
        auth.login("rahul", "Secret123")


def test_forgot_password_wrong_answer(empty_db):
    make_user()
    with pytest.raises(auth.AuthError, match="incorrect"):
        auth.reset_password_with_answer("rahul", "wrong school", "NewPass456", "NewPass456")


def test_forgot_password_unknown_user(empty_db):
    with pytest.raises(auth.AuthError, match="No account"):
        auth.get_security_question("ghost")


def test_reset_unlocks_account(empty_db):
    make_user()
    for _ in range(auth.MAX_FAILED_ATTEMPTS):
        with pytest.raises(auth.AuthError):
            auth.login("rahul", "Wrong1234")
    auth.reset_password_with_answer("rahul", "poddar school", "NewPass456", "NewPass456")
    assert auth.login("rahul", "NewPass456")


# ------------------------------------------------------- change password
def test_change_password(empty_db):
    uid = make_user()["user_id"]
    auth.change_password(uid, "Secret123", "Changed789", "Changed789")
    assert auth.login("rahul", "Changed789")


def test_change_password_wrong_current(empty_db):
    uid = make_user()["user_id"]
    with pytest.raises(auth.AuthError, match="Current password"):
        auth.change_password(uid, "Wrong1234", "Changed789", "Changed789")


def test_change_password_must_differ(empty_db):
    uid = make_user()["user_id"]
    with pytest.raises(auth.AuthError, match="different"):
        auth.change_password(uid, "Secret123", "Secret123", "Secret123")


def test_admin_reset_password(empty_db):
    uid = make_user()["user_id"]
    auth.admin_reset_password(uid, "TempPass1")
    assert auth.login("rahul", "TempPass1")


def test_update_security_question(empty_db):
    uid = make_user()["user_id"]
    auth.update_security_question(uid, "Secret123", auth.SECURITY_QUESTIONS[1], "Sholay")
    assert auth.get_security_question("rahul") == auth.SECURITY_QUESTIONS[1]
    auth.reset_password_with_answer("rahul", "sholay", "NewPass456", "NewPass456")


# ------------------------------------------------------------- demo data
def test_seeded_demo_accounts(seeded_db):
    from src.config import ADMIN_PASSWORD, ADMIN_USERNAME, DEMO_USER_PASSWORD
    assert auth.login(ADMIN_USERNAME, ADMIN_PASSWORD)["role"] == "admin"
    assert auth.login("user_1", DEMO_USER_PASSWORD)["role"] == "user"


# ------------------------------------------------- "keep me signed in"
@pytest.fixture
def session_mod(empty_db, tmp_path, monkeypatch):
    from src import session
    monkeypatch.setattr(session, "SECRET_PATH", tmp_path / ".secret")
    return session


def test_remember_token_valid(session_mod):
    uid = make_user()["user_id"]
    assert session_mod.verify_token(session_mod.make_token(uid))["username"] == "rahul"


def test_remember_token_tampered(session_mod):
    uid = make_user()["user_id"]
    other = auth.register("other", "Secret123", "Secret123", Q, "ans")["user_id"]
    token = session_mod.make_token(uid)
    forged = token.replace(f"{uid}.", f"{other}.", 1)  # try to become another user
    assert session_mod.verify_token(forged) is None
    assert session_mod.verify_token(token[:-1] + ("0" if token[-1] != "0" else "1")) is None
    assert session_mod.verify_token("garbage") is None


def test_remember_token_expired(session_mod):
    uid = make_user()["user_id"]
    assert session_mod.verify_token(session_mod.make_token(uid, days=-1)) is None


def test_password_change_signs_out_remembered_browsers(session_mod):
    uid = make_user()["user_id"]
    token = session_mod.make_token(uid)
    auth.change_password(uid, "Secret123", "Changed789", "Changed789")
    assert session_mod.verify_token(token) is None


def test_deleted_user_token_invalid(session_mod):
    uid = make_user()["user_id"]
    token = session_mod.make_token(uid)
    db.delete_user(uid)
    assert session_mod.verify_token(token) is None
