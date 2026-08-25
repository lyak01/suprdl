from __future__ import annotations

import sqlite3
from pathlib import Path

SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS playlists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    spotify_id TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    url TEXT NOT NULL,
    imported_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status TEXT NOT NULL DEFAULT 'imported'
);

CREATE TABLE IF NOT EXISTS tracks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    playlist_id INTEGER NOT NULL,
    position INTEGER NOT NULL,
    spotify_id TEXT UNIQUE,
    isrc TEXT,
    title_original TEXT NOT NULL,
    artists_original TEXT NOT NULL,
    album_original TEXT,
    duration_ms INTEGER,
    track_number INTEGER,
    disc_number INTEGER,
    release_date TEXT,
    explicit INTEGER NOT NULL DEFAULT 0,
    spotify_url TEXT,
    cover_url TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (playlist_id) REFERENCES playlists (id) ON DELETE CASCADE,
    UNIQUE (playlist_id, position)
);

CREATE INDEX IF NOT EXISTS idx_tracks_playlist_id
ON tracks (playlist_id);

CREATE INDEX IF NOT EXISTS idx_tracks_isrc
ON tracks (isrc);
"""


def connect_database(database_path: Path) -> sqlite3.Connection:
    """Abre una conexión SQLite configurada para SUPRDL."""
    database_path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def initialize_database(database_path: Path) -> None:
    """Crea la estructura inicial de la base de datos."""
    with connect_database(database_path) as connection:
        connection.executescript(SCHEMA)


def database_tables(database_path: Path) -> list[str]:
    """Devuelve las tablas de usuario existentes."""
    with connect_database(database_path) as connection:
        rows = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name NOT LIKE 'sqlite_%'
            ORDER BY name
            """
        ).fetchall()

    return [row["name"] for row in rows]
