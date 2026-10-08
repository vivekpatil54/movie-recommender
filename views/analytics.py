import pandas as pd
import plotly.express as px
import streamlit as st

from src import db, theme
from src.config import GENRES

theme.page_header("📊", "Analytics", "What 100,000+ ratings say about movies and viewers")
WARM = ["#6D28D9", "#A21CAF", "#E11D74", "#FF2E4D", "#FFB224"]


@st.cache_data(ttl=60)
def load():
    ratings = db.query_df("SELECT r.user_id, r.movie_id, r.rating, r.created_at, m.title, m.genres, m.year "
                          "FROM ratings r JOIN movies m ON m.movie_id = r.movie_id")
    ratings["created_at"] = pd.to_datetime(ratings["created_at"])
    return ratings


r = load()
if r.empty:
    theme.empty_state("📭", "No ratings yet.")
    st.stop()

theme.stat_cards([
    ("⭐", "Ratings", f"{len(r):,}", "#FFB224"),
    ("📈", "Average rating", f"{r['rating'].mean():.2f} ★", "#FF2E4D"),
    ("👥", "Active users", f"{r['user_id'].nunique():,}", "#22D3EE"),
    ("🎬", "Movies rated", f"{r['movie_id'].nunique():,}", "#8B5CF6"),
    ("👍", "Liked (≥ 4★)", f"{(r['rating'] >= 4).mean() * 100:.1f}%", "#34D399"),
])

c1, c2 = st.columns(2)
with c1:
    dist = r["rating"].value_counts().sort_index().reset_index()
    fig = px.bar(dist, x="rating", y="count", title="⭐ Rating distribution", color="rating",
                 color_continuous_scale=WARM)
    fig.update_coloraxes(showscale=False)
    fig.update_traces(marker_line_width=0, hovertemplate="%{x}★ · %{y:,} ratings<extra></extra>")
    st.plotly_chart(theme.style_fig(fig), use_container_width=True)
with c2:
    g = r.assign(genre=r["genres"].str.split("|")).explode("genre")
    g = g[g["genre"].isin(GENRES[:-1])].groupby("genre")["rating"].agg(["count", "mean"]).reset_index()
    g["label"] = g["genre"].map(lambda x: f"{theme.GENRE_STYLE.get(x, theme.DEFAULT_STYLE)[0]} {x}")
    fig = px.bar(g.sort_values("count"), x="count", y="label", orientation="h", color="mean",
                 color_continuous_scale=WARM, title="🎭 Ratings per genre (colour = avg rating)",
                 labels={"label": "", "mean": "Avg ★"})
    fig.update_traces(hovertemplate="%{y}<br>%{x:,} ratings<extra></extra>")
    st.plotly_chart(theme.style_fig(fig, 520), use_container_width=True)

c3, c4 = st.columns(2)
with c3:
    quarterly = r.set_index("created_at").resample("QE")["rating"].agg(["count", "mean"]).reset_index()
    fig = px.area(quarterly, x="created_at", y="count", title="📅 Ratings over time (per quarter)",
                  labels={"created_at": "", "count": "Ratings"})
    fig.update_traces(line_color="#FF2E4D", fillcolor="rgba(255,46,77,.18)", line_shape="spline")
    st.plotly_chart(theme.style_fig(fig), use_container_width=True)
with c4:
    decade = r.dropna(subset=["year"]).assign(decade=lambda d: (d["year"] // 10 * 10).astype(int))
    dec = decade.groupby("decade")["rating"].agg(["count", "mean"]).reset_index()
    dec = dec[dec["decade"] >= 1920]
    fig = px.line(dec, x="decade", y="mean", markers=True, title="🕰️ Average rating by release decade",
                  labels={"decade": "", "mean": "Avg ★"}, range_y=[3.0, 4.2])
    fig.update_traces(line_color="#8B5CF6", line_width=3, marker=dict(size=9, color="#FFB224"))
    st.plotly_chart(theme.style_fig(fig), use_container_width=True)

theme.section("Top rated movies (min. 50 ratings)", "🏆")
top = r.groupby(["movie_id", "title"])["rating"].agg(["mean", "count"]).reset_index()
top = top[top["count"] >= 50].sort_values("mean", ascending=False).head(15)
top.insert(0, "rank", ["🥇", "🥈", "🥉"] + [f"#{i}" for i in range(4, len(top) + 1)])
st.dataframe(top.drop(columns="movie_id").rename(columns={"mean": "avg_rating", "count": "ratings"}),
             hide_index=True, use_container_width=True,
             column_config={"rank": st.column_config.TextColumn("", width="small"),
                            "avg_rating": st.column_config.ProgressColumn("Avg rating", min_value=0, max_value=5,
                                                                          format="%.2f ★")})
