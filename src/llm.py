"""AI-504: LLM features with Google Gemini (via API Key from .env) and Ollama fallback.

1. MovieBot  - a tool-using AI agent. The LLM decides which tool to call
               (search the database, recommend, predict, add to watchlist ...),
               we execute it, feed the result back, and the LLM writes the answer.
2. Chains    - prompt-engineered templates that explain recommendations and write
               the user's "Taste Report" (with PDF export).

Prompt-engineering techniques used:
  * Role prompting         - "You are MovieBot, ..." persona with clear scope
  * Explicit rules         - grounding: only mention movies returned by tools
  * Few-shot examples      - example dialogues showing which tool to use
  * Output formatting      - markdown bullet lists, word limits
  * Context injection      - user profile + model output inserted into templates
  * Low temperature        - deterministic, factual answers
"""
import json
import time

import requests

from src import db
from src.config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    LLM_PROVIDER,
    OLLAMA_BASE_URL,
    OLLAMA_MODEL,
)

MAX_TOOL_ROUNDS = 5
GEMINI_FALLBACK_MODELS = [
    GEMINI_MODEL,
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.7-flash",
    "gemini-flash-lite-latest",
]

AGENT_SYSTEM_PROMPT = """You are MovieBot, the friendly movie assistant of the "AI Movie Recommendation System".
You are talking to the user "{username}" (user_id {user_id}).

RULES
1. Use the tools to get facts. Only mention movies that a tool returned - never invent titles, years or ratings.
2. For "recommend me / what should I watch" use recommend_for_me (pass a genre if the user mentioned one).
3. For "movies like X" use similar_to. For "will I like X" use predict_my_opinion.
4. For "add X to my watchlist" use add_to_watchlist. For "rate X 4 stars" use rate_movie.
5. For questions about the user's own taste use my_taste_profile.
6. If a tool returns nothing, say so honestly and suggest another search.
7. Answer in short markdown: a one-line intro, then a bullet list "**Title (Year)** - one-line reason". Max 150 words.
8. Politely refuse topics unrelated to movies.

EXAMPLES
User: suggest some horror movies
Assistant: (calls recommend_for_me with genre="Horror", then lists the results with reasons)

User: anything like Inception?
Assistant: (calls similar_to with title="Inception", then lists the results)

User: would I enjoy Titanic?
Assistant: (calls predict_my_opinion with title="Titanic", then explains the probability in plain words)
"""

EXPLAIN_PROMPT = """You are a film critic writing for a movie app.
User taste profile (JSON): {profile}
Movies our AI model recommended (JSON, score = like-probability): {recommendations}

Task: In 2-3 friendly sentences, explain the overall pattern of why these movies suit this user,
referring to their favourite genres and movies. Then give a one-line reason for the top 3 picks
as a markdown bullet list. Do not mention any movie that is not in the JSON above. Max 140 words."""

REPORT_PROMPT = """You are a professional film analyst. Write a personalised "Movie Taste Report".
User: {username}
Taste profile (JSON): {profile}
Top AI recommendations (JSON): {recommendations}

Write exactly these sections in plain text (no markdown symbols like ** or #):
Taste Summary: 3-4 sentences describing the user's taste using the genres and favourite movies.
Viewing Personality: one creative 3-5 word label and one sentence explaining it.
Why These Recommendations: 2-3 sentences linking the recommendations to the taste profile.
Try Something New: one genre the user rarely watches and why they might enjoy it.
Use only facts from the JSON. Max 250 words."""

