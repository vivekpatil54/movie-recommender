"""Remember-me sessions ("Keep me signed in"): a signed cookie so a page refresh doesn't log the user out.

Token format:  <user_id>.<expiry_unix>.<password_fingerprint>.<hmac_sha256>
  * HMAC with a random server secret (database/.session_secret) -> cannot be forged or edited.
  * Password fingerprint -> changing the password signs out every remembered browser.
  * Expiry -> valid for REMEMBER_DAYS only.
"""
import hashlib
import hmac
import secrets
import time

import streamlit as st
import streamlit.components.v1 as components

from src import db
from src.config import DB_PATH

COOKIE = "cinemind_session"
REMEMBER_DAYS = 7
SECRET_PATH = DB_PATH.parent / ".session_secret"


def _secret() -> bytes:
    if not SECRET_PATH.exists():
        SECRET_PATH.parent.mkdir(parents=True, exist_ok=True)
        SECRET_PATH.write_text(secrets.token_hex(32))
    return SECRET_PATH.read_text().strip().encode()


def _fingerprint(user_id: int) -> str:
    row = db._one("SELECT password_hash FROM users WHERE user_id = ?", (user_id,))
    return hashlib.sha256((row or {}).get("password_hash", "").encode()).hexdigest()[:12] if row else ""


def _sign(payload: str) -> str:
    return hmac.new(_secret(), payload.encode(), hashlib.sha256).hexdigest()


def make_token(user_id: int, days: int = REMEMBER_DAYS) -> str:
    payload = f"{user_id}.{int(time.time()) + days * 86400}.{_fingerprint(user_id)}"
    return f"{payload}.{_sign(payload)}"


def verify_token(token: str):
    """Return the public user dict for a valid token, else None."""
    try:
        user_id, expiry, fp, sig = token.split(".")
        payload = f"{user_id}.{expiry}.{fp}"
        if not hmac.compare_digest(sig, _sign(payload)) or int(expiry) < time.time():
            return None
        if not fp or fp != _fingerprint(int(user_id)):
            return None
        return db.get_user(int(user_id))
    except (ValueError, AttributeError):
        return None


def _js_cookie(value: str, max_age: int):
    components.html(
        f"<script>window.parent.document.cookie = '{COOKIE}={value}; path=/; max-age={max_age}; SameSite=Strict';</script>",
        height=0,
    )


def remember(user_id: int):
    """Ask the app to store a remember-me cookie on the next render."""
    st.session_state.pending_cookie = make_token(user_id)


def forget():
    st.session_state.clear_cookie = True


def sync_cookie():
    """Write/clear the cookie in the browser (called once per run from app.py)."""
    if st.session_state.pop("clear_cookie", False):
        _js_cookie("", 0)
    token = st.session_state.pop("pending_cookie", None)
    if token:
        _js_cookie(token, REMEMBER_DAYS * 86400)


def restore_from_cookie():
    """Sign the user in from a valid cookie (unless they just logged out in this tab)."""
    if st.session_state.get("logged_out"):
        return None
    try:
        token = st.context.cookies.get(COOKIE)
    except Exception:  # no browser context (e.g. headless tests)
        return None
    return verify_token(token) if token else None
