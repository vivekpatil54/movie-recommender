"""One command to build everything: database -> ML models -> ANN.

Run:  python -m src.train_all
"""
from src import seed, train_ann, train_ml

if __name__ == "__main__":
    print("=" * 60, "\n1/3  Seeding SQLite database\n" + "=" * 60)
    seed.seed()
    print("=" * 60, "\n2/3  Training ML models (AI-503)\n" + "=" * 60)
    train_ml.main()
    print("=" * 60, "\n3/3  Training ANN (AI-505)\n" + "=" * 60)
    train_ann.main()
    print("\nAll done. Start the app:\n  python -m src.api        (terminal 1)\n  streamlit run app.py     (terminal 2)")