# Gemini Tool Declarations for Function Calling
GEMINI_TOOLS_DECL = [
    {
        "function_declarations": [
            {
                "name": "search_movies",
                "description": "Search the movie database by title/keyword text, genre (e.g. Comedy, Sci-Fi) and release year range.",
                "parameters": {
                    "type": "OBJECT",
                    "properties": {
                        "query": {"type": "STRING", "description": "Movie title or keyword to search for"},
                        "genre": {"type": "STRING", "description": "Genre filter (e.g. Comedy, Action, Horror)"},
                        "year_from": {"type": "INTEGER", "description": "Minimum release year"},
                        "year_to": {"type": "INTEGER", "description": "Maximum release year"},
                    },
                },
            },
            {
                "name": "recommend_for_me",
                "description": "Personalised recommendations for the current user from the trained AI model. Optional genre filter.",
                "parameters": {
                    "type": "OBJECT",
                    "properties": {
                        "genre": {"type": "STRING", "description": "Optional genre filter (e.g. Sci-Fi, Drama)"},
                        "count": {"type": "INTEGER", "description": "Number of movies to recommend (1 to 10)"},
                    },
                },
            },
            {
                "name": "similar_to",
                "description": "Find movies similar to the given movie title.",
                "parameters": {
                    "type": "OBJECT",
                    "properties": {
                        "title": {"type": "STRING", "description": "Movie title to find similar films for"},
                        "count": {"type": "INTEGER", "description": "Number of similar movies (1 to 10)"},
                    },
                    "required": ["title"],
                },
            },
            {
                "name": "predict_my_opinion",
                "description": "Predict with the neural network how likely the current user is to like a movie.",
                "parameters": {
                    "type": "OBJECT",
                    "properties": {
                        "title": {"type": "STRING", "description": "Movie title to predict user opinion for"}
                    },
                    "required": ["title"],
                },
            },
            {
                "name": "my_taste_profile",
                "description": "The current user's favourite genres, favourite movies and rating habits.",
                "parameters": {
                    "type": "OBJECT",
                    "properties": {},
                },
            },
            {
                "name": "add_to_watchlist",
                "description": "Add a movie to the current user's watchlist.",
                "parameters": {
                    "type": "OBJECT",
                    "properties": {
                        "title": {"type": "STRING", "description": "Movie title to add to watchlist"}
                    },
                    "required": ["title"],
                },
            },
            {
                "name": "rate_movie",
                "description": "Save the current user's rating (0.5 to 5.0 stars) for a movie.",
                "parameters": {
                    "type": "OBJECT",
                    "properties": {
                        "title": {"type": "STRING", "description": "Movie title to rate"},
                        "rating": {"type": "NUMBER", "description": "Star rating from 0.5 to 5.0"},
                    },
                    "required": ["title", "rating"],
                },
            },
        ]
    }
]

# ------------------------------------------------------------------ status
_status_cache = {"at": 0.0, "value": None}


def ollama_status() -> dict:
    """Check LLM provider status (Gemini if configured with API key, else Ollama)."""
    if _status_cache["value"] and time.time() - _status_cache["at"] < 15:
        return _status_cache["value"]
    _status_cache["value"] = _probe_llm()
    _status_cache["at"] = time.time()
    return _status_cache["value"]


def llm_status() -> dict:
    """Alias for ollama_status for provider-agnostic status checking."""
    return ollama_status()


def _probe_llm() -> dict:
    if LLM_PROVIDER == "gemini" or (GEMINI_API_KEY and LLM_PROVIDER != "ollama"):
        if not GEMINI_API_KEY:
            return {"provider": "gemini", "running": False, "model": GEMINI_MODEL, "model_available": False, "installed_models": []}
        return {
            "provider": "gemini",
            "running": True,
            "model": GEMINI_MODEL,
            "model_available": True,
            "installed_models": list(dict.fromkeys(GEMINI_FALLBACK_MODELS)),
        }
    return _probe_ollama()


def _probe_ollama() -> dict:
    try:
        r = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=1)
        r.raise_for_status()
        names = [m["name"] for m in r.json().get("models", [])]
        has_model = any(n == OLLAMA_MODEL or n.split(":")[0] == OLLAMA_MODEL.split(":")[0] for n in names)
        return {"provider": "ollama", "running": True, "model": OLLAMA_MODEL, "model_available": has_model, "installed_models": names}
    except requests.RequestException:
        return {"provider": "ollama", "running": False, "model": OLLAMA_MODEL, "model_available": False, "installed_models": []}


def setup_hint() -> str:
    s = ollama_status()
    if s.get("provider") == "gemini":
        if not GEMINI_API_KEY:
            return "Gemini API key is missing. Add GEMINI_API_KEY in your .env file."
        return ""
    if not s["running"]:
        return ("Ollama is not running. Install it from https://ollama.com, then run "
                f"`ollama pull {OLLAMA_MODEL}` or set GEMINI_API_KEY in .env.")
    if not s["model_available"]:
        return f"Ollama is running but the model is missing. Run: `ollama pull {OLLAMA_MODEL}`"
    return ""


# ------------------------------------------------------------------- tools
def _fmt(items: list) -> str:
    return json.dumps(
        [{k: it.get(k) for k in ("title", "year", "genres", "score", "reason") if k in it} for it in items]
    )


