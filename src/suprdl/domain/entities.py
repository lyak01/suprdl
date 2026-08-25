from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Playlist:
    spotify_id: str
    name: str
    url: str
    id: int | None = None
    status: str = "imported"


@dataclass(slots=True)
class Track:
    playlist_id: int
    position: int
    title_original: str
    artists_original: str
    id: int | None = None
    spotify_id: str | None = None
    isrc: str | None = None
    album_original: str | None = None
    duration_ms: int | None = None
    track_number: int | None = None
    disc_number: int | None = None
    release_date: str | None = None
    explicit: bool = False
    spotify_url: str | None = None
    cover_url: str | None = None
