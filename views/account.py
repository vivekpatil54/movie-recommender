import sqlite3

import streamlit as st

from src import auth, db, theme
from src.ui import auth_user, logout, set_logged_in

theme.page_header("⚙️", "My Account", "Your profile, password and security settings")
me = auth_user()
GENDERS = ["", "Male", "Female", "Other"]

tab_profile, tab_password, tab_security, tab_delete = st.tabs(
    [":material/person: Profile", ":material/password: Change Password", ":material/shield: Security Question",
     ":material/warning: Delete Account"]
)

with tab_profile:
    u = db.get_user(me["user_id"])
    name = u["full_name"] or u["username"]
    role = '<span class="role">ADMIN</span>' if u["role"] == "admin" else '<span class="role user">USER</span>'
    theme._html(f"""<div class="profile" style="max-width:560px"><div class="avatar" style="width:58px;height:58px;font-size:1.3rem">
        {theme.initials(name)}</div><div><div class="name" style="font-size:1.1rem">{theme.esc(name)}{role}</div>
        <div class="handle">@{theme.esc(u['username'])} · member since {u['created_at'][:10]} ·
        last login {theme.esc((u['last_login'] or '-').replace('T', ' '))}</div></div></div>""")
    with st.form("profile"):
        username = st.text_input("Username", u["username"])
        full_name = st.text_input("Full name", u["full_name"] or "")
        email = st.text_input("Email", u["email"] or "")
        c1, c2 = st.columns(2)
        age = c1.number_input("Age", 5, 100, int(u["age"] or 20))
        gender = c2.selectbox("Gender", GENDERS, index=GENDERS.index(u["gender"]) if u["gender"] in GENDERS else 0)
        if st.form_submit_button("Save profile", type="primary", icon=":material/save:"):
            if not auth.USERNAME_RE.match(username.strip()):
                st.error("Username must be 3-30 characters: letters, digits, _ or . only.")
            elif email and not auth.EMAIL_RE.match(email.strip()):
                st.error("Please enter a valid email address.")
            else:
                try:
                    db.update_user(me["user_id"], username, full_name, email.strip(), int(age), gender)
                    set_logged_in({**me, **db.get_user(me["user_id"])})
                    st.success("Profile updated.")
                except sqlite3.IntegrityError:
                    st.error("That username is already taken.")

with tab_password:
    with st.form("change_pw", clear_on_submit=True):
        current = st.text_input("Current password", type="password")
        new = st.text_input("New password", type="password", help="Min 8 characters with a letter and a digit")
        confirm = st.text_input("Confirm new password", type="password")
        if st.form_submit_button("Change password", type="primary", icon=":material/password:"):
            try:
                auth.change_password(me["user_id"], current, new, confirm)
                from src import session
                session.remember(me["user_id"])  # old remembered browsers are signed out; keep this one
                st.success("Password changed successfully. Other remembered devices have been signed out.")
            except auth.AuthError as e:
                st.error(str(e))

with tab_security:
    st.write("Used on the **Forgot Password** page to verify it's you.")
    with st.form("security", clear_on_submit=True):
        question = st.selectbox("New security question", auth.SECURITY_QUESTIONS)
        answer = st.text_input("Answer", type="password")
        current = st.text_input("Current password (to confirm)", type="password")
        if st.form_submit_button("Update security question", type="primary", icon=":material/shield:"):
            try:
                auth.update_security_question(me["user_id"], current, question, answer)
                st.success("Security question updated.")
            except auth.AuthError as e:
                st.error(str(e))

with tab_delete:
    st.warning("This permanently deletes your account, ratings, watchlist and history.")
    with st.form("delete_me"):
        current = st.text_input("Password", type="password")
        sure = st.checkbox("Yes, delete my account permanently")
        if st.form_submit_button("Delete my account", icon=":material/delete_forever:"):
            if me["role"] == "admin" and len(db.query_df("SELECT 1 FROM users WHERE role='admin'")) == 1:
                st.error("You are the only admin - make another user admin before deleting this account.")
            elif not sure:
                st.error("Tick the confirmation box.")
            else:
                try:
                    auth.login(me["username"], current)
                    db.delete_user(me["user_id"])
                    logout()
                except auth.AuthError:
                    st.error("Password is incorrect.")