def _exec_tool(name: str, args: dict, user_id: int, engine) -> str:
    args = args or {}
    if name == "search_movies":
        query = str(args.get("query", "") or "")
        genre = str(args.get("genre", "") or "")
        try:
            yf = int(float(args.get("year_from", 0) or 0))
        except (ValueError, TypeError):
            yf = 0
        try:
            yt = int(float(args.get("year_to", 0) or 0))
        except (ValueError, TypeError):
            yt = 0
        df = db.search_movies(query, genre, yf or None, yt or None, limit=8)
        return df.to_json(orient="records") if not df.empty else "No movies found."
    elif name == "recommend_for_me":
        genre = str(args.get("genre", "") or "")
        try:
            count = max(1, min(int(float(args.get("count", 5))), 10))
        except (ValueError, TypeError):
            count = 5
        items = engine.recommend(user_id, n=count, model="ann", genre=genre)
        return _fmt(items) or "[]"
    elif name == "similar_to":
        title = str(args.get("title", "") or "")
        try:
            count = max(1, min(int(float(args.get("count", 5))), 10))
        except (ValueError, TypeError):
            count = 5
        movie = db.find_movie_by_title(title)
        if not movie:
            return f"Movie '{title}' not found in the database."
        return json.dumps({
            "matched_movie": movie["title"],
            "similar": json.loads(_fmt(engine.similar_movies(movie["movie_id"], count))),
        })
    elif name == "predict_my_opinion":
        title = str(args.get("title", "") or "")
        movie = db.find_movie_by_title(title)
        if not movie:
            return f"Movie '{title}' not found in the database."
        res = engine.predict(user_id, movie["movie_id"], "ann")
        db.log_prediction(user_id, movie["movie_id"], "ANN (Keras)", res["probability"], res["label"])
        return json.dumps(res)
    elif name == "my_taste_profile":
        return json.dumps(engine.user_profile(user_id))
    elif name == "add_to_watchlist":
        title = str(args.get("title", "") or "")
        movie = db.find_movie_by_title(title)
        if not movie:
            return f"Movie '{title}' not found in the database."
        db.add_to_watchlist(user_id, movie["movie_id"])
        return f"Added '{movie['title']}' to the watchlist."
    elif name == "rate_movie":
        title = str(args.get("title", "") or "")
        movie = db.find_movie_by_title(title)
        if not movie:
            return f"Movie '{title}' not found in the database."
        try:
            raw_r = float(args.get("rating", 5.0))
            rating = min(5.0, max(0.5, round(raw_r * 2) / 2))
        except (ValueError, TypeError):
            rating = 5.0
        db.upsert_rating(user_id, movie["movie_id"], rating)
        return f"Saved {rating} stars for '{movie['title']}'."
    return f"Unknown tool {name}"


def _gemini_generate(prompt: str, system_instruction: str = "", temperature: float = 0.2) -> str:
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set.")
    
    last_err = None
    models = list(dict.fromkeys(GEMINI_FALLBACK_MODELS))
    for model_name in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={GEMINI_API_KEY}"
        payload = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": temperature},
        }
        if system_instruction:
            payload["system_instruction"] = {"parts": [{"text": system_instruction}]}
        try:
            r = requests.post(url, json=payload, timeout=25)
            if r.status_code == 200:
                data = r.json()
                return data["candidates"][0]["content"]["parts"][0]["text"].strip()
            elif r.status_code in (429, 503, 404):
                last_err = Exception(f"Model {model_name} returned status {r.status_code}")
                continue
            else:
                r.raise_for_status()
        except requests.RequestException as e:
            last_err = e
            continue
    raise last_err or Exception("All Gemini models failed.")


