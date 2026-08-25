from pathlib import Path

from suprdl.config.settings import load_settings


def test_load_default_settings() -> None:
    config_path = Path("config/default.toml")

    settings = load_settings(config_path)

    assert settings.application.workers == 1
    assert settings.application.default_profile == "original"
    assert settings.matching.review_threshold == 70
    assert settings.spotify.client_id_env == "SUPRDL_SPOTIFY_CLIENT_ID"
