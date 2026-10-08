"""Streamlit UI test cases (headless) for authentication and role-based access."""
import pytest
from streamlit.testing.v1 import AppTest

from src import auth
from src.config import ADMIN_PASSWORD, ADMIN_USERNAME, BASE_DIR, DEMO_USER_PASSWORD

T = 120
APP = str(BASE_DIR / "app.py")


def app():
    at = AppTest.from_file(APP, default_timeout=T)
    at.run()
    return at


def login(at, username, password):
    [t for t in at.text_input if t.label == "Username or email"][0].input(username)
    [t for t in at.text_input if t.label == "Password"][0].input(password)
    [b for b in at.button if b.label == "Sign In"][0].click().run()
    return at


def page(at, path):
    at.switch_page(path).run()
    return at


def test_signed_out_shows_only_sign_in(seeded_db):
    at = app()
    assert not at.exception
    assert [b for b in at.button if b.label == "Sign In"]
    assert "auth_user" not in at.session_state


def test_wrong_password_shows_error(seeded_db):
    at = login(app(), "user_1", "WrongPass1")
    assert any("Invalid username or password" in e.value for e in at.error)
    assert "auth_user" not in at.session_state


def test_user_login_and_logout(seeded_db):
    at = login(app(), "user_1", DEMO_USER_PASSWORD)
    assert not at.exception
    assert at.session_state["auth_user"]["username"] == "user_1"
    assert at.session_state["user_id"] == 1
    [b for b in at.sidebar.button if "Logout" in b.label][0].click().run()
    assert "auth_user" not in at.session_state
    assert [b for b in at.button if b.label == "Sign In"]


def test_sign_up_then_sign_in(seeded_db):
    at = page(app(), "views/auth_signup.py")
    fields = {t.label: t for t in at.text_input}
    fields["Username *"].input("new_student")
    fields["Email"].input("student@example.com")
    fields["Password *"].input("Student123")
    fields["Confirm password *"].input("Student123")
    fields["Answer *"].input("Poddar")
    at.checkbox[0].check()
    [b for b in at.button if b.label == "Create account"][0].click().run()
    assert not at.exception and not at.error
    login(app(), "new_student", "Student123")
    assert auth.login("student@example.com", "Student123")["username"] == "new_student"


def test_sign_up_validation_error(seeded_db):
    at = page(app(), "views/auth_signup.py")
    fields = {t.label: t for t in at.text_input}
    fields["Username *"].input("x")
    fields["Password *"].input("weak")
    fields["Confirm password *"].input("weak")
    fields["Answer *"].input("abc")
    at.checkbox[0].check()
    [b for b in at.button if b.label == "Create account"][0].click().run()
    assert at.error


def test_forgot_password_flow(seeded_db):
    from src.config import DEMO_SECURITY_ANSWER
    at = page(app(), "views/auth_forgot.py")
    at.text_input[0].input("user_2")
    [b for b in at.button if b.label == "Continue"][0].click().run()
    assert at.session_state["forgot"]["question"]
    fields = {t.label: t for t in at.text_input}
    fields["Your answer"].input(DEMO_SECURITY_ANSWER)
    fields["New password"].input("Changed123")
    fields["Confirm new password"].input("Changed123")
    [b for b in at.button if b.label == "Reset password"][0].click().run()
    assert not at.error
    assert auth.login("user_2", "Changed123")


def test_change_password_from_account(seeded_db):
    at = login(app(), "user_3", DEMO_USER_PASSWORD)
    page(at, "views/account.py")
    fields = {t.label: t for t in at.text_input}
    fields["Current password"].input(DEMO_USER_PASSWORD)
    fields["New password"].input("Changed456")
    fields["Confirm new password"].input("Changed456")
    [b for b in at.button if b.label == "Change password"][0].click().run()
    assert any("changed" in s.value for s in at.success)
    assert auth.login("user_3", "Changed456")


def test_normal_user_cannot_manage(seeded_db):
    at = login(app(), "user_1", DEMO_USER_PASSWORD)
    page(at, "views/movies.py")
    assert not at.exception
    assert not [b for b in at.button if b.label == "Add movie"]  # browse only
    try:
        page(at, "views/users.py")  # the admin page is not even registered for normal users
        assert not [b for b in at.button if b.label == "Create user"]
    except ValueError:
        pass


@pytest.mark.parametrize("view", ["home", "recommendations", "moviebot", "report", "my_ratings", "movies",
                                  "users", "analytics", "model_performance", "account"])
def test_admin_can_open_every_page(seeded_db, view):
    at = login(app(), ADMIN_USERNAME, ADMIN_PASSWORD)
    page(at, f"views/{view}.py")
    assert not at.exception, at.exception
    assert not [e for e in at.error if "Admins only" in e.value]
