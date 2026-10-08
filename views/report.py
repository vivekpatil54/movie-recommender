import streamlit as st

from src import client, db, llm, theme
from src.report import build_pdf
from src.ui import current_user_id, require_engine

theme.page_header("📄", "Movie Taste Report", "An AI-written analysis of your taste with personal picks, as a PDF")
require_engine()
user_id = current_user_id()
user = db.get_user(user_id)

profile = client.profile(user_id)
if profile["num_ratings"] == 0:
    theme.empty_state("⭐", "Rate a few movies on <b>Ratings &amp; Watchlist</b> first, then come back for your report.")
    st.stop()

theme.stat_cards([
    ("🎬", "Movies rated", profile["num_ratings"], "#FF2E4D"),
    ("⭐", "Average rating", f"{profile['avg_rating']} ★", "#FFB224"),
    ("👍", "Liked (≥ 4★)", f"{profile['liked_pct']}%", "#34D399"),
    ("🏆", "Top genre", profile["top_genres"][0]["genre"] if profile["top_genres"] else "-", "#8B5CF6"),
])

left, right = st.columns([1.1, 1])
with left:
    theme.section("Your top genres", "🎭")
    top = profile["top_genres"]
    if top:
        most = max(g["count"] for g in top)
        theme.bars([(f"{theme.GENRE_STYLE.get(g['genre'], theme.DEFAULT_STYLE)[0]} {g['genre']}", g["count"] / most,
                     f"{g['avg_rating']}★") for g in top])
with right:
    theme.section("All-time favourites", "💖")
    for m in profile["favourite_movies"]:
        st.markdown(f":material/star: **{m['title']}** · {m['rating']}★")

st.write("")
if llm.setup_hint():
    st.caption(":material/info: LLM is offline - the report will use template text instead of AI-written analysis.")

if st.button("Generate my report", type="primary", icon=":material/auto_awesome:"):
    with st.status("Building your report...", expanded=True) as status:
        st.write(":material/neurology: Running the ANN to pick your top 10 movies...")
        recs = client.recommend(user_id, 10, "ann")
        st.write(":material/smart_toy: Asking the LLM to write your taste analysis...")
        text = llm.taste_report(user["username"], profile, recs)
        st.write(":material/picture_as_pdf: Creating the PDF...")
        st.session_state.report = {"user_id": user_id, "text": text, "pdf": build_pdf(user, profile, recs, text)}
        status.update(label="Report ready!", state="complete", expanded=False)

rep = st.session_state.get("report")
if rep and rep["user_id"] == user_id:
    theme.section("Preview", "👀")
    paragraphs = "".join(f"<p style='margin:0 0 10px'>{theme.esc(p)}</p>" for p in rep["text"].splitlines() if p.strip())
    theme._html(f'<div class="callout">{paragraphs}</div>')
    st.write("")
    st.download_button("Download PDF", rep["pdf"], file_name=f"taste_report_{user['username']}.pdf",
                       mime="application/pdf", type="primary", icon=":material/download:")
