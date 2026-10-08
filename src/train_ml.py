"""AI-503: Machine Learning model development.

Trains and evaluates
  1. Content-based model       TF-IDF on genres + tags + title (cosine similarity)
  2. Collaborative filtering   Truncated SVD (matrix factorisation) on the user x movie rating matrix
  3. Like/Dislike classifiers  Logistic Regression and Random Forest

Saves models to models/, figures to reports/figures/, metrics to reports/metrics.json.
Run:  python -m src.train_ml
"""
import joblib
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.sparse import csr_matrix
from sklearn.decomposition import TruncatedSVD
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    ConfusionMatrixDisplay, RocCurveDisplay, accuracy_score, classification_report,
    confusion_matrix, f1_score, mean_absolute_error, precision_score, recall_score,
    roc_auc_score, root_mean_squared_error,
)
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from src.config import (
    FIGURES_DIR, GENRES, LOGREG_PATH, MODELS_DIR, RANDOM_STATE, RF_PATH, SVD_PATH, TFIDF_PATH,
)
from src.dataset import classification_data, ratings_matrix_summary, save_metrics, train_test_frames
from src.features import FEATURE_COLUMNS, movie_text

SVD_COMPONENTS = 50


def savefig(name: str):
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / name, dpi=120)
    plt.close()


# ------------------------------------------------------------------ EDA plots
def eda(ratings: pd.DataFrame, movies: pd.DataFrame):
    plt.figure(figsize=(7, 4))
    sns.countplot(x="rating", data=ratings, color="#4C72B0")
    plt.title("Rating distribution")
    savefig("eda_rating_distribution.png")

    counts = {g: movies["genres"].str.contains(g, regex=False).sum() for g in GENRES[:-1]}
    plt.figure(figsize=(8, 5))
    pd.Series(counts).sort_values().plot.barh(color="#55A868")
    plt.title("Movies per genre")
    plt.xlabel("Number of movies")
    savefig("eda_genre_counts.png")

    plt.figure(figsize=(7, 4))
    ratings.groupby("user_id").size().plot.hist(bins=50, log=True, color="#C44E52")
    plt.title("Ratings per user (log scale)")
    plt.xlabel("Number of ratings")
    savefig("eda_ratings_per_user.png")

    by_year = movies.dropna(subset=["year"]).groupby("year").size()
    plt.figure(figsize=(8, 4))
    by_year[by_year.index >= 1920].plot(color="#8172B2")
    plt.title("Movies released per year")
    savefig("eda_movies_per_year.png")


# ---------------------------------------------------------- 1. Content model
def train_content(movies: pd.DataFrame) -> dict:
    vectorizer = TfidfVectorizer(stop_words="english", min_df=2, max_features=5000, ngram_range=(1, 2))
    matrix = vectorizer.fit_transform(movie_text(movies))
    joblib.dump(vectorizer, TFIDF_PATH)

    # Sanity check: neighbours of a well-known movie
    idx = movies.index[movies["title"].str.startswith("Toy Story (1995)")][0]
    sims = (matrix @ matrix[idx].T).toarray().ravel()
    top = movies.iloc[np.argsort(-sims)[1:6]]["title"].tolist()
    print("Content model - similar to Toy Story:", top)
    return {"vocabulary_size": len(vectorizer.vocabulary_), "example_similar_to_toy_story": top}


# ------------------------------------------------- 2. Collaborative filtering
def _svd_fit(ratings: pd.DataFrame, movie_ids: np.ndarray):
    user_ids = np.sort(ratings["user_id"].unique())
    u_index = {u: i for i, u in enumerate(user_ids)}
    m_index = {m: i for i, m in enumerate(movie_ids)}
    user_mean = ratings.groupby("user_id")["rating"].mean()
    centered = ratings["rating"] - ratings["user_id"].map(user_mean)
    mat = csr_matrix(
        (centered, (ratings["user_id"].map(u_index), ratings["movie_id"].map(m_index))),
        shape=(len(user_ids), len(movie_ids)),
    )
    svd = TruncatedSVD(n_components=SVD_COMPONENTS, random_state=RANDOM_STATE)
    user_f = svd.fit_transform(mat)          # users x k
    item_f = svd.components_.T               # movies x k
    return svd, u_index, m_index, user_mean, user_f, item_f


