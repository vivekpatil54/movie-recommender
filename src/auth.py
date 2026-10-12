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

VOWELS = set("aeiouyAEIOUY")
COMMON_2LETTER_ACCEPTED = {"dr", "mr", "ms", "ng", "al", "ed", "om", "li", "lu", "yu", "jo", "bo", "ty", "oz"}
KEYBOARD_PATTERNS = ["asdf", "qwer", "zxcv", "hjkl", "yuio", "sdfg", "dfgh", "fghj", "ghjk"]


POPULAR_EMAIL_DOMAINS = {
    "gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "icloud.com",
    "live.com", "msn.com", "me.com", "mac.com", "proton.me", "protonmail.com",
    "zoho.com", "aol.com", "mail.com", "yandex.com", "gmx.com", "rediffmail.com",
    "yahoo.co.in", "yahoo.in", "zoho.in", "outlook.in", "rediff.com", "example.com"
}

COMMON_TLDS = {
    "com", "org", "net", "edu", "gov", "mil", "int", "info", "biz", "name", "pro",
    "io", "ai", "co", "me", "app", "dev", "tech", "online", "site", "store", "cloud",
    "xyz", "live", "space", "tv", "fm", "cc", "ws", "mobi", "asia", "in", "us", "uk",
    "ca", "au", "de", "fr", "jp", "cn", "ru", "br", "za", "ch", "se", "nl", "eu",
    "es", "it", "sg", "nz", "ae", "sa", "pk", "bd", "lk", "np", "my", "id", "th",
    "vn", "ph", "kr", "mx", "ar", "cl", "ie", "no", "fi", "dk", "pl", "cz", "at",
    "be", "gr", "pt", "tr", "il", "ua", "ro", "hu"
}


class AuthError(Exception):
    """Raised with a user-friendly message when an auth action fails."""


def validate_username(username: str):
    """Validate username syntax, casing consistency, and prevent gibberish."""
    if not username:
        raise AuthError("Please enter a username.")
    u = username.strip()
    if not USERNAME_RE.match(u):
        raise AuthError("Username must be 3-30 characters: letters, digits, _ or . only.")
    if u.isdigit():
        raise AuthError("Username cannot consist only of numbers.")
    if not any(c.isalpha() for c in u):
        raise AuthError("Username must contain at least one letter.")

    has_upper = any(c.isupper() for c in u)
    has_lower = any(c.islower() for c in u)
    if has_upper and has_lower:
        raise AuthError(
            "Username cannot mix uppercase and lowercase letters (e.g. 'PaTIL_VIvek'). "
            "Please use all lowercase letters (e.g. 'patil_vivek')."
        )

    alpha_words = re.findall(r"[A-Za-z]+", u)
    for word in alpha_words:
        w_lower = word.lower()
        if len(w_lower) >= 4:
            v_count = sum(1 for ch in w_lower if ch in VOWELS)
            if v_count == 0:
                raise AuthError(f"Username segment '{word}' appears to be invalid or random text.")
            if re.search(r"[bcdfghjklmnpqrstvwxz]{5,}", w_lower):
                raise AuthError(f"Username segment '{word}' contains unrealistic consonant sequences.")
        if re.search(r"([A-Za-z])\1\1", word):
            raise AuthError(f"Username segment '{word}' contains repeated characters.")


def validate_full_name(name: str):
    """Validate a person's real-world full name.
    
    Rules:
    - Must be between 2 and 60 characters.
    - Letters, spaces, hyphens, and apostrophes only. No numbers.
    - Each word must follow standard capitalization:
        * Title Case ('Satish', 'Solanki')
        * all lowercase ('satish', 'nandu')
        * all uppercase ('SATISH', 'SOLANKI')
      Mixed internal casing like 'SatIsh' or 'SoLAnki' is rejected.
    - Words must be realistic (not keyboard spam like 'jhjdbvbbsdbdhdbvd', 'bcdhsbhcd', etc.):
        * Must contain at least one vowel per word (for words >= 3 chars, or accepted 2-char words)
        * No 5+ consecutive consonants
        * No 4+ consecutive vowels
        * No 3+ consecutive identical characters (e.g. 'aaa', 'bbb')
        * Realistic vowel-to-length ratio for longer words
    """
    if not name or not name.strip():
        raise AuthError("Please enter your full name.")
    clean_name = name.strip()

    if re.search(r"\d", clean_name):
        raise AuthError("Name cannot contain numbers. Names must contain only alphabetic letters and spaces.")

    if not re.match(r"^[A-Za-z]+(?:[ '-][A-Za-z]+)*$", clean_name):
        raise AuthError("Name can only contain alphabetic letters, spaces, hyphens, and apostrophes.")

    if len(clean_name) < 2 or len(clean_name) > 60:
        raise AuthError("Name must be between 2 and 60 characters.")

    words = [w for w in re.split(r"[ '-]+", clean_name) if w]
    if not words:
        raise AuthError("Please enter a valid human name.")

    # Casing check per word
    for word in words:
        if not (word.istitle() or word.islower() or word.isupper()):
            raise AuthError(
                f"Name contains invalid capitalization in '{word}'. "
                "Use standard Title Case (e.g. 'Satish Solanki'), all lowercase, or all uppercase."
            )

    # Phonetic realism / anti-gibberish checks per word
    for word in words:
        w_lower = word.lower()
        v_count = sum(1 for ch in w_lower if ch in VOWELS)

        if len(w_lower) >= 3 and v_count == 0:
            raise AuthError(f"'{word}' is not a valid name. Names must contain vowels.")
        elif len(w_lower) == 2 and v_count == 0 and w_lower not in COMMON_2LETTER_ACCEPTED:
            raise AuthError(f"'{word}' is not a valid name or prefix.")

        if re.search(r"([A-Za-z])\1\1", word):
            raise AuthError(f"'{word}' contains repeated characters and is not a valid name.")

        if re.search(r"[bcdfghjklmnpqrstvwxz]{5,}", w_lower):
            raise AuthError(f"'{word}' appears to be random or invalid text. Please enter a real name.")

        if re.search(r"[aeiouy]{4,}", w_lower):
            raise AuthError(f"'{word}' appears to be invalid. Please enter a real name.")

        for pat in KEYBOARD_PATTERNS:
            if pat in w_lower:
                raise AuthError(f"'{word}' appears to be keyboard pattern text. Please enter a real name.")

        if len(w_lower) >= 5 and (v_count / len(w_lower)) < 0.18:
            raise AuthError(f"'{word}' contains too many consonants. Please enter a real name.")


