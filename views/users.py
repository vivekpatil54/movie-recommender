import sqlite3

import streamlit as st

from src import auth, db, theme
from src.ui import auth_user, clear_caches, require_admin

require_admin()
theme.page_header("🛡️", "Manage Users", "Create, edit, reset passwords, change roles and delete accounts")
GENDERS = ["", "Male", "Female", "Other"]
me = auth_user()

tab_list, tab_add, tab_edit = st.tabs([":material/group: All Users", ":material/person_add: Add User",
                                     ":material/manage_accounts: Edit / Reset / Delete"])

# ------------------------------------------------------------------- READ
with tab_list:
    users = db.list_users()
    c1, c2 = st.columns([3, 1])
    q = c1.text_input("Search username / name / email", icon=":material/search:")
    role = c2.selectbox("Role", ["All", "user", "admin"])
    view = users
    if q:
        view = view[view[["username", "full_name", "email"]].fillna("").apply(
            lambda r: q.lower() in " ".join(r).lower(), axis=1)]
    if role != "All":
        view = view[view["role"] == role]
    st.caption(f"{len(view)} of {len(users)} users")
    st.dataframe(view, hide_index=True, use_container_width=True)

# ----------------------------------------------------------------- CREATE
with tab_add:
    with st.form("add_user", clear_on_submit=True):
        c1, c2 = st.columns(2)
        username = c1.text_input("Username *")
        full_name = c2.text_input("Full name")
        email = st.text_input("Email")
        c3, c4, c5 = st.columns(3)
        age = c3.number_input("Age", 5, 100, 20)
        gender = c4.selectbox("Gender", GENDERS)
        new_role = c5.selectbox("Role", ["user", "admin"])
        c6, c7 = st.columns(2)
        password = c6.text_input("Password *", type="password")
        confirm = c7.text_input("Confirm password *", type="password")
        question = st.selectbox("Security question *", auth.SECURITY_QUESTIONS)
        answer = st.text_input("Security answer *", type="password")
        if st.form_submit_button("Create user", type="primary", icon=":material/person_add:"):
            try:
                u = auth.register(username, password, confirm, question, answer, full_name=full_name,
                                  email=email, age=int(age), gender=gender, role=new_role)
                clear_caches()
                st.success(f"Created {u['username']} (id {u['user_id']}, {u['role']}).")
            except auth.AuthError as e:
                st.error(str(e))

# --------------------------------------------------------- UPDATE / DELETE
with tab_edit:
    users = db.list_users()
    by_id = users.set_index("user_id")
    uid = st.selectbox("User", by_id.index, index=None, placeholder="Choose a user...",
                       format_func=lambda u: f"#{u} · {by_id.loc[u, 'username']} ({by_id.loc[u, 'role']})")
    if uid:
        uid = int(uid)
        u = db.get_user(uid)
        is_self = uid == me["user_id"]

        st.markdown("**Profile**")
        with st.form("edit_user"):
            username = st.text_input("Username", u["username"])
            full_name = st.text_input("Full name", u["full_name"] or "")
            email = st.text_input("Email", u["email"] or "")
            c1, c2, c3 = st.columns(3)
            age = c1.number_input("Age", 5, 100, int(u["age"] or 20))
            gender = c2.selectbox("Gender", GENDERS, index=GENDERS.index(u["gender"]) if u["gender"] in GENDERS else 0)
            new_role = c3.selectbox("Role", ["user", "admin"], index=0 if u["role"] == "user" else 1,
                                    disabled=is_self, help="You can't change your own role")
            if st.form_submit_button("Save changes", type="primary", icon=":material/save:"):
                try:
                    db.update_user(uid, username, full_name, email, int(age), gender)
                    if not is_self:
                        db.set_user_role(uid, new_role)
                    clear_caches()
                    st.success("User updated.")
                except sqlite3.IntegrityError:
                    st.error("That username is already taken.")

        c_reset, c_delete = st.columns(2)
        with c_reset:
            st.markdown("**Reset password**")
            st.caption("For users who forgot both their password and security answer.")
            with st.form("admin_reset", clear_on_submit=True):
                temp = st.text_input("Temporary password", type="password")
                if st.form_submit_button("Set temporary password", icon=":material/lock_reset:"):
                    try:
                        auth.admin_reset_password(uid, temp)
                        st.success("Password reset. Ask the user to change it from My Account.")
                    except auth.AuthError as e:
                        st.error(str(e))
        with c_delete:
            st.markdown("**Delete user**")
            st.caption("Deletes the user with all ratings, watchlist and history.")
            with st.form("admin_delete"):
                sure = st.checkbox("I'm sure")
                if st.form_submit_button("Delete user", disabled=is_self, icon=":material/person_remove:"):
                    if not sure:
                        st.warning("Tick the confirmation box.")
                    else:
                        db.delete_user(uid)
                        clear_caches()
                        st.rerun()
            if is_self:
                st.caption("Use My Account to delete your own account.")