def _gemini_chat(user_id: int, message: str, history: list, engine) -> dict:
    user = db.get_user(user_id) or {"username": f"user_{user_id}"}
    system_text = AGENT_SYSTEM_PROMPT.format(username=user["username"], user_id=user_id)

    base_contents = []
    for h in history[-10:]:
        role = "user" if h["role"] == "user" else "model"
        base_contents.append({"role": role, "parts": [{"text": h["content"]}]})
    base_contents.append({"role": "user", "parts": [{"text": message}]})

    trace = []
    models = list(dict.fromkeys(GEMINI_FALLBACK_MODELS))

    for model_name in models:
        try:
            working_contents = list(base_contents)
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={GEMINI_API_KEY}"

            for _ in range(MAX_TOOL_ROUNDS):
                payload = {
                    "contents": working_contents,
                    "tools": GEMINI_TOOLS_DECL,
                    "system_instruction": {"parts": [{"text": system_text}]},
                    "generationConfig": {"temperature": 0.2},
                }
                r = requests.post(url, json=payload, timeout=25)
                if r.status_code != 200:
                    break

                res = r.json()
                candidates = res.get("candidates", [])
                if not candidates:
                    break
                candidate = candidates[0]
                content = candidate.get("content", {})
                parts = content.get("parts", [])

                func_calls = [p["functionCall"] for p in parts if "functionCall" in p]
                if not func_calls:
                    reply_text = "".join(p.get("text", "") for p in parts)
                    return {"reply": reply_text.strip(), "tool_calls": trace}

                working_contents.append(content)
                for fc in func_calls:
                    fn_name = fc.get("name")
                    fn_args = fc.get("args", {})
                    fn_result = _exec_tool(fn_name, fn_args, user_id, engine)
                    trace.append({"tool": fn_name, "args": fn_args, "result": str(fn_result)[:1500]})
                    working_contents.append({
                        "role": "user",
                        "parts": [{
                            "functionResponse": {
                                "name": fn_name,
                                "response": {"name": fn_name, "content": fn_result},
                            }
                        }],
                    })

            if candidates and parts:
                text = "".join(p.get("text", "") for p in parts)
                if text:
                    return {"reply": text.strip(), "tool_calls": trace}
        except Exception:
            continue

    return {"reply": "⚠️ MovieBot encountered an issue contacting Gemini. Please try again in a moment.", "tool_calls": trace}


# ------------------------------------------------------------------- agent
def chat(user_id: int, message: str, history: list, engine) -> dict:
    """Run one agent turn. history = [{"role": "user"|"assistant", "content": str}, ...]

    Returns {"reply": str, "tool_calls": [{"tool", "args", "result"}]}.
    """
    hint = setup_hint()
    if hint:
        return {"reply": f"⚠️ MovieBot is offline. {hint}", "tool_calls": []}

    if GEMINI_API_KEY and (LLM_PROVIDER == "gemini" or LLM_PROVIDER != "ollama"):
        return _gemini_chat(user_id, message, history, engine)

    # Ollama + LangChain Fallback
    try:
        from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
        from langchain_ollama import ChatOllama

        user = db.get_user(user_id) or {"username": f"user_{user_id}"}
        llm = ChatOllama(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL, temperature=0.2)
        # Wrap tool execution
        from langchain_core.tools import tool

        @tool
        def search_movies(query: str = "", genre: str = "", year_from: int = 0, year_to: int = 0) -> str:
            """Search the movie database by title/keyword text, genre and release year range."""
            return _exec_tool("search_movies", {"query": query, "genre": genre, "year_from": year_from, "year_to": year_to}, user_id, engine)

        @tool
        def recommend_for_me(genre: str = "", count: int = 5) -> str:
            """Personalised recommendations for the current user from the trained AI model."""
            return _exec_tool("recommend_for_me", {"genre": genre, "count": count}, user_id, engine)

        @tool
        def similar_to(title: str, count: int = 5) -> str:
            """Find movies similar to the given movie title."""
            return _exec_tool("similar_to", {"title": title, "count": count}, user_id, engine)

        @tool
        def predict_my_opinion(title: str) -> str:
            """Predict with the neural network how likely the current user is to like a movie."""
            return _exec_tool("predict_my_opinion", {"title": title}, user_id, engine)

        @tool
        def my_taste_profile() -> str:
            """The current user's favourite genres, favourite movies and rating habits."""
            return _exec_tool("my_taste_profile", {}, user_id, engine)

        @tool
        def add_to_watchlist(title: str) -> str:
            """Add a movie to the current user's watchlist."""
            return _exec_tool("add_to_watchlist", {"title": title}, user_id, engine)

        @tool
        def rate_movie(title: str, rating: float) -> str:
            """Save the current user's rating (0.5 to 5.0 stars) for a movie."""
            return _exec_tool("rate_movie", {"title": title, "rating": rating}, user_id, engine)

        tools = [search_movies, recommend_for_me, similar_to, predict_my_opinion, my_taste_profile, add_to_watchlist, rate_movie]
        by_name = {t.name: t for t in tools}
        bound_llm = llm.bind_tools(tools)

        messages = [SystemMessage(AGENT_SYSTEM_PROMPT.format(username=user["username"], user_id=user_id))]
        for h in history[-10:]:
            messages.append(HumanMessage(h["content"]) if h["role"] == "user" else AIMessage(h["content"]))
        messages.append(HumanMessage(message))

        trace = []
        for _ in range(MAX_TOOL_ROUNDS):
            ai = bound_llm.invoke(messages)
            messages.append(ai)
            if not ai.tool_calls:
                return {"reply": ai.content, "tool_calls": trace}
            for call in ai.tool_calls:
                fn = by_name.get(call["name"])
                try:
                    result = fn.invoke(call["args"]) if fn else f"Unknown tool {call['name']}"
                except Exception as e:
                    result = f"Tool error: {e}"
                trace.append({"tool": call["name"], "args": call["args"], "result": str(result)[:1500]})
                messages.append(ToolMessage(str(result), tool_call_id=call["id"]))

        final = llm.invoke(messages + [HumanMessage("Summarise the answer for the user now.")])
        return {"reply": final.content, "tool_calls": trace}
    except Exception as e:
        return {"reply": f"⚠️ Error executing agent: {e}", "tool_calls": []}


