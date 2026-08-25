from __future__ import annotations

import sqlite3

from suprdl.domain.entities import Playlist, Track


class PlaylistRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

    def create(self, playlist: Playlist) -> Playlist:
        cursor = self.connection.execute(
            """
            INSERT INTO playlists (spotify_id, name, url, status)
            VALUES (?, ?, ?, ?)
            """,
            (
                playlist.spotify_id,
                playlist.name,
                playlist.url,
                playlist.status,
            ),
        )
        self.connection.commit()

        playlist.id = int(cursor.lastrowid)
        return playlist

    def get_by_id(self, playlist_id: int) -> Playlist | None:
        row = self.connection.execute(
            """
            SELECT id, spotify_id, name, url, status
            FROM playlists
            WHERE id = ?
            """,
            (playlist_id,),
        ).fetchone()

        if row is None:
            return None

        return Playlist(
            id=int(row["id"]),
            spotify_id=row["spotify_id"],
            name=row["name"],
            url=row["url"],
            status=row["status"],
        )

    def get_by_spotify_id(self, spotify_id: str) -> Playlist | None:
        row = self.connection.execute(
            """
            SELECT id, spotify_id, name, url, status
            FROM playlists
            WHERE spotify_id = ?
            """,
            (spotify_id,),
        ).fetchone()

        if row is None:
            return None

        return Playlist(
            id=int(row["id"]),
            spotify_id=row["spotify_id"],
            name=row["name"],
            url=row["url"],
            status=row["status"],
        )

    def list_all(self) -> list[Playlist]:
        rows = self.connection.execute(
            """
            SELECT id, spotify_id, name, url, status
            FROM playlists
            ORDER BY id
            """
        ).fetchall()

        return [
            Playlist(
                id=int(row["id"]),
                spotify_id=row["spotify_id"],
                name=row["name"],
                url=row["url"],
                status=row["status"],
            )
            for row in rows
        ]


class TrackRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

    def create(self, track: Track) -> Track:
        cursor = self.connection.execute(
            """
            INSERT INTO tracks (
                playlist_id,
                position,
                spotify_id,
                isrc,
                title_original,
                artists_original,
                album_original,
                duration_ms,
                track_number,
                disc_number,
                release_date,
                explicit,
                spotify_url,
                cover_url
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                track.playlist_id,
                track.position,
                track.spotify_id,
                track.isrc,
                track.title_original,
                track.artists_original,
                track.album_original,
                track.duration_ms,
                track.track_number,
                track.disc_number,
                track.release_date,
                int(track.explicit),
                track.spotify_url,
                track.cover_url,
            ),
        )
        self.connection.commit()

        track.id = int(cursor.lastrowid)
        return track

    def get_by_id(self, track_id: int) -> Track | None:
        row = self.connection.execute(
            """
            SELECT
                id,
                playlist_id,
                position,
                spotify_id,
                isrc,
                title_original,
                artists_original,
                album_original,
                duration_ms,
                track_number,
                disc_number,
                release_date,
                explicit,
                spotify_url,
                cover_url
            FROM tracks
            WHERE id = ?
            """,
            (track_id,),
        ).fetchone()

        if row is None:
            return None

        return self._from_row(row)

    def list_by_playlist(self, playlist_id: int) -> list[Track]:
        rows = self.connection.execute(
            """
            SELECT
                id,
                playlist_id,
                position,
                spotify_id,
                isrc,
                title_original,
                artists_original,
                album_original,
                duration_ms,
                track_number,
                disc_number,
                release_date,
                explicit,
                spotify_url,
                cover_url
            FROM tracks
            WHERE playlist_id = ?
            ORDER BY position
            """,
            (playlist_id,),
        ).fetchall()

        return [self._from_row(row) for row in rows]

    def count_by_playlist(self, playlist_id: int) -> int:
        row = self.connection.execute(
            """
            SELECT COUNT(*) AS total
            FROM tracks
            WHERE playlist_id = ?
            """,
            (playlist_id,),
        ).fetchone()

        return int(row["total"])

    @staticmethod
    def _from_row(row: sqlite3.Row) -> Track:
        return Track(
            id=int(row["id"]),
            playlist_id=int(row["playlist_id"]),
            position=int(row["position"]),
            spotify_id=row["spotify_id"],
            isrc=row["isrc"],
            title_original=row["title_original"],
            artists_original=row["artists_original"],
            album_original=row["album_original"],
            duration_ms=row["duration_ms"],
            track_number=row["track_number"],
            disc_number=row["disc_number"],
            release_date=row["release_date"],
            explicit=bool(row["explicit"]),
            spotify_url=row["spotify_url"],
            cover_url=row["cover_url"],
        )
