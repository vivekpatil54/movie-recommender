import streamlit as st

from src import client, db, theme
from src.ui import GENRE_OPTIONS, clear_caches, is_admin, movie_picker

theme.page_header("🎬", "Movies", "Browse 9,700+ movies by title, tag, genre and year")

# Everyone can browse; only admins can add / edit / delete movies
if is_admin():
    tab_browse, tab_add, tab_edit = st.tabs([":material/search: Browse", ":material/add_circle: Add Movie", ":material/edit: Edit / Delete"])
else:
    tab_browse = st.container()

# ------------------------------------------------------------------- READ
with tab_browse:
    c1, c2, c3, c4 = st.columns([3, 2, 1, 1])
    text = c1.text_input("Search title or tag", placeholder="e.g. batman, time travel", icon=":material/search:")
    genre = c2.selectbox("Genre", [""] + GENRE_OPTIONS,
                         format_func=lambda g: f"{theme.GENRE_STYLE[g][0]} {g}" if g else "🎬 All genres")
    y_from = c3.number_input("From year", 1900, 2030, 1900)
    y_to = c4.number_input("To year", 1900, 2030, 2030)
    df = db.search_movies(text, genre, y_from, y_to, limit=200)
    st.caption(f"Showing {len(df)} movies (most-rated first, max 200)")
    st.dataframe(df, hide_index=True, use_container_width=True, column_config={
        "avg_rating": st.column_config.ProgressColumn("Avg rating", min_value=0, max_value=5, format="%.2f ★"),
        "year": st.column_config.NumberColumn("Year", format="%d"),
    })

if not is_admin():
    st.stop()

# ----------------------------------------------------------------- CREATE
with tab_add:
    with st.form("add_movie", clear_on_submit=True):
        title = st.text_input("Title *", placeholder="e.g. Jawan (2023)")
        year = st.number_input("Release year", 1890, 2035, 2024)
        genres = st.multiselect("Genres", GENRE_OPTIONS)
        tags = st.text_input("Tags (comma separated)", placeholder="action, shah rukh khan, heist")
        if st.form_submit_button("Add movie", type="primary", icon=":material/add:"):
            if not title.strip():
                st.error("Title is required.")
            else:
                new_id = db.create_movie(title, int(year), "|".join(genres) or None, tags.lower())
                clear_caches()
                client.catalogue_changed()
                st.success(f"Added '{title}' (id {new_id}). It can now be recommended by the content model.")

# --------------------------------------------------------- UPDATE / DELETE
with tab_edit:
    movie_id = movie_picker("Movie to edit", key="edit_movie")
    if movie_id:
        m = db.get_movie(movie_id)
        st.caption(f"id {m['movie_id']} · {m['num_ratings']} ratings · avg {m['avg_rating'] or '-'}★")
        with st.form("edit_movie_form"):
            title = st.text_input("Title", m["title"])
            year = st.number_input("Year", 1890, 2035, int(m["year"] or 2000))
            current = [g for g in m["genres"].split("|") if g in GENRE_OPTIONS]
            genres = st.multiselect("Genres", GENRE_OPTIONS, default=current)
            tags = st.text_area("Tags", m["tags"] or "")
            c1, c2 = st.columns(2)
            save = c1.form_submit_button("Save changes", type="primary", icon=":material/save:")
            confirm = c2.checkbox("I'm sure - delete this movie and its ratings")
            delete = c2.form_submit_button("Delete movie", icon=":material/delete:")
        if save:
            db.update_movie(movie_id, title, int(year), "|".join(genres) or None, tags)
            clear_caches()
            client.catalogue_changed()
            st.success("Movie updated.")
        if delete:
            if confirm:
                db.delete_movie(movie_id)
                clear_caches()
                client.catalogue_changed()
                st.success("Movie deleted.")
                st.rerun()
            else:
                st.warning("Tick the confirmation box to delete.")