def train_collaborative(ratings, movies, train_df, test_df) -> dict:
    movie_ids = movies["movie_id"].to_numpy()

    # Evaluate on the held-out 20% of ratings
    _, u_index, m_index, user_mean, user_f, item_f = _svd_fit(train_df, movie_ids)
    known = test_df["user_id"].isin(u_index)
    t = test_df[known]
    ui = t["user_id"].map(u_index).to_numpy()
    mi = t["movie_id"].map(m_index).to_numpy()
    pred = np.clip(t["user_id"].map(user_mean).to_numpy() + np.sum(user_f[ui] * item_f[mi], axis=1), 0.5, 5.0)
    baseline = np.full(len(t), train_df["rating"].mean())
    metrics = {
        "svd_rmse": round(root_mean_squared_error(t["rating"], pred), 4),
        "svd_mae": round(mean_absolute_error(t["rating"], pred), 4),
        "baseline_global_mean_rmse": round(root_mean_squared_error(t["rating"], baseline), 4),
        "components": SVD_COMPONENTS,
    }
    print("Collaborative filtering:", metrics)

    plt.figure(figsize=(6, 4))
    plt.bar(["Global mean (baseline)", "SVD"], [metrics["baseline_global_mean_rmse"], metrics["svd_rmse"]],
            color=["#999999", "#4C72B0"])
    plt.ylabel("RMSE (lower is better)")
    plt.title("Rating prediction error on test set")
    savefig("cf_rmse_comparison.png")

    # Refit on all ratings and save normalised item factors for item-item similarity
    _, _, m_index, _, _, item_f = _svd_fit(ratings, movie_ids)
    norms = np.linalg.norm(item_f, axis=1, keepdims=True)
    item_f = np.divide(item_f, norms, out=np.zeros_like(item_f), where=norms > 0)
    joblib.dump({"movie_ids": movie_ids, "item_factors": item_f.astype(np.float32)}, SVD_PATH)
    return metrics


# ----------------------------------------------------- 3. Like classifiers
def evaluate_classifier(name, model, X_test, y_test) -> dict:
    proba = model.predict_proba(X_test)[:, 1]
    pred = (proba >= 0.5).astype(int)
    metrics = {
        "accuracy": round(accuracy_score(y_test, pred), 4),
        "precision": round(precision_score(y_test, pred), 4),
        "recall": round(recall_score(y_test, pred), 4),
        "f1": round(f1_score(y_test, pred), 4),
        "roc_auc": round(roc_auc_score(y_test, proba), 4),
        "confusion_matrix": confusion_matrix(y_test, pred).tolist(),
    }
    print(f"\n{name}\n" + classification_report(y_test, pred, target_names=["Dislike", "Like"]))

    ConfusionMatrixDisplay.from_predictions(y_test, pred, display_labels=["Dislike", "Like"], cmap="Blues")
    plt.title(f"Confusion matrix - {name}")
    savefig(f"cm_{name.lower().replace(' ', '_')}.png")
    return metrics


def train_classifiers() -> dict:
    X_train, y_train, X_test, y_test = classification_data()
    print(f"Classifier data: train={X_train.shape}, test={X_test.shape}, like-rate={y_train.mean():.3f}")

    logreg = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000))
    logreg.fit(X_train, y_train)
    joblib.dump(logreg, LOGREG_PATH)

    rf = RandomForestClassifier(
        n_estimators=200, max_depth=14, min_samples_leaf=5, n_jobs=-1, random_state=RANDOM_STATE
    )
    rf.fit(X_train, y_train)
    joblib.dump(rf, RF_PATH)

    results = {
        "logistic_regression": evaluate_classifier("Logistic Regression", logreg, X_test, y_test),
        "random_forest": evaluate_classifier("Random Forest", rf, X_test, y_test),
    }

    fig, ax = plt.subplots(figsize=(6, 5))
    RocCurveDisplay.from_estimator(logreg, X_test, y_test, name="Logistic Regression", ax=ax)
    RocCurveDisplay.from_estimator(rf, X_test, y_test, name="Random Forest", ax=ax)
    ax.plot([0, 1], [0, 1], "k--", lw=1)
    ax.set_title("ROC curve - ML classifiers")
    savefig("roc_ml_classifiers.png")

    imp = pd.Series(rf.feature_importances_, index=FEATURE_COLUMNS).sort_values().tail(15)
    plt.figure(figsize=(7, 5))
    imp.plot.barh(color="#4C72B0")
    plt.title("Random Forest - top 15 feature importances")
    savefig("rf_feature_importance.png")
    return results


def main():
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    ratings, movies, train_df, test_df = train_test_frames()
    summary = ratings_matrix_summary(ratings)
    print("Dataset:", summary)

    eda(ratings, movies)
    content = train_content(movies)
    collab = train_collaborative(ratings, movies, train_df, test_df)
    classifiers = train_classifiers()

    save_metrics("dataset", summary)
    save_metrics("content_model", content)
    save_metrics("collaborative_filtering", collab)
    save_metrics("ml_classifiers", classifiers)
    print("\nSaved models to", MODELS_DIR)


if __name__ == "__main__":
    main()
