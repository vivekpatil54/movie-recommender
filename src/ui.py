"""Shared Streamlit helpers (current user, movie pickers, recommendation cards)."""
import streamlit as st

from src import client, db, llm, theme
from src.config import GENRES
from src.recommender import MODELS, ModelsNotTrained, get_engine

GENRE_OPTIONS = GENRES[:-1]

def inject_css():
    theme.inject()


@st.cache_data(ttl=30)
def user_options() -> dict:
    df = db.list_users()
    return {int(r.user_id): f"#{r.user_id} · {r.username} ({r.num_ratings} ratings)" for r in df.itertuples()}


@st.cache_data(ttl=30)
def movie_options() -> dict:
    df = db.query_df("SELECT movie_id, title FROM movies ORDER BY title")
    return dict(zip(df["movie_id"].astype(int), df["title"]))


def clear_caches():
    user_options.clear()
    movie_options.clear()


# ------------------------------------------------------------ auth session
def auth_user():
    """The signed-in user (dict) or None."""
    return st.session_state.get("auth_user")


def is_admin() -> bool:
    u = auth_user()
    return bool(u and u["role"] == "admin")


def set_logged_in(user: dict):
    st.session_state.auth_user = user
    st.session_state.user_id = user["user_id"]


def logout():
    from src import session
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.session_state.logged_out = True  # don't auto sign-in again from the old cookie in this tab
    session.forget()
    st.rerun()


def require_admin():
    if not is_admin():
        st.error("Admins only.", icon=":material/block:")
        st.stop()


def sidebar():
    me = auth_user()
    with st.sidebar:
        name = me["full_name"] or me["username"]
        role = '<span class="role">ADMIN</span>' if me["role"] == "admin" else '<span class="role user">USER</span>'
        theme._html(f"""<div class="profile"><div class="avatar">{theme.initials(name)}</div>
            <div><div class="name">{theme.esc(name)}{role}</div><div class="handle">@{theme.esc(me['username'])}</div></div></div>""")

        if me["role"] == "admin":
            # Admins can view the app as any user (handy for demos with MovieLens users)
            users = user_options()
            ids = list(users)
            current = st.session_state.get("user_id", me["user_id"])
            st.session_state.user_id = st.selectbox(
                ":material/visibility: View app as user", ids, index=ids.index(current) if current in ids else 0,
                format_func=users.get,
            )
        else:
            st.session_state.user_id = me["user_id"]

        if st.button("Logout", icon=":material/logout:", use_container_width=True):
            logout()

        api = client.api_available()
        ollama = llm.ollama_status()
        theme._html(
            '<div style="margin-top:14px">'
            + theme.pill("ok" if api else "warn", "API", "Flask" if api else "Local")
            + theme.pill("ok" if ollama["model_available"] else "off", "LLM", "Online" if ollama["model_available"] else "Offline")
            + "</div>"
        )


def current_user_id():
    uid = st.session_state.get("user_id")
    if uid is None:
        st.info("Please sign in.")
        st.stop()
    return int(uid)


def require_engine():
    try:
        return get_engine()
    except ModelsNotTrained as e:
        st.error(f"Models are not trained yet. {e}")
        st.code("python -m src.train_all", language="bash")
        st.stop()


def movie_picker(label: str, key: str):
    options = movie_options()
    return st.selectbox(label, list(options), format_func=options.get, key=key, index=None,
                        placeholder="Type to search a movie...")


def model_picker(key: str, include_hybrid: bool = True):
    keys = [k for k in MODELS if include_hybrid or k != "hybrid"]
    return st.selectbox("AI model", keys, format_func=MODELS.get, key=key)


def movie_cards(items: list, user_id=None, key_prefix: str = "card", cols: int = 3, score_label: str = "match"):
    if not items:
        theme.empty_state("🍿", "No movies to show yet.")
        return
    columns = st.columns(cols)
    for i, it in enumerate(items):
        with columns[i % cols]:
            st.markdown(theme.movie_card_html(it, i + 1, score_label, delay_ms=i * 70), unsafe_allow_html=True)
            if user_id is not None and st.button("Add to watchlist", icon=":material/bookmark_add:",
                                                 key=f"{key_prefix}_{it['movie_id']}_{i}", use_container_width=True):
                db.add_to_watchlist(user_id, it["movie_id"])
                st.toast(f"Added **{it['title']}** to your watchlist", icon="🍿")
