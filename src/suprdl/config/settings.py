from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PathsConfig:
    database: Path
    cache: Path
    downloads: Path
    library: Path
    reports: Path


@dataclass(frozen=True)
class ApplicationConfig:
    log_level: str
    workers: int
    default_profile: str


@dataclass(frozen=True)
class MatchingConfig:
    automatic_accept_threshold: int
    review_threshold: int


@dataclass(frozen=True)
class SpotifyConfig:
    client_id_env: str
    client_secret_env: str


@dataclass(frozen=True)
class Settings:
    paths: PathsConfig
    application: ApplicationConfig
    matching: MatchingConfig
    spotify: SpotifyConfig


def load_settings(config_path: Path) -> Settings:
    """Carga la configuración desde un archivo TOML."""
    with config_path.open("rb") as file:
        raw = tomllib.load(file)

    return Settings(
        paths=PathsConfig(
            database=Path(raw["paths"]["database"]),
            cache=Path(raw["paths"]["cache"]),
            downloads=Path(raw["paths"]["downloads"]),
            library=Path(raw["paths"]["library"]),
            reports=Path(raw["paths"]["reports"]),
        ),
        application=ApplicationConfig(
            log_level=raw["application"]["log_level"],
            workers=int(raw["application"]["workers"]),
            default_profile=raw["application"]["default_profile"],
        ),
        matching=MatchingConfig(
            automatic_accept_threshold=int(
                raw["matching"]["automatic_accept_threshold"]
            ),
            review_threshold=int(raw["matching"]["review_threshold"]),
        ),
        spotify=SpotifyConfig(
            client_id_env=raw["spotify"]["client_id_env"],
            client_secret_env=raw["spotify"]["client_secret_env"],
        ),
    )


def default_config_path(project_root: Path) -> Path:
    """Devuelve la ruta de configuración predeterminada."""
    return project_root / "config" / "default.toml"
