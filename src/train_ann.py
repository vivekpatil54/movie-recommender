"""AI-505: Artificial Neural Network (deep learning) with TensorFlow / Keras.

A feed-forward ANN that predicts whether a user will LIKE a movie (rating >= 4),
trained on the same features and the same train/test split as the ML classifiers
so the results are directly comparable.

Run:  python -m src.train_ann
"""
import os

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

import joblib
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from sklearn.metrics import (
    ConfusionMatrixDisplay, RocCurveDisplay, accuracy_score, classification_report,
    confusion_matrix, f1_score, precision_score, recall_score, roc_auc_score,
)
from sklearn.preprocessing import StandardScaler
from tensorflow import keras
from tensorflow.keras import layers

from src.config import ANN_PATH, FIGURES_DIR, MODELS_DIR, RANDOM_STATE, REPORTS_DIR, SCALER_PATH
from src.dataset import classification_data, load_metrics, save_metrics
from src.train_ml import savefig

EPOCHS = 60
BATCH_SIZE = 256


def build_model(n_features: int) -> keras.Model:
    model = keras.Sequential([
        layers.Input(shape=(n_features,), name="features"),
        layers.Dense(128, activation="relu", name="hidden_1"),
        layers.BatchNormalization(name="batch_norm_1"),
        layers.Dropout(0.3, name="dropout_1"),
        layers.Dense(64, activation="relu", name="hidden_2"),
        layers.BatchNormalization(name="batch_norm_2"),
        layers.Dropout(0.3, name="dropout_2"),
        layers.Dense(32, activation="relu", name="hidden_3"),
        layers.Dense(1, activation="sigmoid", name="like_probability"),
    ], name="movie_like_ann")
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=1e-3),
        loss="binary_crossentropy",
        metrics=["accuracy", keras.metrics.AUC(name="auc")],
    )
    return model


def plot_history(history):
    h = history.history
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    for ax, key, title in zip(axes, ["loss", "accuracy", "auc"], ["Loss", "Accuracy", "AUC"]):
        ax.plot(h[key], label="train")
        ax.plot(h[f"val_{key}"], label="validation")
        ax.set_title(f"ANN {title} per epoch")
        ax.set_xlabel("Epoch")
        ax.legend()
    savefig("ann_training_curves.png")


def plot_model_comparison():
    metrics = load_metrics()
    models = {
        "Logistic Regression": metrics.get("ml_classifiers", {}).get("logistic_regression"),
        "Random Forest": metrics.get("ml_classifiers", {}).get("random_forest"),
        "ANN (Keras)": metrics.get("ann"),
    }
    models = {k: v for k, v in models.items() if v}
    keys = ["accuracy", "precision", "recall", "f1", "roc_auc"]
    x = np.arange(len(keys))
    width = 0.8 / len(models)
    plt.figure(figsize=(9, 4.5))
    for i, (name, m) in enumerate(models.items()):
        bars = plt.bar(x + i * width, [m[k] for k in keys], width, label=name)
        plt.bar_label(bars, fmt="%.2f", fontsize=7)
    plt.xticks(x + width * (len(models) - 1) / 2, [k.upper().replace("_", " ") for k in keys])
    plt.ylim(0, 1.12)
    plt.title("Model comparison on test set")
    plt.legend(loc="upper center", ncol=len(models), frameon=False)
    savefig("model_comparison.png")


def main():
    tf.keras.utils.set_random_seed(RANDOM_STATE)
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    X_train, y_train, X_test, y_test = classification_data()
    scaler = StandardScaler().fit(X_train)
    joblib.dump(scaler, SCALER_PATH)
    Xtr, Xte = scaler.transform(X_train), scaler.transform(X_test)

    model = build_model(Xtr.shape[1])
    lines = []
    model.summary(print_fn=lambda s, **_: lines.append(s))
    (REPORTS_DIR / "ann_architecture.txt").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))

    history = model.fit(
        Xtr, y_train,
        validation_split=0.1,
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        callbacks=[
            keras.callbacks.EarlyStopping(monitor="val_auc", mode="max", patience=6, restore_best_weights=True),
            keras.callbacks.ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=3),
        ],
        verbose=2,
    )
    model.save(ANN_PATH)
    plot_history(history)

    proba = model.predict(Xte, verbose=0).ravel()
    pred = (proba >= 0.5).astype(int)
    metrics = {
        "accuracy": round(accuracy_score(y_test, pred), 4),
        "precision": round(precision_score(y_test, pred), 4),
        "recall": round(recall_score(y_test, pred), 4),
        "f1": round(f1_score(y_test, pred), 4),
        "roc_auc": round(roc_auc_score(y_test, proba), 4),
        "confusion_matrix": confusion_matrix(y_test, pred).tolist(),
        "epochs_trained": len(history.history["loss"]),
        "final_train_loss": round(float(history.history["loss"][-1]), 4),
        "final_val_loss": round(float(history.history["val_loss"][-1]), 4),
        "parameters": int(model.count_params()),
    }
    print("\nANN\n" + classification_report(y_test, pred, target_names=["Dislike", "Like"]))

    ConfusionMatrixDisplay.from_predictions(y_test, pred, display_labels=["Dislike", "Like"], cmap="Purples")
    plt.title("Confusion matrix - ANN")
    savefig("cm_ann.png")

    fig, ax = plt.subplots(figsize=(6, 5))
    RocCurveDisplay.from_predictions(y_test, proba, name="ANN", ax=ax)
    ax.plot([0, 1], [0, 1], "k--", lw=1)
    ax.set_title("ROC curve - ANN")
    savefig("roc_ann.png")

    save_metrics("ann", metrics)
    plot_model_comparison()
    print("Saved ANN to", ANN_PATH, "and figures to", FIGURES_DIR)


if __name__ == "__main__":
    main()