def validate_email(email: str):
    """Validate that email adheres to real-world formats and is not keyboard spam."""
    if not email:
        raise AuthError("Please enter a valid email address.")
    clean_email = email.strip()
    if len(clean_email) < 6 or len(clean_email) > 100:
        raise AuthError("Please enter a valid email address between 6 and 100 characters.")
    if "@" not in clean_email or clean_email.count("@") != 1:
        raise AuthError("Please enter a valid email address containing a single '@'.")

    local_part, domain = clean_email.split("@")

    if not local_part or not domain:
        raise AuthError("Please enter a complete email address (e.g. name@gmail.com).")

    if not re.match(r"^[A-Za-z0-9](?:[A-Za-z0-9._%+-]*[A-Za-z0-9])?$", local_part):
        raise AuthError("The email username format is invalid.")

    if ".." in local_part or ".." in domain:
        raise AuthError("Email address cannot contain consecutive dots ('..').")

    # Check local part gibberish (e.g. gsdshdgh)
    alpha_local = "".join(c for c in local_part if c.isalpha())
    if len(alpha_local) >= 4:
        v_count = sum(1 for c in alpha_local if c in VOWELS)
        if v_count == 0:
            raise AuthError("The email username appears to be invalid or random letters.")
        if re.search(r"[bcdfghjklmnpqrstvwxz]{5,}", alpha_local.lower()):
            raise AuthError("The email username contains unrealistic consonant sequences.")

    domain_lower = domain.lower()
    if domain_lower in POPULAR_EMAIL_DOMAINS:
        return

    domain_parts = domain_lower.split(".")
    if len(domain_parts) < 2:
        raise AuthError("Please enter a valid email domain (e.g. @gmail.com or @company.com).")

    tld = domain_parts[-1]
    second_tld = domain_parts[-2] if len(domain_parts) >= 3 else ""
    compound_tld = f"{second_tld}.{tld}" if second_tld in {"co", "ac", "edu", "gov", "org", "net", "res"} else tld

    if tld not in COMMON_TLDS and compound_tld not in COMMON_TLDS:
        raise AuthError(f"The email domain extension '.{tld}' is not recognized. Please use a valid real-world email.")

    main_domain = domain_parts[-2] if compound_tld == tld else (domain_parts[-3] if len(domain_parts) >= 3 else domain_parts[0])
    if len(main_domain) < 2:
        raise AuthError("The email domain name is too short.")

    if not re.match(r"^[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$", main_domain):
        raise AuthError("The email domain contains invalid characters.")

    # Check domain name gibberish (e.g. hdsh)
    alpha_domain = "".join(c for c in main_domain if c.isalpha())
    if len(alpha_domain) >= 3:
        v_dom = sum(1 for c in alpha_domain if c in VOWELS)
        if v_dom == 0:
            raise AuthError(f"The email domain '{main_domain}.{tld}' appears to be invalid or gibberish.")
        if re.search(r"[bcdfghjklmnpqrstvwxz]{5,}", alpha_domain):
            raise AuthError(f"The email domain '{main_domain}.{tld}' contains invalid consonant sequences.")


def validate_age(age) -> int:
    """Validate age requirement: must be 18 or older."""
    if age is None or age == "":
        return None
    try:
        age_int = int(age)
    except (ValueError, TypeError):
        raise AuthError("Please enter a valid numerical age.")
    if age_int < 18:
        raise AuthError("You must be at least 18 years old to register.")
    if age_int > 120:
        raise AuthError("Please enter a valid age between 18 and 120.")
    return age_int


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
    username = (username or "").strip()
    full_name = (full_name or "").strip()
    email = (email or "").strip()

    validate_username(username)

    if full_name:
        validate_full_name(full_name)

    if email:
        validate_email(email)

    validated_age = validate_age(age)

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
            (username, full_name, email, validated_age, gender, db.now(), hash_secret(password),
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
