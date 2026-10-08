import shutil

import pytest

from src import db
from src.config import DB_PATH


@pytest.fixture
def empty_db(tmp_path, monkeypatch):
    """A fresh, empty database in a temp folder (the real database is never touched)."""
    monkeypatch.setattr(db, "DB_PATH", tmp_path / "test.db")
    db.init_db()
    return tmp_path / "test.db"


@pytest.fixture
def seeded_db(tmp_path, monkeypatch):
    """A temp copy of the real seeded database (MovieLens + demo accounts)."""
    if not DB_PATH.exists():
        pytest.skip("Run `python -m src.train_all` first")
    path = tmp_path / "seeded.db"
    shutil.copy(DB_PATH, path)
    monkeypatch.setattr(db, "DB_PATH", path)
    return path
