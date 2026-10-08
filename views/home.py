import streamlit as st

from src import client, db, llm, theme
from src.ui import auth_user, movie_cards, require_engine

me = auth_user()
name = (me["full_name"] or me["username"]).split()[0]
c = db.dashboard_counts()

theme._html(f"""
<section class="hero">
  <div class="hero-glow"></div>
  <span class="floaty" style="right:7%;top:22%;--r:-12deg">🍿</span>
  <span class="floaty" style="right:19%;top:58%;--r:10deg;animation-delay:-2s;font-size:34px">🎬</span>
  <span class="floaty" style="right:4%;top:66%;--r:8deg;animation-delay:-4s;font-size:30px">⭐</span>
  <span class="hero-badge">👋 Welcome back, {theme.esc(name)}</span>
  <div class="hero-title">Find your next <span class="grad-text">favourite movie</span><br/>with the power of AI</div>
  <p class="hero-sub">Machine learning, a deep neural network and an open-source LLM work together to understand
  your taste and recommend films you'll love.</p>
  <div class="hero-pills"><span>🌲 Random Forest</span><span>🧠 Keras ANN</span><span>🔗 SVD + TF-IDF</span><span>🤖 LangChain · Ollama</span></div>
</section>
""")

b1, b2, b3, _ = st.columns([1, 1, 1, 2])
if b1.button("Get recommendations", icon=":material/auto_awesome:", type="primary", use_container_width=True):
    st.switch_page("views/recommendations.py")
if b2.button("Chat with MovieBot", icon=":material/smart_toy:", use_container_width=True):
    st.switch_page("views/moviebot.py")
if b3.button("Rate movies", icon=":material/star:", use_container_width=True):
    st.switch_page("views/my_ratings.py")

theme.section("Platform at a glance", "📈")
theme.stat_cards([
    ("👥", "Users", f"{c['users']:,}", "#22D3EE"),
    ("🎬", "Movies", f"{c['movies']:,}", "#FF2E4D"),
    ("⭐", "Ratings", f"{c['ratings']:,}", "#FFB224"),
    ("🔖", "Watchlist items", f"{c['watchlist']:,}", "#34D399"),
    ("✨", "Recommendations", f"{c['recommendation_history']:,}", "#8B5CF6"),
    ("🎯", "Predictions", f"{c['predictions']:,}", "#F472B6"),
])

theme.section("How CineMind works", "⚙️")
theme._html("""
<div class="features">
  <div class="feature" style="--g:linear-gradient(135deg,#FF2E4D,#FF8A00)">
    <div class="feature-head"><div class="feature-icon">🧮</div><div><div class="feature-code">AI-503</div>
    <div class="feature-title">Machine Learning</div></div></div>
    <ul><li>TF-IDF content-based model</li><li>SVD collaborative filtering</li>
    <li>Random Forest &amp; Logistic Regression</li><li>Flask REST API + SQLite CRUD</li></ul>
  </div>
  <div class="feature" style="--g:linear-gradient(135deg,#8B5CF6,#22D3EE);animation-delay:.1s">
    <div class="feature-head"><div class="feature-icon">🧠</div><div><div class="feature-code">AI-505</div>
    <div class="feature-title">Deep Learning</div></div></div>
    <ul><li>Keras ANN · 128-64-32 neurons</li><li>Predicts Like / Dislike probability</li>
    <li>Re-ranks every recommendation</li><li>Loss, accuracy &amp; ROC evaluation</li></ul>
  </div>
  <div class="feature" style="--g:linear-gradient(135deg,#C026D3,#F472B6);animation-delay:.2s">
    <div class="feature-head"><div class="feature-icon">🤖</div><div><div class="feature-code">AI-504</div>
    <div class="feature-title">LLM &amp; AI Agent</div></div></div>
    <ul><li>Open-source LLM via Ollama</li><li>LangChain tool-calling agent</li>
    <li>Prompt-engineered explanations</li><li>AI-written Taste Report (PDF)</li></ul>
  </div>
</div>
""")

s = llm.ollama_status()
api = client.api_available()
provider_title = "Gemini" if s.get("provider") == "gemini" else "Ollama"
theme._html(
    '<div style="margin:-6px 0 4px">'
    + theme.pill("ok" if api else "warn", "Flask API", "running" if api else "local mode")
    + theme.pill("ok" if s["model_available"] else "off", f"{provider_title} · {s['model']}", "ready" if s["model_available"] else "offline")
    + "</div>"
)
if not s["model_available"]:
    st.caption(f":material/info: {llm.setup_hint()}")

theme.section("Most loved movies", "🔥")
engine = require_engine()
movie_cards(engine.popular(6), st.session_state.get("user_id"), key_prefix="home", score_label="score")
