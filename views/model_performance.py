import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src import theme
from src.config import FIGURES_DIR, REPORTS_DIR
from src.dataset import load_metrics

theme.page_header("🧠", "Model Performance", "How well each model predicts whether you'll like a movie (20% test set)")
m = load_metrics()
if not m:
    theme.empty_state("🧪", "No metrics yet. Train the models first with <code>python -m src.train_all</code>")
    st.stop()


def fig(name, caption=None):
    path = FIGURES_DIR / name
    if path.exists():
        with st.container(border=True):
            st.image(str(path), caption=caption, use_container_width=True)


if "dataset" in m:
    d = m["dataset"]
    theme.stat_cards([
        ("👥", "Users", d["users"], "#22D3EE"),
        ("🎬", "Movies rated", f"{d['movies_rated']:,}", "#FF2E4D"),
        ("⭐", "Ratings", f"{d['ratings']:,}", "#FFB224"),
        ("🕳️", "Matrix sparsity", f"{d['sparsity_pct']}%", "#8B5CF6"),
        ("👍", "Liked (≥4★)", f"{d['liked_pct']}%", "#34D399"),
    ])

MODELS = {
    "ANN (Keras)": (m.get("ann"), "🧠", "#8B5CF6"),
    "Random Forest": (m.get("ml_classifiers", {}).get("random_forest"), "🌲", "#34D399"),
    "Logistic Regression": (m.get("ml_classifiers", {}).get("logistic_regression"), "📈", "#22D3EE"),
}
MODELS = {k: v for k, v in MODELS.items() if v[0]}
KEYS = ["accuracy", "precision", "recall", "f1", "roc_auc"]
best = max(MODELS, key=lambda k: MODELS[k][0]["roc_auc"])

theme.section("Leaderboard", "🏆")
cols = st.columns(len(MODELS))
for col, (name, (met, icon, color)) in zip(cols, sorted(MODELS.items(), key=lambda kv: -kv[1][0]["roc_auc"])):
    with col:
        crown = ' <span class="role">BEST</span>' if name == best else ""
        theme._html(f'<div class="stat" style="--c:{color}"><div class="stat-icon">{icon}</div>'
                    f'<div class="stat-value" style="font-size:1.1rem">{name}{crown}</div>'
                    f'<div class="stat-label">ROC-AUC <b style="color:var(--text)">{met["roc_auc"]:.3f}</b> · '
                    f'Accuracy <b style="color:var(--text)">{met["accuracy"] * 100:.1f}%</b></div></div>')
        theme.bars([(k.replace("_", " ").upper().replace("ROC AUC", "ROC-AUC"), met[k], f"{met[k]:.2f}") for k in KEYS])

left, right = st.columns([1.15, 1])
with left:
    figure = go.Figure()
    for name, (met, icon, color) in MODELS.items():
        figure.add_bar(name=f"{icon} {name}", x=[k.upper().replace("_", "-") for k in KEYS], y=[met[k] for k in KEYS],
                       marker_color=color, text=[f"{met[k]:.2f}" for k in KEYS], textposition="outside")
    figure.update_layout(title="📊 Metric comparison", barmode="group", yaxis_range=[0.6, 0.85],
                         legend=dict(orientation="h", y=-0.15))
    st.plotly_chart(theme.style_fig(figure, 400), use_container_width=True)
with right:
    radar = go.Figure()
    for name, (met, icon, color) in MODELS.items():
        radar.add_scatterpolar(r=[met[k] for k in KEYS] + [met[KEYS[0]]],
                               theta=[k.upper().replace("_", "-") for k in KEYS] + [KEYS[0].upper()],
                               name=f"{icon} {name}", line_color=color, fill="toself", opacity=.55)
    radar.update_layout(title="🕸️ Model radar", polar=dict(bgcolor="rgba(0,0,0,0)",
                        radialaxis=dict(range=[0.65, 0.82], gridcolor="rgba(255,255,255,.1)"),
                        angularaxis=dict(gridcolor="rgba(255,255,255,.1)")),
                        legend=dict(orientation="h", y=-0.15))
    st.plotly_chart(theme.style_fig(radar, 400), use_container_width=True)

with st.expander("Raw metrics table", icon=":material/table:"):
    table = pd.DataFrame({k: v[0] for k, v in MODELS.items()}).T[KEYS].astype(float)
    st.dataframe(table.style.format("{:.4f}").highlight_max(axis=0, color="rgba(255,46,77,.3)"), use_container_width=True)

tab_ann, tab_ml, tab_cf, tab_eda = st.tabs([":material/neurology: ANN (AI-505)", ":material/forest: ML classifiers (AI-503)",
                                            ":material/hub: Collaborative & Content", ":material/query_stats: Dataset EDA"])
with tab_ann:
    if "ann" in m:
        a = m["ann"]
        theme.stat_cards([
            ("🔢", "Parameters", f"{a['parameters']:,}", "#8B5CF6"),
            ("🔁", "Epochs (early stop)", a["epochs_trained"], "#22D3EE"),
            ("📉", "Final val loss", a["final_val_loss"], "#FF2E4D"),
            ("🎯", "Recall", f"{a['recall'] * 100:.1f}%", "#34D399"),
        ])
    fig("ann_training_curves.png", "Training vs validation loss / accuracy / AUC - curves stay together, so no overfitting")
    c1, c2 = st.columns(2)
    with c1:
        fig("cm_ann.png")
    with c2:
        fig("roc_ann.png")
    arch = REPORTS_DIR / "ann_architecture.txt"
    if arch.exists():
        with st.expander("Network architecture", icon=":material/account_tree:"):
            st.code(arch.read_text(encoding="utf-8"))

with tab_ml:
    c1, c2 = st.columns(2)
    with c1:
        fig("cm_logistic_regression.png")
        fig("roc_ml_classifiers.png")
    with c2:
        fig("cm_random_forest.png")
        fig("rf_feature_importance.png")

with tab_cf:
    if "collaborative_filtering" in m:
        cf = m["collaborative_filtering"]
        improvement = (1 - cf["svd_rmse"] / cf["baseline_global_mean_rmse"]) * 100
        theme.stat_cards([
            ("📉", "SVD RMSE", cf["svd_rmse"], "#34D399"),
            ("📏", "Baseline RMSE", cf["baseline_global_mean_rmse"], "#FF2E4D"),
            ("🚀", "Error reduced by", f"{improvement:.1f}%", "#FFB224"),
            ("🧩", "Latent factors", cf["components"], "#8B5CF6"),
        ])
    fig("cf_rmse_comparison.png")
    if "content_model" in m:
        st.markdown("**:material/movie: Content model sanity check:** movies most similar to *Toy Story (1995)*")
        st.pills("similar", m["content_model"]["example_similar_to_toy_story"], label_visibility="collapsed",
                 disabled=True)

with tab_eda:
    c1, c2 = st.columns(2)
    with c1:
        fig("eda_rating_distribution.png")
        fig("eda_ratings_per_user.png")
    with c2:
        fig("eda_genre_counts.png")
        fig("eda_movies_per_year.png")
