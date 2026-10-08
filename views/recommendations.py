import streamlit as st

from src import client, db, theme
from src.recommender import MODELS
from src.ui import GENRE_OPTIONS, current_user_id, movie_cards, movie_picker, require_engine

theme.page_header("🎯", "Recommendations", "Personal picks from three ML models and a deep neural network")
require_engine()
user_id = current_user_id()

tab_for_you, tab_similar, tab_predict, tab_history = st.tabs([
    ":material/auto_awesome: For You", ":material/join_inner: Similar Movies",
    ":material/psychology: Will I Like It?", ":material/history: History",
])

with tab_for_you:
    with st.container(border=True):
        c1, c2, c3, c4 = st.columns([2, 2, 1, 1.2], vertical_alignment="bottom")
        model = c1.selectbox("AI model", list(MODELS), format_func=MODELS.get, key="rec_model")
        genre = c2.selectbox("Genre", [""] + GENRE_OPTIONS,
                             format_func=lambda g: f"{theme.GENRE_STYLE[g][0]} {g}" if g else "🎬 Any genre")
        n = c3.number_input("How many", 3, 30, 9, step=3)
        go = c4.button("Recommend", type="primary", icon=":material/auto_awesome:", use_container_width=True)
    if go or st.session_state.get("recs_user") != user_id:
        with st.spinner("Running the model..."):
            st.session_state.recs = client.recommend(user_id, int(n), model, genre)
            st.session_state.recs_user = user_id
            st.session_state.pop("explanation", None)

    recs = st.session_state.get("recs", [])
    if recs and recs[0]["reason"].startswith("Popular"):
        st.info("You haven't rated any movies yet, so these are popular picks. Rate a few movies for "
                "personalised results!", icon=":material/lightbulb:")
    movie_cards(recs, user_id, key_prefix="rec")

    if recs:
        if st.button("Explain these picks with AI", icon=":material/tips_and_updates:"):
            with st.spinner("Asking the LLM..."):
                st.session_state.explanation = client.explain(user_id, recs)
        if st.session_state.get("explanation"):
            with st.container(border=True):
                st.markdown("##### :violet[:material/smart_toy:] Why these picks")
                st.markdown(st.session_state.explanation)

with tab_similar:
    movie_id = movie_picker("Pick a movie you like", key="similar_movie")
    if movie_id:
        movie_cards(client.similar(movie_id, 9), user_id, key_prefix="sim", score_label="similar")
    else:
        theme.empty_state("🔍", "Choose a movie to discover similar titles.")

with tab_predict:
    st.markdown("Predict how likely you are to **like** a movie (rate it ≥ 4★), using all three trained models.")
    c1, c2 = st.columns([3, 1], vertical_alignment="bottom")
    with c1:
        movie_id = movie_picker("Pick a movie", key="predict_movie")
    run = c2.button("Predict", type="primary", icon=":material/bolt:", use_container_width=True, disabled=not movie_id)
    if movie_id and run:
        results = [client.predict(user_id, movie_id, m) for m in ["ann", "random_forest", "logistic_regression"]]
        left, right = st.columns([1, 2.2])
        with left:
            avg = sum(r["probability"] for r in results) / 3
            st.markdown(theme.movie_card_html({**results[0], "score": avg,
                                               "reason": "Average of the three models"}, 1, "like"),
                        unsafe_allow_html=True)
        with right:
            cards = ""
            for i, r in enumerate(results):
                pct = r["probability"] * 100
                verdict = "👍 Like" if r["label"] == "Like" else "👎 Dislike"
                cards += (
                    f'<div class="stat" style="--c:{theme.ring_color(pct)};animation-delay:{i * 90}ms">'
                    f'<div class="mv-ring" style="position:static;width:70px;height:70px;--p:{pct:.0f};'
                    f'--rc:{theme.ring_color(pct)};margin-bottom:10px"><span style="width:56px;height:56px;font-size:.9rem">'
                    f'{pct:.0f}%</span></div><div class="stat-value" style="font-size:1.05rem">{verdict}</div>'
                    f'<div class="stat-label">{theme.esc(r["model"])}</div></div>'
                )
            theme._html(f'<div class="stats" style="grid-template-columns:repeat(3,1fr)">{cards}</div>')
            agree = len({r["label"] for r in results}) == 1
            if agree:
                st.success(f"All three models agree: **{results[0]['label']}**", icon=":material/verified:")
            else:
                st.warning("The models disagree - this one could go either way!", icon=":material/balance:")
            if results[0]["already_rated"] is not None:
                st.caption(f":material/star: You already rated this movie {results[0]['already_rated']}★.")

with tab_history:
    theme.section("Recent recommendations", "🕘")
    hist = db.get_recommendation_history(user_id)
    if hist.empty:
        theme.empty_state("📭", "No recommendations yet.")
    else:
        st.dataframe(hist, hide_index=True, use_container_width=True, column_config={
            "score": st.column_config.ProgressColumn("Match", min_value=0, max_value=1, format="percent")})
        if st.button("Clear recommendation history", icon=":material/delete_sweep:"):
            db.clear_recommendation_history(user_id)
            st.rerun()

    theme.section("Prediction log", "🎯")
    preds = db.get_predictions(user_id)
    if preds.empty:
        theme.empty_state("🧪", "No predictions yet - try the Will I Like It? tab.")
    else:
        st.dataframe(preds, hide_index=True, use_container_width=True, column_config={
            "probability": st.column_config.ProgressColumn("Probability", min_value=0, max_value=1, format="percent")})
        c1, c2 = st.columns([3, 1], vertical_alignment="bottom")
        pid = c1.selectbox("Delete a prediction record", preds["prediction_id"], index=None,
                           format_func=lambda p: f"#{p} · " + preds.set_index("prediction_id").loc[p, "title"])
        if c2.button("Delete record", icon=":material/delete:", disabled=not pid, use_container_width=True):
            db.delete_prediction(int(pid))
            st.rerun()
