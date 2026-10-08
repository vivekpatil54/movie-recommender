import streamlit as st

from src import db, theme
from src.ui import current_user_id, movie_picker

theme.page_header("⭐", "Ratings & Watchlist", "Rate movies to teach the AI your taste, and keep track of what to watch")
user_id = current_user_id()

ratings = db.get_user_ratings(user_id)
wl = db.get_watchlist(user_id)
theme.stat_cards([
    ("⭐", "Movies rated", len(ratings), "#FFB224"),
    ("📈", "Average rating", f"{ratings['rating'].mean():.2f} ★" if len(ratings) else "-", "#FF2E4D"),
    ("🔖", "On watchlist", int((wl["status"] != "Watched").sum()) if len(wl) else 0, "#8B5CF6"),
    ("✅", "Watched", int((wl["status"] == "Watched").sum()) if len(wl) else 0, "#34D399"),
])

tab_rate, tab_ratings, tab_watch = st.tabs([":material/add_reaction: Rate a Movie", ":material/star: My Ratings",
                                            ":material/bookmarks: My Watchlist"])

STARS = lambda r: "★" * int(r) + ("½" if r % 1 else "")  # noqa: E731

# ---------------------------------------------------------------- CREATE
with tab_rate:
    movie_id = movie_picker("Movie", key="rate_movie")
    if movie_id:
        m = db.get_movie(movie_id)
        st.markdown(theme.movie_card_html({**m, "score": (m["avg_rating"] or 0) / 5,
                                           "reason": f"Community: {m['avg_rating'] or '-'}★ from {m['num_ratings']} ratings"},
                                          1, "avg"), unsafe_allow_html=True)
    with st.form("rate_form", clear_on_submit=True):
        rating = st.slider("Your rating", 0.5, 5.0, 4.0, 0.5, format="%.1f ★")
        review = st.text_area("Review (optional)", max_chars=500, placeholder="What did you think?")
        add_watch = st.checkbox("Also mark as Watched in my watchlist")
        if st.form_submit_button("Save rating", type="primary", icon=":material/save:"):
            if not movie_id:
                st.error("Pick a movie first.", icon=":material/error:")
            else:
                db.upsert_rating(user_id, movie_id, rating, review)
                if add_watch:
                    db.add_to_watchlist(user_id, movie_id, "Watched")
                st.toast(f"Saved {STARS(rating)} for **{db.get_movie(movie_id)['title']}**", icon="⭐")
                st.success(f"Saved {rating}★ for {db.get_movie(movie_id)['title']}", icon=":material/check_circle:")

# --------------------------------------------------- READ / UPDATE / DELETE
with tab_ratings:
    if ratings.empty:
        theme.empty_state("🎬", "No ratings yet. Rate your first movie in the <b>Rate a Movie</b> tab!")
    else:
        q = st.text_input("Filter by title", key="rating_filter", placeholder="Search your ratings...",
                          icon=":material/search:")
        view = ratings[ratings["title"].str.contains(q, case=False, regex=False)] if q else ratings
        st.dataframe(view.drop(columns=["rating_id", "movie_id"]), hide_index=True, use_container_width=True,
                     column_config={"rating": st.column_config.ProgressColumn("Rating", min_value=0, max_value=5,
                                                                              format="%.1f ★")})

        theme.section("Edit or delete a rating", "✏️")
        by_id = view.set_index("rating_id")
        rid = st.selectbox("Rating", by_id.index, index=None, format_func=lambda r: by_id.loc[r, "title"],
                           placeholder="Choose a rated movie...")
        if rid:
            row = by_id.loc[rid]
            with st.form("edit_rating"):
                new_rating = st.slider("Rating", 0.5, 5.0, float(row["rating"]), 0.5, format="%.1f ★")
                new_review = st.text_area("Review", row["review"] or "")
                c1, c2 = st.columns(2)
                if c1.form_submit_button("Update", type="primary", icon=":material/edit:", use_container_width=True):
                    db.upsert_rating(user_id, int(row["movie_id"]), new_rating, new_review)
                    st.toast("Rating updated", icon="✏️")
                    st.rerun()
                if c2.form_submit_button("Delete", icon=":material/delete:", use_container_width=True):
                    db.delete_rating(int(rid))
                    st.toast("Rating deleted", icon="🗑️")
                    st.rerun()

with tab_watch:
    with st.expander("Add a movie to the watchlist", icon=":material/bookmark_add:"):
        c1, c2, c3 = st.columns([3, 1.4, 1], vertical_alignment="bottom")
        with c1:
            mid = movie_picker("Movie", key="watch_movie")
        status = c2.selectbox("Status", db.WATCH_STATUSES)
        if c3.button("Add", type="primary", icon=":material/add:", disabled=not mid, use_container_width=True):
            db.add_to_watchlist(user_id, mid, status)
            st.rerun()

    if wl.empty:
        theme.empty_state("🔖", "Your watchlist is empty. Add movies from Recommendations or above.")
    else:
        ICONS = {"Plan to Watch": "🕒", "Watching": "▶️", "Watched": "✅"}
        for status_name in db.WATCH_STATUSES:
            group = wl[wl["status"] == status_name]
            if group.empty:
                continue
            theme.section(f"{status_name} ({len(group)})", ICONS[status_name])
            for row in group.itertuples():
                with st.container(border=True):
                    emoji = theme.genre_style(row.genres)[0]
                    c1, c2, c3 = st.columns([5, 2.2, 0.6], vertical_alignment="center")
                    c1.markdown(f"**{emoji} {row.title}**  \n:gray[{row.genres.replace('|', ' · ')}]")
                    new = c2.selectbox("Status", db.WATCH_STATUSES, index=db.WATCH_STATUSES.index(row.status),
                                       key=f"ws_{row.watch_id}", label_visibility="collapsed")
                    if new != row.status:
                        db.update_watchlist_status(row.watch_id, new)
                        st.rerun()
                    if c3.button("", icon=":material/delete:", key=f"wd_{row.watch_id}", help="Remove"):
                        db.remove_from_watchlist(row.watch_id)
                        st.rerun()
