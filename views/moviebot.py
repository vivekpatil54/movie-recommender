import streamlit as st

from src import client, llm, theme
from src.ui import current_user_id, require_engine

status = llm.ollama_status()
hint = llm.setup_hint()
provider_label = "Google Gemini" if status.get("provider") == "gemini" else "Ollama"
model_label = status.get("model", "AI")

theme.page_header("🤖", "MovieBot", f"An AI agent powered by <b>{model_label}</b> ({provider_label}) using tools")
require_engine()
user_id = current_user_id()

theme._html(theme.pill("ok" if status["model_available"] else "off", f"{provider_label}",
                       f"{model_label} ready" if status["model_available"] else "offline"))
if hint:
    st.warning(hint, icon=":material/cloud_off:")

key = f"chat_{user_id}"
history = st.session_state.setdefault(key, [])
BOT, ME = "🤖", "🧑"

SUGGESTIONS = {
    "🚀 Sci-fi picks": "Recommend me some sci-fi movies",
    "🦇 Like The Dark Knight": "Movies like The Dark Knight",
    "🚢 Will I like Titanic?": "Will I like Titanic?",
    "🎭 My movie taste": "What's my movie taste?",
    "🔖 Add Inception": "Add Inception to my watchlist",
}

if not history:
    with st.chat_message("assistant", avatar=BOT):
        st.markdown("Hi! I'm **MovieBot** 🎬. Ask me for recommendations, similar movies, whether you'd like a "
                    "film, or tell me to add something to your watchlist.")
    choice = st.pills("Try asking", list(SUGGESTIONS), label_visibility="collapsed")
    if choice:
        st.session_state.pending = SUGGESTIONS[choice]

for msg in history:
    with st.chat_message(msg["role"], avatar=BOT if msg["role"] == "assistant" else ME):
        st.markdown(msg["content"])

if history and st.button("Clear chat", icon=":material/delete_sweep:"):
    history.clear()
    st.rerun()

prompt = st.chat_input("Ask MovieBot anything about movies...") or st.session_state.pop("pending", None)
if prompt:
    with st.chat_message("user", avatar=ME):
        st.markdown(prompt)
    with st.chat_message("assistant", avatar=BOT):
        with st.spinner("MovieBot is thinking..."):
            try:
                res = client.chat(user_id, prompt, [{"role": m["role"], "content": m["content"]} for m in history])
            except Exception as e:
                res = {"reply": f"⚠️ Error talking to the LLM: {e}", "tool_calls": []}
    history.append({"role": "user", "content": prompt})
    history.append({"role": "assistant", "content": res["reply"], "tool_calls": res["tool_calls"]})
    st.rerun()
