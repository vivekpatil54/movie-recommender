"""Visual design system: global CSS (theme, animations) + reusable HTML components.

Design: "Cinema Night" - midnight background, crimson -> magenta -> violet gradients,
glass cards, gentle entrance animations and hover glows. All motion is disabled for
users who ask their OS for reduced motion.
"""
import html
import re
from pathlib import Path

import streamlit as st

from src.config import BASE_DIR

ASSETS = BASE_DIR / "assets"
LOGO = str(ASSETS / "logo.svg")
ICON = str(ASSETS / "icon.svg")

# Genre -> (emoji, gradient start, gradient end) used for generated "posters" and chips
GENRE_STYLE = {
    "Action": ("💥", "#FF2E4D", "#FF8A00"),
    "Adventure": ("🧭", "#F59E0B", "#EF4444"),
    "Animation": ("🎨", "#22D3EE", "#8B5CF6"),
    "Children": ("🧸", "#34D399", "#22D3EE"),
    "Comedy": ("😂", "#FFB224", "#F472B6"),
    "Crime": ("🕵️", "#475569", "#991B1B"),
    "Documentary": ("🎥", "#64748B", "#0EA5E9"),
    "Drama": ("🎭", "#7C3AED", "#DB2777"),
    "Fantasy": ("🧙", "#8B5CF6", "#06B6D4"),
    "Film-Noir": ("🚬", "#1F2937", "#6B7280"),
    "Horror": ("👻", "#27272A", "#B91C1C"),
    "IMAX": ("🎞️", "#0EA5E9", "#6366F1"),
    "Musical": ("🎵", "#EC4899", "#F59E0B"),
    "Mystery": ("🔍", "#1E3A8A", "#7C3AED"),
    "Romance": ("💖", "#F43F5E", "#F472B6"),
    "Sci-Fi": ("🚀", "#06B6D4", "#3B82F6"),
    "Thriller": ("🔪", "#1E293B", "#DC2626"),
    "War": ("🎖️", "#4D7C0F", "#78716C"),
    "Western": ("🤠", "#B45309", "#92400E"),
}
DEFAULT_STYLE = ("🎬", "#FF2E4D", "#7C3AED")

