from pathlib import Path

from suprdl.infrastructure.database import (
    database_tables,
    initialize_database,
)


def test_initialize_database_creates_expected_tables(tmp_path: Path) -> None:
    database_path = tmp_path / "test.db"

    initialize_database(database_path)

    assert database_path.is_file()
    assert database_tables(database_path) == ["playlists", "tracks"]


def test_initialize_database_is_idempotent(tmp_path: Path) -> None:
    database_path = tmp_path / "test.db"

    initialize_database(database_path)
    initialize_database(database_path)

    assert database_tables(database_path) == ["playlists", "tracks"]