# ------------------------------------------------------------------ chains
def _slim(recs: list) -> str:
    return json.dumps([{k: r[k] for k in ("title", "genres", "score", "reason")} for r in recs[:8]])


def explain_recommendations(profile: dict, recs: list) -> str:
    if setup_hint():
        return fallback_explanation(profile, recs)
    
    prompt = EXPLAIN_PROMPT.format(profile=json.dumps(profile), recommendations=_slim(recs))
    if GEMINI_API_KEY and (LLM_PROVIDER == "gemini" or LLM_PROVIDER != "ollama"):
        try:
            return _gemini_generate(prompt, temperature=0.3)
        except Exception:
            return fallback_explanation(profile, recs)

    # Ollama fallback
    try:
        from langchain_core.output_parsers import StrOutputParser
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_ollama import ChatOllama

        llm = ChatOllama(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL, temperature=0.5)
        chain = ChatPromptTemplate.from_template(EXPLAIN_PROMPT) | llm | StrOutputParser()
        return chain.invoke({"profile": json.dumps(profile), "recommendations": _slim(recs)}).strip()
    except Exception:
        return fallback_explanation(profile, recs)


def taste_report(username: str, profile: dict, recs: list) -> str:
    if setup_hint():
        return fallback_report(profile, recs)

    prompt = REPORT_PROMPT.format(username=username, profile=json.dumps(profile), recommendations=_slim(recs))
    if GEMINI_API_KEY and (LLM_PROVIDER == "gemini" or LLM_PROVIDER != "ollama"):
        try:
            return _gemini_generate(prompt, temperature=0.3)
        except Exception:
            return fallback_report(profile, recs)

    # Ollama fallback
    try:
        from langchain_core.output_parsers import StrOutputParser
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_ollama import ChatOllama

        llm = ChatOllama(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL, temperature=0.5)
        chain = ChatPromptTemplate.from_template(REPORT_PROMPT) | llm | StrOutputParser()
        return chain.invoke({"username": username, "profile": json.dumps(profile), "recommendations": _slim(recs)}).strip()
    except Exception:
        return fallback_report(profile, recs)


# ---------------------------------------------- template fallbacks (no LLM)
def fallback_explanation(profile: dict, recs: list) -> str:
    genres = ", ".join(g["genre"] for g in profile.get("top_genres", [])[:3]) or "a mix of genres"
    lines = [f"These picks match your love for {genres}."]
    lines += [f"- **{r['title']}** - {r['reason']}" for r in recs[:3]]
    return "\n".join(lines)


def fallback_report(profile: dict, recs: list) -> str:
    genres = [g["genre"] for g in profile.get("top_genres", [])]
    fav = ", ".join(m["title"] for m in profile.get("favourite_movies", [])[:3]) or "-"
    return (
        f"Taste Summary: You have rated {profile.get('num_ratings', 0)} movies with an average of "
        f"{profile.get('avg_rating')} stars. Your strongest genres are {', '.join(genres[:3]) or 'not known yet'}. "
        f"Favourites include {fav}.\n\n"
        f"Viewing Personality: Passionate Cinephile\nYou explore a wide range of film genres with a keen eye for quality.\n\n"
        f"Why These Recommendations: They are the titles our neural network predicts you are most likely to enjoy, "
        f"based on similarity to movies you rated highly.\n\n"
        f"Try Something New: Animation\nExpanding your horizons with acclaimed animated storytelling might pleasantly surprise you."
    )