CSS = r"""
<style>
/* ============================================================ tokens */
:root {
  --bg: #0A0A14; --surface: rgba(24, 24, 42, .72); --surface-solid: #161627;
  --border: rgba(255,255,255,.08); --border-strong: rgba(255,255,255,.14);
  --text: #ECECF4; --muted: #9A9AB8;
  --red: #FF2E4D; --magenta: #C026D3; --violet: #8B5CF6; --amber: #FFB224; --cyan: #22D3EE; --green: #34D399;
  --grad: linear-gradient(135deg, #FF2E4D 0%, #C026D3 55%, #7C3AED 100%);
  --grad-warm: linear-gradient(135deg, #FF2E4D, #FF8A00);
  --shadow: 0 10px 30px -12px rgba(0,0,0,.6);
  --glow: 0 0 0 1px rgba(255,46,77,.35), 0 12px 40px -10px rgba(255,46,77,.45);
}

/* ======================================================== animations */
@keyframes fadeUp   { from { opacity: 0; transform: translateY(16px); } to { opacity: 1; transform: none; } }
@keyframes fadeIn   { from { opacity: 0; } to { opacity: 1; } }
@keyframes popIn    { 0% { opacity: 0; transform: scale(.92); } 70% { transform: scale(1.02); } 100% { opacity: 1; transform: none; } }
@keyframes gradientShift { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
@keyframes float    { 0%, 100% { transform: translateY(0) rotate(var(--r, 0deg)); } 50% { transform: translateY(-14px) rotate(var(--r, 0deg)); } }
@keyframes pulse    { 0% { box-shadow: 0 0 0 0 currentColor; } 70% { box-shadow: 0 0 0 7px transparent; } 100% { box-shadow: 0 0 0 0 transparent; } }
@keyframes shimmer  { from { transform: translateX(-120%) skewX(-20deg); } to { transform: translateX(220%) skewX(-20deg); } }
@keyframes blob     { 0%, 100% { transform: translate(0, 0) scale(1); } 33% { transform: translate(40px, -30px) scale(1.08); } 66% { transform: translate(-30px, 25px) scale(.95); } }
@keyframes barGrow  { from { width: 0; } }
@property --p { syntax: '<number>'; inherits: false; initial-value: 0; }
@keyframes ring     { from { --p: 0; } }

/* ============================================================ base */
html, body, .stApp, .stMarkdown, p, label, input, textarea, select, button, li { font-family: 'Inter', system-ui, sans-serif; }
.stApp {
  background:
    radial-gradient(1200px 600px at 100% -10%, rgba(124,58,237,.16), transparent 60%),
    radial-gradient(900px 500px at -10% 10%, rgba(255,46,77,.12), transparent 55%),
    var(--bg);
  background-attachment: fixed;
}
[data-testid="stHeader"] { background: rgba(10,10,20,.55); backdrop-filter: blur(12px); }
[data-testid="stMainBlockContainer"] { animation: fadeIn .45s ease both; padding-top: 2.6rem; }
h1, h2, h3 { letter-spacing: -.02em; }
::selection { background: rgba(255,46,77,.35); }
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-thumb { background: #2A2A44; border-radius: 10px; border: 2px solid var(--bg); }
::-webkit-scrollbar-thumb:hover { background: #3A3A5C; }
a { transition: color .2s; }

/* ========================================================= sidebar */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #11112A 0%, #0C0C1A 100%);
  border-right: 1px solid var(--border);
}
[data-testid="stSidebarNav"] a, [data-testid="stSidebarNavLink"] {
  border-radius: 10px; margin: 1px 0; transition: background .2s, transform .2s;
}
[data-testid="stSidebarNavLink"]:hover { background: rgba(255,255,255,.05); transform: translateX(3px); }
[data-testid="stSidebarNavLink"][aria-current="page"] {
  background: linear-gradient(90deg, rgba(255,46,77,.22), rgba(139,92,246,.12));
  box-shadow: inset 3px 0 0 var(--red);
}
[data-testid="stNavSectionHeader"] { letter-spacing: .12em; font-size: .68rem; text-transform: uppercase; color: var(--muted); }

/* ========================================================= buttons */
.stButton > button, .stDownloadButton > button, [data-testid="stFormSubmitButton"] > button {
  font-weight: 600; transition: transform .18s ease, box-shadow .25s ease, background .25s ease, border-color .25s;
  position: relative; overflow: hidden;
}
.stButton > button:hover, .stDownloadButton > button:hover, [data-testid="stFormSubmitButton"] > button:hover {
  transform: translateY(-2px); border-color: rgba(255,46,77,.6);
}
.stButton > button:active, [data-testid="stFormSubmitButton"] > button:active { transform: translateY(0) scale(.98); }
[data-testid="stBaseButton-primary"], [data-testid="stBaseButton-primaryFormSubmit"] {
  background: var(--grad) !important; background-size: 200% 200% !important; border: none !important;
  animation: gradientShift 6s ease infinite; box-shadow: 0 8px 22px -8px rgba(255,46,77,.6);
}
[data-testid="stBaseButton-primary"]:hover, [data-testid="stBaseButton-primaryFormSubmit"]:hover {
  box-shadow: 0 12px 30px -8px rgba(192,38,211,.7);
}
[data-testid="stBaseButton-primary"]::after, [data-testid="stBaseButton-primaryFormSubmit"]::after {
  content: ""; position: absolute; top: 0; left: 0; width: 40%; height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,.28), transparent);
  transform: translateX(-120%) skewX(-20deg);
}
[data-testid="stBaseButton-primary"]:hover::after, [data-testid="stBaseButton-primaryFormSubmit"]:hover::after {
  animation: shimmer .8s ease;
}
[data-testid="stBaseButton-secondary"], [data-testid="stBaseButton-secondaryFormSubmit"] {
  background: rgba(255,255,255,.04) !important; backdrop-filter: blur(6px);
}

/* ================================================ cards / containers */
[data-testid="stForm"] {
  background: var(--surface); backdrop-filter: blur(14px);
  border: 1px solid var(--border) !important; box-shadow: var(--shadow);
  animation: fadeUp .5s ease both;
}
[data-testid="stMetric"] {
  background: var(--surface); border: 1px solid var(--border); border-radius: 16px;
  padding: 14px 16px; box-shadow: var(--shadow); animation: popIn .5s ease both;
  transition: transform .25s, box-shadow .25s, border-color .25s;
}
[data-testid="stMetric"]:hover { transform: translateY(-3px); border-color: rgba(255,46,77,.4); box-shadow: var(--glow); }
[data-testid="stMetricValue"] { font-family: 'Poppins', sans-serif; font-weight: 700; }
[data-testid="stExpander"] details { background: var(--surface); border-radius: 14px; border-color: var(--border); }
[data-testid="stDataFrame"], [data-testid="stTable"] { border-radius: 14px; overflow: hidden; border: 1px solid var(--border); animation: fadeUp .5s ease both; }
[data-testid="stImage"] img { border-radius: 14px; }
[data-testid="stAlert"] { border-radius: 14px; animation: fadeUp .4s ease both; backdrop-filter: blur(8px); }
[data-testid="stPlotlyChart"] { background: var(--surface); border: 1px solid var(--border); border-radius: 16px; padding: 6px; animation: fadeUp .55s ease both; }

/* ============================================================ tabs */
[data-testid="stTabs"] [role="tablist"] {
  gap: 6px; background: rgba(255,255,255,.03); padding: 6px; border-radius: 14px; border: 1px solid var(--border);
  flex-wrap: wrap;
}
[data-testid="stTabs"] [role="tablist"]::after { display: none !important; }
[data-testid="stTab"] { border-radius: 10px !important; padding: 8px 16px !important; transition: background .25s, color .25s, box-shadow .25s; }
[data-testid="stTab"]:hover { background: rgba(255,255,255,.06); }
[data-testid="stTab"][aria-selected="true"] { background: var(--grad); color: #fff !important; box-shadow: 0 6px 18px -8px rgba(255,46,77,.7); }
[data-testid="stTab"][aria-selected="true"] * { color: #fff !important; }
[data-testid="stTab"] > div:empty { display: none !important; }
[data-testid="stTabPanel"] { animation: fadeUp .35s ease both; }

/* ======================================================== inputs */
[data-baseweb="input"], [data-baseweb="select"] > div, [data-baseweb="textarea"] { transition: border-color .2s, box-shadow .2s; }
[data-baseweb="input"]:focus-within, [data-baseweb="select"] > div:focus-within, [data-baseweb="textarea"]:focus-within {
  box-shadow: 0 0 0 3px rgba(255,46,77,.22);
}

/* ============================================================ chat */
[data-testid="stChatMessage"] {
  background: var(--surface); border: 1px solid var(--border); border-radius: 18px; padding: 14px 16px;
  animation: fadeUp .35s ease both;
}
[data-testid="stChatInput"] { border-radius: 16px; box-shadow: 0 8px 30px -12px rgba(139,92,246,.55); }

/* =================================================== page header */
.pg-head { display: flex; align-items: center; gap: 16px; margin: 0 0 1.4rem; animation: fadeUp .45s ease both; }
.pg-icon {
  width: 56px; height: 56px; flex: none; border-radius: 16px; display: grid; place-items: center; font-size: 28px;
  background: var(--grad); background-size: 200% 200%; animation: gradientShift 8s ease infinite;
  box-shadow: 0 10px 28px -10px rgba(255,46,77,.75);
}
.pg-title { font-family: 'Poppins', sans-serif; font-size: 2rem; font-weight: 800; line-height: 1.1; margin: 0; letter-spacing: -.02em; }
.pg-sub { color: var(--muted); margin: 4px 0 0; font-size: .95rem; }
.grad-text {
  background: linear-gradient(90deg, #FF2E4D, #FF7A59, #C026D3, #8B5CF6, #FF2E4D); background-size: 300% 100%;
  -webkit-background-clip: text; background-clip: text; color: transparent; animation: gradientShift 8s linear infinite;
}

/* ============================================================ hero */
.hero {
  position: relative; overflow: hidden; border-radius: 24px; padding: 42px 40px 36px; margin-bottom: 1.6rem;
  background: linear-gradient(135deg, rgba(255,46,77,.16), rgba(124,58,237,.18)), rgba(20,20,36,.75);
  border: 1px solid var(--border-strong); box-shadow: var(--shadow); animation: fadeUp .6s ease both;
}
.hero::before {
  content: ""; position: absolute; inset: 0;
  background-image: repeating-linear-gradient(90deg, rgba(255,255,255,.05) 0 18px, transparent 18px 36px);
  height: 10px; opacity: .8;
}
.hero::after {
  content: ""; position: absolute; left: 0; right: 0; bottom: 0; height: 10px;
  background-image: repeating-linear-gradient(90deg, rgba(255,255,255,.05) 0 18px, transparent 18px 36px);
}
.hero-glow { position: absolute; width: 420px; height: 420px; right: -120px; top: -160px; border-radius: 50%;
  background: radial-gradient(circle, rgba(192,38,211,.45), transparent 65%); filter: blur(10px); animation: blob 14s ease-in-out infinite; }
.hero-badge { display: inline-flex; align-items: center; gap: 8px; padding: 6px 12px; border-radius: 999px; font-size: .78rem;
  background: rgba(255,255,255,.06); border: 1px solid var(--border-strong); color: #D6D6E8; position: relative; }
.hero-title { font-family: 'Poppins', sans-serif; font-size: clamp(1.9rem, 3.6vw, 3.1rem); font-weight: 800; line-height: 1.08;
  margin: 16px 0 10px; letter-spacing: -.03em; position: relative; max-width: 780px; }
.hero-sub { color: #B9B9D0; font-size: 1.05rem; max-width: 640px; margin: 0 0 20px; position: relative; }
.hero-pills { display: flex; flex-wrap: wrap; gap: 8px; position: relative; }
.hero-pills span { padding: 7px 14px; border-radius: 999px; font-size: .82rem; font-weight: 600;
  background: rgba(10,10,20,.5); border: 1px solid var(--border-strong); animation: popIn .5s ease both; }
.hero-pills span:nth-child(2) { animation-delay: .08s; } .hero-pills span:nth-child(3) { animation-delay: .16s; }
.hero-pills span:nth-child(4) { animation-delay: .24s; }
.floaty { position: absolute; font-size: 42px; animation: float 6s ease-in-out infinite; filter: drop-shadow(0 8px 16px rgba(0,0,0,.5)); opacity: .9; }

/* ======================================================= stat cards */
.stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 14px; margin: 0 0 1.6rem; }
.stat { background: var(--surface); border: 1px solid var(--border); border-radius: 18px; padding: 16px; position: relative; overflow: hidden;
  animation: fadeUp .5s ease both; transition: transform .25s, box-shadow .25s, border-color .25s; }
.stat:hover { transform: translateY(-4px); border-color: rgba(255,255,255,.18); box-shadow: 0 16px 34px -14px var(--c, #FF2E4D); }
.stat::after { content: ""; position: absolute; width: 90px; height: 90px; right: -30px; top: -30px; border-radius: 50%;
  background: radial-gradient(circle, var(--c, #FF2E4D), transparent 70%); opacity: .25; }
.stat-icon { width: 38px; height: 38px; border-radius: 12px; display: grid; place-items: center; font-size: 19px;
  background: color-mix(in srgb, var(--c, #FF2E4D) 22%, transparent); margin-bottom: 10px; }
.stat-value { font-family: 'Poppins', sans-serif; font-size: 1.55rem; font-weight: 700; line-height: 1.1; }
.stat-label { color: var(--muted); font-size: .8rem; margin-top: 2px; }

/* ===================================================== feature cards */
.features { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; margin-bottom: 1.6rem; }
.feature { position: relative; border-radius: 20px; padding: 20px; background: var(--surface); border: 1px solid var(--border);
  animation: fadeUp .55s ease both; transition: transform .3s, box-shadow .3s; overflow: hidden; }
.feature::before { content: ""; position: absolute; inset: 0; border-radius: 20px; padding: 1px; background: var(--g);
  -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0); -webkit-mask-composite: xor; mask-composite: exclude;
  opacity: 0; transition: opacity .3s; }
.feature:hover { transform: translateY(-5px); box-shadow: var(--shadow); }
.feature:hover::before { opacity: 1; }
.feature-head { display: flex; align-items: center; gap: 10px; margin-bottom: 10px; }
.feature-icon { width: 42px; height: 42px; border-radius: 13px; display: grid; place-items: center; font-size: 21px; background: var(--g); }
.feature-code { font-size: .7rem; font-weight: 700; letter-spacing: .1em; color: var(--muted); }
.feature-title { font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 1.02rem; }
.feature ul { margin: 0; padding-left: 0; list-style: none; }
.feature li { padding: 5px 0 5px 22px; position: relative; color: #C9C9DC; font-size: .88rem; }
.feature li::before { content: "✓"; position: absolute; left: 0; color: var(--green); font-weight: 700; }

/* ======================================================= movie cards */
.mv-card { background: var(--surface); border: 1px solid var(--border); border-radius: 18px; overflow: hidden; margin-bottom: 8px;
  animation: fadeUp .5s ease both; transition: transform .3s cubic-bezier(.2,.8,.2,1), box-shadow .3s, border-color .3s; }
.mv-card:hover { transform: translateY(-6px); border-color: rgba(255,46,77,.45); box-shadow: var(--glow); }
.mv-poster { position: relative; height: 128px; background: linear-gradient(135deg, var(--c1), var(--c2)); overflow: hidden; }
.mv-poster::before { content: ""; position: absolute; inset: 0;
  background: radial-gradient(circle at 20% 120%, rgba(0,0,0,.45), transparent 60%), linear-gradient(180deg, transparent 40%, rgba(10,10,20,.55)); }
.mv-poster::after { content: ""; position: absolute; left: 0; right: 0; top: 0; height: 8px;
  background-image: repeating-linear-gradient(90deg, rgba(0,0,0,.35) 0 10px, transparent 10px 20px); }
.mv-emoji { position: absolute; right: 14px; bottom: 6px; font-size: 54px; transition: transform .4s cubic-bezier(.2,.8,.2,1);
  filter: drop-shadow(0 6px 14px rgba(0,0,0,.45)); }
.mv-card:hover .mv-emoji { transform: scale(1.15) rotate(-8deg); }
.mv-rank { position: absolute; left: 12px; top: 16px; font-family: 'Poppins', sans-serif; font-weight: 800; font-size: .8rem;
  padding: 3px 9px; border-radius: 999px; background: rgba(10,10,20,.55); backdrop-filter: blur(6px); }
.mv-year { position: absolute; left: 12px; bottom: 10px; font-size: .75rem; font-weight: 600; padding: 2px 8px; border-radius: 8px;
  background: rgba(10,10,20,.55); backdrop-filter: blur(6px); }
.mv-ring { position: absolute; right: 12px; top: 16px; width: 46px; height: 46px; border-radius: 50%; display: grid; place-items: center;
  background: conic-gradient(var(--rc, #34D399) calc(var(--p) * 1%), rgba(255,255,255,.15) 0); animation: ring 1.3s cubic-bezier(.2,.8,.2,1) both; }
.mv-ring span { width: 36px; height: 36px; border-radius: 50%; background: rgba(10,10,20,.82); display: grid; place-items: center;
  font-size: .68rem; font-weight: 700; }
.mv-body { padding: 12px 14px 14px; }
.mv-title { font-family: 'Poppins', sans-serif; font-weight: 700; font-size: .98rem; line-height: 1.25; margin-bottom: 8px;
  display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; min-height: 2.5em; }
.chips { display: flex; flex-wrap: wrap; gap: 5px; margin-bottom: 8px; }
.chip { font-size: .68rem; font-weight: 600; padding: 3px 8px; border-radius: 999px;
  background: color-mix(in srgb, var(--cc, #FF2E4D) 20%, transparent); border: 1px solid color-mix(in srgb, var(--cc, #FF2E4D) 40%, transparent); }
.mv-reason { font-size: .78rem; color: var(--muted); line-height: 1.35; display: -webkit-box; -webkit-line-clamp: 2;
  -webkit-box-orient: vertical; overflow: hidden; min-height: 2.7em; }

/* ======================================================= misc parts */
.pill { display: inline-flex; align-items: center; gap: 7px; padding: 5px 11px; border-radius: 999px; font-size: .76rem; font-weight: 600;
  background: rgba(255,255,255,.05); border: 1px solid var(--border); margin: 2px 4px 2px 0; }
.dot { width: 8px; height: 8px; border-radius: 50%; background: currentColor; animation: pulse 2s infinite; }
.pill.ok { color: var(--green); } .pill.warn { color: var(--amber); } .pill.off { color: #F87171; }
.pill b { color: var(--text); font-weight: 600; }
.section { display: flex; align-items: center; gap: 10px; margin: 1.6rem 0 .8rem; animation: fadeUp .45s ease both; }
.section h3 { font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 1.25rem; margin: 0; }
.section .line { flex: 1; height: 1px; background: linear-gradient(90deg, var(--border-strong), transparent); }
.empty { text-align: center; padding: 36px 20px; border: 1px dashed var(--border-strong); border-radius: 18px; color: var(--muted);
  animation: fadeUp .45s ease both; }
.empty .big { font-size: 46px; display: block; margin-bottom: 6px; animation: float 5s ease-in-out infinite; }
.profile { display: flex; align-items: center; gap: 12px; padding: 12px; border-radius: 16px; margin-bottom: 10px;
  background: linear-gradient(135deg, rgba(255,46,77,.14), rgba(139,92,246,.12)); border: 1px solid var(--border-strong); animation: fadeUp .4s ease both; }
.avatar { width: 44px; height: 44px; flex: none; border-radius: 14px; display: grid; place-items: center; font-family: 'Poppins', sans-serif;
  font-weight: 800; color: #fff; background: var(--grad); box-shadow: 0 6px 16px -6px rgba(255,46,77,.7); }
.profile .name { font-weight: 700; line-height: 1.2; } .profile .handle { color: var(--muted); font-size: .78rem; }
.role { display: inline-block; font-size: .64rem; font-weight: 800; letter-spacing: .08em; padding: 2px 7px; border-radius: 6px; margin-left: 4px;
  background: rgba(255,178,36,.18); color: var(--amber); vertical-align: middle; }
.role.user { background: rgba(34,211,238,.15); color: var(--cyan); }
.callout { border-radius: 18px; padding: 18px 20px; background: linear-gradient(135deg, rgba(139,92,246,.18), rgba(34,211,238,.08));
  border: 1px solid rgba(139,92,246,.35); animation: fadeUp .45s ease both; }
.bar-row { display: grid; grid-template-columns: 120px 1fr 48px; align-items: center; gap: 10px; margin: 8px 0; font-size: .85rem; }
.bar-track { height: 9px; border-radius: 9px; background: rgba(255,255,255,.07); overflow: hidden; }
.bar-fill { height: 100%; border-radius: 9px; background: var(--grad); animation: barGrow 1.1s cubic-bezier(.2,.8,.2,1) both; }

/* ================================================== auth screens */
.auth-bg { position: fixed; inset: 0; z-index: 0; pointer-events: none; overflow: hidden; }
.auth-bg i { position: absolute; border-radius: 50%; filter: blur(70px); opacity: .55; animation: blob 18s ease-in-out infinite; }
.auth-bg i:nth-child(1) { width: 460px; height: 460px; background: #FF2E4D; left: -120px; top: -100px; }
.auth-bg i:nth-child(2) { width: 520px; height: 520px; background: #7C3AED; right: -160px; bottom: -160px; animation-delay: -6s; }
.auth-bg i:nth-child(3) { width: 300px; height: 300px; background: #22D3EE; left: 45%; top: 55%; opacity: .25; animation-delay: -11s; }
.auth-brand { text-align: center; margin: 10px 0 18px; animation: fadeUp .5s ease both; position: relative; }
.auth-brand img { width: 230px; max-width: 80%; }
.auth-title { font-family: 'Poppins', sans-serif; font-weight: 800; font-size: 1.7rem; margin: 10px 0 2px; }
.auth-sub { color: var(--muted); font-size: .92rem; }
.auth-foot { text-align: center; color: var(--muted); font-size: .75rem; margin-top: 18px; }
.steps { display: flex; gap: 8px; justify-content: center; margin: 4px 0 14px; }
.steps span { font-size: .75rem; font-weight: 600; padding: 4px 12px; border-radius: 999px; border: 1px solid var(--border-strong); color: var(--muted); }
.steps span.on { background: var(--grad); color: #fff; border-color: transparent; }

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation: none !important; transition: none !important; }
}
@media (max-width: 640px) {
  .hero { padding: 28px 20px; } .floaty { display: none; } .pg-title { font-size: 1.5rem; }
}
</style>
"""


