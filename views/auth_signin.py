import streamlit as st

from src import auth, session, theme
from src.ui import set_logged_in

theme.auth_background()
_, mid, _ = st.columns([1, 1.3, 1])
with mid:
    theme.auth_brand("Welcome back", "Sign in to get movie picks made just for you")

    if st.session_state.pop("flash", None):
        st.balloons()
        st.success(st.session_state.pop("flash_msg", "Done. Please sign in."), icon=":material/check_circle:")

    with st.form("signin"):
        login = st.text_input("Username or email", placeholder="e.g. user_1 or you@example.com")
        password = st.text_input("Password", type="password", placeholder="Your password")
        keep = st.checkbox("Keep me signed in for 7 days", value=True)
        submitted = st.form_submit_button("Sign In", type="primary", icon=":material/login:", use_container_width=True)
    if submitted:
        if not login or not password:
            st.error("Enter your username and password.", icon=":material/error:")
        else:
            try:
                with st.spinner("Signing you in..."):
                    user = auth.login(login, password)
                    set_logged_in(user)
                    st.session_state.pop("logged_out", None)
                    if keep:
                        session.remember(user["user_id"])
                st.rerun()
            except auth.AuthError as e:
                st.error(str(e), icon=":material/error:")

    c1, c2 = st.columns(2)
    c1.page_link("views/auth_signup.py", label="Create an account", icon=":material/person_add:")
    c2.page_link("views/auth_forgot.py", label="Forgot password?", icon=":material/lock_reset:")
    theme._html('<div class="auth-foot">🎬 TYBCA AI &amp; Data Analytics · Minor Project 2026-27 · Group 107</div>')
