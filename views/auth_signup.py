import streamlit as st

from src import auth, theme

GENDERS = ["", "Male", "Female", "Other"]

theme.auth_background()
_, mid, _ = st.columns([1, 1.8, 1])
with mid:
    theme.auth_brand("Create your account", "Join CineMind and let AI find your next favourite movie")

    with st.form("signup"):
        c1, c2 = st.columns(2)
        username = c1.text_input("Username *", placeholder="rahul_patil", help="3-30 characters: letters, digits, _ or .")
        full_name = c2.text_input("Full name", placeholder="Rahul Patil")
        email = st.text_input("Email", placeholder="you@example.com")
        c3, c4 = st.columns(2)
        age = c3.number_input("Age", 5, 100, 20)
        gender = c4.selectbox("Gender", GENDERS, format_func=lambda g: g or "Prefer not to say")
        c5, c6 = st.columns(2)
        password = c5.text_input("Password *", type="password", help="Min 8 characters with a letter and a digit")
        confirm = c6.text_input("Confirm password *", type="password")
        st.markdown("**:material/shield: Security question** · used to reset your password if you forget it")
        question = st.selectbox("Question *", auth.SECURITY_QUESTIONS)
        answer = st.text_input("Answer *", type="password", help="Not case-sensitive")
        agree = st.checkbox("I confirm the details above are correct")
        submitted = st.form_submit_button("Create account", type="primary", icon=":material/person_add:", use_container_width=True)

    if submitted:
        if not agree:
            st.error("Please tick the confirmation box.", icon=":material/error:")
        else:
            try:
                user = auth.register(username, password, confirm, question, answer,
                                     full_name=full_name, email=email, age=int(age), gender=gender)
                st.session_state.flash = True
                st.session_state.flash_msg = f"Account '{user['username']}' created. Please sign in."
                st.switch_page("views/auth_signin.py")
            except auth.AuthError as e:
                st.error(str(e), icon=":material/error:")

    st.page_link("views/auth_signin.py", label="Already have an account? Sign in", icon=":material/login:")