def inject():
    st.markdown(CSS, unsafe_allow_html=True)


def esc(text) -> str:
    return html.escape(str(text if text is not None else ""))


def _html(markup: str):
    """Render HTML. Lines are stripped so Markdown never treats indentation as a code block."""
    st.markdown(" ".join(line.strip() for line in markup.splitlines() if line.strip()), unsafe_allow_html=True)


# ----------------------------------------------------------- page parts
def page_header(icon: str, title: str, subtitle: str = ""):
    _html(f"""<div class="pg-head"><div class="pg-icon">{icon}</div><div>
          <div class="pg-title">{esc(title)}</div>{f'<p class="pg-sub">{subtitle}</p>' if subtitle else ''}
          </div></div>""")


def section(title: str, icon: str = ""):
    _html(f'<div class="section"><h3>{icon} {esc(title)}</h3><div class="line"></div></div>')


def empty_state(icon: str, text: str):
    _html(f'<div class="empty"><span class="big">{icon}</span>{text}</div>')


def stat_cards(items: list):
    """items: [(icon, label, value, color), ...]"""
    cards = "".join(
        f'<div class="stat" style="--c:{c};animation-delay:{i * 70}ms"><div class="stat-icon">{icon}</div>'
        f'<div class="stat-value">{esc(value)}</div><div class="stat-label">{esc(label)}</div></div>'
        for i, (icon, label, value, c) in enumerate(items)
    )
    _html(f'<div class="stats">{cards}</div>')


