"""Authentication: sign up, sign in, forgot / reset / change password, roles.

Security measures
  * Passwords and security answers are never stored in plain text: PBKDF2-HMAC-SHA256
    with a random 16-byte salt and 200,000 iterations (Python standard library).
  * Constant-time hash comparison (hmac.compare_digest).
  * Password policy: at least 8 characters with a letter and a digit.
  * Account lock for 5 minutes after 5 wrong passwords in a row.
  * Login error messages do not reveal whether the username exists.
"""
import base64
import hashlib
import hmac
import os
import re
import sqlite3
from datetime import datetime, timedelta

from src import db

ITERATIONS = 200_000
MAX_FAILED_ATTEMPTS = 5
LOCK_MINUTES = 5

SECURITY_QUESTIONS = [
    "What is the name of your first school?",
    "What is your favourite movie?",
    "What is the name of your first pet?",
    "In which city were you born?",
    "What is your mother's maiden name?",
    "Who is your favourite actor?",
]

USERNAME_RE = re.compile(r"^[A-Za-z0-9_.]{3,30}$")
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class AuthError(Exception):
    """Raised with a user-friendly message when an auth action fails."""


# ------------------------------------------------------------------ hashing
def hash_secret(secret: str, salt: bytes = None) -> str:
    salt = salt or os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", secret.encode("utf-8"), salt, ITERATIONS)
    return f"pbkdf2_sha256${ITERATIONS}${base64.b64encode(salt).decode()}${base64.b64encode(digest).decode()}"


def verify_secret(secret: str, stored: str) -> bool:
    if not stored:
        return False
    try:
        _, iterations, salt_b64, digest_b64 = stored.split("$")
        digest = hashlib.pbkdf2_hmac("sha256", secret.encode("utf-8"), base64.b64decode(salt_b64), int(iterations))
        return hmac.compare_digest(digest, base64.b64decode(digest_b64))
    except (ValueError, TypeError):
        return False


def _normalise_answer(answer: str) -> str:
    """Security answers are case- and space-insensitive ("  Delhi " == "delhi")."""
    return " ".join(answer.lower().split())


# --------------------------------------------------------------- validation
def password_problems(password: str) -> list:
    problems = []
    if len(password) < 8:
        problems.append("at least 8 characters")
    if not re.search(r"[A-Za-z]", password):
        problems.append("a letter")
    if not re.search(r"\d", password):
        problems.append("a digit")
    return problems


def _check_password(password: str, confirm: str = None):
    problems = password_problems(password)
    if problems:
        raise AuthError("Password must contain " + ", ".join(problems) + ".")
    if confirm is not None and password != confirm:
        raise AuthError("Passwords do not match.")


def _find_auth_row(login: str):
    """Look up a user by username or email (case-insensitive), including hashes."""
    return db._one(
        "SELECT * FROM users WHERE lower(username) = lower(?) OR (email <> '' AND lower(email) = lower(?))",
        (login.strip(), login.strip()),
    )


def _public(row: dict) -> dict:
    return {k: row[k] for k in ("user_id", "username", "full_name", "email", "age", "gender", "role")}


# ------------------------------------------------------------------ sign up
def register(username: str, password: str, confirm: str, security_question: str, security_answer: str,
             full_name: str = "", email: str = "", age=None, gender: str = "", role: str = "user") -> dict:
    username, email = username.strip(), email.strip()
    if not USERNAME_RE.match(username):
        raise AuthError("Username must be 3-30 characters: letters, digits, _ or . only.")
    if email and not EMAIL_RE.match(email):
        raise AuthError("Please enter a valid email address.")
    _check_password(password, confirm)
    if security_question not in SECURITY_QUESTIONS:
        raise AuthError("Please choose a security question.")
    if len(_normalise_answer(security_answer)) < 2:
        raise AuthError("Please enter an answer to the security question.")
    if _find_auth_row(username) or (email and _find_auth_row(email)):
        raise AuthError("That username or email is already registered.")
    try:
        user_id = db._execute(
            """INSERT INTO users (username, full_name, email, age, gender, created_at, password_hash,
                                  security_question, security_answer_hash, role)
               VALUES (?,?,?,?,?,?,?,?,?,?)""",
            (username, full_name.strip(), email, age, gender, db.now(), hash_secret(password),
             security_question, hash_secret(_normalise_answer(security_answer)), role),
        )
    except sqlite3.IntegrityError:
        raise AuthError("That username is already registered.")
    return db.get_user(user_id)


