from pathlib import Path

from suprdl.domain.entities import Playlist, Track
from suprdl.infrastructure.database import (
    connect_database,
    initialize_database,
)
from suprdl.infrastructure.repositories import (
    PlaylistRepository,
    TrackRepository,
)


def create_test_repositories(
    database_path: Path,
) -> tuple[PlaylistRepository, TrackRepository]:
    initialize_database(database_path)
    connection = connect_database(database_path)

    return PlaylistRepository(connection), TrackRepository(connection)


def test_playlist_can_be_created_and_retrieved(tmp_path: Path) -> None:
    playlist_repository, _ = create_test_repositories(tmp_path / "test.db")

    playlist = Playlist(
        spotify_id="spotify-playlist-1",
        name="Playlist de prueba",
        url="https://open.spotify.com/playlist/spotify-playlist-1",
    )

    created = playlist_repository.create(playlist)
    loaded = playlist_repository.get_by_id(created.id)

    assert created.id is not None
    assert loaded == created


def test_playlist_can_be_found_by_spotify_id(tmp_path: Path) -> None:
    playlist_repository, _ = create_test_repositories(tmp_path / "test.db")

    playlist_repository.create(
        Playlist(
            spotify_id="spotify-playlist-2",
            name="Otra playlist",
            url="https://open.spotify.com/playlist/spotify-playlist-2",
        )
    )

    loaded = playlist_repository.get_by_spotify_id("spotify-playlist-2")

    assert loaded is not None
    assert loaded.name == "Otra playlist"


def test_tracks_are_listed_by_position(tmp_path: Path) -> None:
    playlist_repository, track_repository = create_test_repositories(
        tmp_path / "test.db"
    )

    playlist = playlist_repository.create(
        Playlist(
            spotify_id="spotify-playlist-3",
            name="Playlist con canciones",
            url="https://open.spotify.com/playlist/spotify-playlist-3",
        )
    )

    track_repository.create(
        Track(
            playlist_id=playlist.id,
            position=2,
            title_original="Segunda",
            artists_original="Artista",
        )
    )
    track_repository.create(
        Track(
            playlist_id=playlist.id,
            position=1,
            title_original="Primera",
            artists_original="Artista",
        )
    )

    tracks = track_repository.list_by_playlist(playlist.id)

    assert [track.position for track in tracks] == [1, 2]
    assert track_repository.count_by_playlist(playlist.id) == 2