def pill(state: str, label: str, value: str) -> str:
    return f'<span class="pill {state}"><i class="dot"></i>{esc(label)} <b>{esc(value)}</b></span>'


def bars(rows: list):
    """rows: [(label, value_0_to_1, text), ...] - animated horizontal bars."""
    _html("".join(
        f'<div class="bar-row"><span>{esc(label)}</span><div class="bar-track">'
        f'<div class="bar-fill" style="width:{max(2, min(100, v * 100)):.0f}%;animation-delay:{i * 90}ms"></div>'
        f'</div><b>{esc(text)}</b></div>'
        for i, (label, v, text) in enumerate(rows)
    ))


def auth_background():
    _html('<div class="auth-bg"><i></i><i></i><i></i></div>')


def auth_brand(title: str, subtitle: str):
    svg = Path(LOGO).read_text(encoding="utf-8")
    import base64
    src = "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()
    _html(f'<div class="auth-brand"><img src="{src}" alt="CineMind logo"/>'
          f'<div class="auth-title">{esc(title)}</div><div class="auth-sub">{esc(subtitle)}</div></div>')


def initials(name: str) -> str:
    parts = [p for p in re.split(r"[\s_.]+", name or "") if p]
    return (parts[0][0] + (parts[1][0] if len(parts) > 1 else "")).upper() if parts else "?"