# ------------------------------------------------------------------ sign in
def login(username_or_email: str, password: str) -> dict:
    row = _find_auth_row(username_or_email)
    if not row:
        raise AuthError("Invalid username or password.")

    if row["locked_until"] and datetime.fromisoformat(row["locked_until"]) > datetime.now():
        mins = int((datetime.fromisoformat(row["locked_until"]) - datetime.now()).total_seconds() // 60) + 1
        raise AuthError(f"Account locked after too many wrong attempts. Try again in {mins} minute(s) "
                        "or use Forgot Password.")

    if not verify_secret(password, row["password_hash"]):
        attempts = row["failed_attempts"] + 1
        locked = (datetime.now() + timedelta(minutes=LOCK_MINUTES)).isoformat(timespec="seconds") \
            if attempts >= MAX_FAILED_ATTEMPTS else None
        db._execute("UPDATE users SET failed_attempts = ?, locked_until = ? WHERE user_id = ?",
                    (0 if locked else attempts, locked, row["user_id"]))
        if locked:
            raise AuthError(f"Too many wrong attempts. Account locked for {LOCK_MINUTES} minutes.")
        raise AuthError(f"Invalid username or password. {MAX_FAILED_ATTEMPTS - attempts} attempt(s) left.")

    db._execute("UPDATE users SET failed_attempts = 0, locked_until = NULL, last_login = ? WHERE user_id = ?",
                (db.now(), row["user_id"]))
    return _public(row)


# ---------------------------------------------------------- forgot password
def get_security_question(username_or_email: str) -> str:
    row = _find_auth_row(username_or_email)
    if not row or not row["security_question"]:
        raise AuthError("No account with a security question was found for that username / email.")
    return row["security_question"]


def reset_password_with_answer(username_or_email: str, answer: str, new_password: str, confirm: str) -> dict:
    row = _find_auth_row(username_or_email)
    if not row or not verify_secret(_normalise_answer(answer), row["security_answer_hash"]):
        raise AuthError("The security answer is incorrect.")
    _check_password(new_password, confirm)
    _set_password(row["user_id"], new_password)
    return _public(row)


# ----------------------------------------------------------- reset / change
def change_password(user_id: int, current_password: str, new_password: str, confirm: str):
    row = db._one("SELECT password_hash FROM users WHERE user_id = ?", (user_id,))
    if not row or not verify_secret(current_password, row["password_hash"]):
        raise AuthError("Current password is incorrect.")
    if current_password == new_password:
        raise AuthError("New password must be different from the current password.")
    _check_password(new_password, confirm)
    _set_password(user_id, new_password)


def admin_reset_password(user_id: int, new_password: str):
    """Admin sets a temporary password for a user (e.g. user forgot the security answer too)."""
    _check_password(new_password)
    _set_password(user_id, new_password)


def update_security_question(user_id: int, current_password: str, question: str, answer: str):
    row = db._one("SELECT password_hash FROM users WHERE user_id = ?", (user_id,))
    if not row or not verify_secret(current_password, row["password_hash"]):
        raise AuthError("Current password is incorrect.")
    if question not in SECURITY_QUESTIONS or len(_normalise_answer(answer)) < 2:
        raise AuthError("Choose a question and enter an answer.")
    db._execute("UPDATE users SET security_question = ?, security_answer_hash = ? WHERE user_id = ?",
                (question, hash_secret(_normalise_answer(answer)), user_id))


def _set_password(user_id: int, password: str):
    db._execute("UPDATE users SET password_hash = ?, failed_attempts = 0, locked_until = NULL WHERE user_id = ?",
                (hash_secret(password), user_id))
