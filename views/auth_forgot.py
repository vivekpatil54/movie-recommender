import streamlit as st

from src import auth, theme

theme.auth_background()
_, mid, _ = st.columns([1, 1.3, 1])
with mid:
    theme.auth_brand("Reset your password", "Verify it's you with your security question")
    state = st.session_state.setdefault("forgot", {})
    step2 = "question" in state
    theme._html(f'<div class="steps"><span class="{"" if step2 else "on"}">1 · Find account</span>'
                f'<span class="{"on" if step2 else ""}">2 · Verify &amp; reset</span></div>')

    if not step2:
        with st.form("forgot_step1"):
            login = st.text_input("Username or email", placeholder="e.g. user_1")
            if st.form_submit_button("Continue", type="primary", icon=":material/arrow_forward:", use_container_width=True):
                try:
                    state.update(login=login, question=auth.get_security_question(login))
                    st.rerun()
                except auth.AuthError as e:
                    st.error(str(e), icon=":material/error:")
    else:
        st.info(f"**Account:** {state['login']}  \n**Security question:** {state['question']}", icon=":material/help:")
        with st.form("forgot_step2"):
            answer = st.text_input("Your answer", type="password")
            new = st.text_input("New password", type="password", help="Min 8 characters with a letter and a digit")
            confirm = st.text_input("Confirm new password", type="password")
            ok = st.form_submit_button("Reset password", type="primary", icon=":material/lock_reset:", use_container_width=True)
        if ok:
            try:
                auth.reset_password_with_answer(state["login"], answer, new, confirm)
                st.session_state.pop("forgot")
                st.session_state.flash = True
                st.session_state.flash_msg = "Password reset successfully. Sign in with your new password."
                st.switch_page("views/auth_signin.py")
            except auth.AuthError as e:
                st.error(str(e), icon=":material/error:")
        if st.button("Use a different account", icon=":material/arrow_back:"):
            st.session_state.pop("forgot")
            st.rerun()
        st.caption("Forgot the answer too? Ask the administrator to set a temporary password for you.")

    st.page_link("views/auth_signin.py", label="Back to Sign in", icon=":material/login:")