# ------------------------------------------------------------ movie cards
YEAR_SUFFIX = re.compile(r"\s*\((\d{4})\)\s*$")


def split_title(title: str):
    m = YEAR_SUFFIX.search(title)
    return (title[: m.start()], m.group(1)) if m else (title, "")


def genre_style(genres: str):
    first = (genres or "").split("|")[0]
    return GENRE_STYLE.get(first, DEFAULT_STYLE)


def ring_color(pct: float) -> str:
    return "#34D399" if pct >= 75 else "#FFB224" if pct >= 50 else "#FF2E4D"


def movie_card_html(it: dict, rank: int, score_label: str = "match", delay_ms: int = 0) -> str:
    title, year = split_title(it["title"])
    year = year or (str(it["year"]) if it.get("year") else "")
    emoji, c1, c2 = genre_style(it["genres"])
    pct = max(0.0, min(100.0, float(it.get("score", 0)) * 100))
    chips = "".join(
        f'<span class="chip" style="--cc:{GENRE_STYLE.get(g, DEFAULT_STYLE)[1]}">{esc(g)}</span>'
        for g in it["genres"].split("|")[:3] if g != "(no genres listed)"
    )
    reason = it.get("reason", "")
    return (
        f'<div class="mv-card" style="animation-delay:{delay_ms}ms">'
        f'<div class="mv-poster" style="--c1:{c1};--c2:{c2}">'
        f'<span class="mv-rank">#{rank}</span><span class="mv-emoji">{emoji}</span>'
        f'<div class="mv-ring" style="--p:{pct:.0f};--rc:{ring_color(pct)}" title="{pct:.0f}% {esc(score_label)}"><span>{pct:.0f}%</span></div>'
        + (f'<span class="mv-year">{year}</span>' if year else "")
        + f'</div><div class="mv-body"><div class="mv-title" title="{esc(it["title"])}">{esc(title)}</div>'
        f'<div class="chips">{chips}</div><div class="mv-reason">✨ {esc(reason)}</div></div></div>'
    )


# ---------------------------------------------------------------- plotly
def style_fig(fig, height: int = 360):
    fig.update_layout(
        height=height, margin=dict(l=10, r=10, t=50, b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="#C9C9DC"),
        title=dict(font=dict(family="Poppins, sans-serif", size=16, color="#ECECF4")),
        hoverlabel=dict(bgcolor="#1D1D33", bordercolor="#3A3A5C", font=dict(family="Inter")),
        transition=dict(duration=600, easing="cubic-in-out"),
    )
    fig.update_xaxes(gridcolor="rgba(255,255,255,.06)", zeroline=False)
    fig.update_yaxes(gridcolor="rgba(255,255,255,.06)", zeroline=False)
    return fig
