"""CineMind - AI Based Movie Recommendation System (Streamlit dashboard).

Run:  streamlit run app.py
"""
import streamlit as st

from src.theme import ICON, LOGO  # noqa: E402

st.set_page_config(page_title="CineMind · AI Movie Recommender", page_icon=ICON, layout="wide")

from src import db, session  # noqa: E402
from src.ui import auth_user, inject_css, is_admin, set_logged_in, sidebar  # noqa: E402

db.init_db()
inject_css()
st.logo(LOGO, icon_image=ICON, size="large")

if not auth_user():
    remembered = session.restore_from_cookie()  # "Keep me signed in" survives a page refresh
    if remembered:
        set_logged_in(remembered)
session.sync_cookie()

if not auth_user():
    # Signed out: only the authentication pages are reachable
    nav = st.navigation([
        st.Page("views/auth_signin.py", title="Sign In", icon=":material/login:", default=True),
        st.Page("views/auth_signup.py", title="Sign Up", icon=":material/person_add:"),
        st.Page("views/auth_forgot.py", title="Forgot Password", icon=":material/lock_reset:"),
    ], position="hidden")
    nav.run()
    st.stop()

pages = {
    "": [st.Page("views/home.py", title="Home", icon=":material/home:", default=True)],
    "AI Features": [
        st.Page("views/recommendations.py", title="Recommendations", icon=":material/auto_awesome:"),
        st.Page("views/moviebot.py", title="MovieBot", icon=":material/smart_toy:"),
        st.Page("views/report.py", title="Taste Report", icon=":material/description:"),
    ],
    "My Library": [
        st.Page("views/my_ratings.py", title="Ratings & Watchlist", icon=":material/star:"),
        st.Page("views/movies.py", title="Movies", icon=":material/movie:"),
    ],
    "Insights": [
        st.Page("views/analytics.py", title="Analytics", icon=":material/monitoring:"),
        st.Page("views/model_performance.py", title="Model Performance", icon=":material/psychology:"),
    ],
    "Account": [st.Page("views/account.py", title="My Account", icon=":material/manage_accounts:")],
}
if is_admin():
    pages["Admin"] = [st.Page("views/users.py", title="Manage Users", icon=":material/admin_panel_settings:")]

nav = st.navigation(pages)
sidebar()
nav.run()
