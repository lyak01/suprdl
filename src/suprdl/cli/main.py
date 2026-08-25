from __future__ import annotations

import platform
from importlib.metadata import version as package_version
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from suprdl.config.settings import default_config_path, load_settings
from suprdl.infrastructure.database import (
    database_tables,
    initialize_database,
)

app = typer.Typer(
    name="suprdl",
    help="Gestor modular de bibliotecas de audio.",
    no_args_is_help=True,
)

config_app = typer.Typer(
    name="config",
    help="Gestiona la configuración de suprdl.",
)

db_app = typer.Typer(
    name="db",
    help="Gestiona la base de datos local.",
)

app.add_typer(config_app, name="config")
app.add_typer(db_app, name="db")

console = Console()


@app.command("version")
def show_version() -> None:
    """Muestra la versión instalada de suprdl."""
    console.print(f"suprdl {package_version('suprdl')}")


@app.command()
def doctor() -> None:
    """Comprueba el estado básico del entorno local."""
    project_root = Path.cwd()
    config_path = default_config_path(project_root)

    console.print("[green]Entorno básico disponible.[/green]")
    console.print(f"Python: {platform.python_version()}")
    console.print(f"suprdl: {package_version('suprdl')}")
    console.print(f"Configuración: {config_path}")

    if not config_path.is_file():
        console.print("[red]Configuración no encontrada.[/red]")
        raise typer.Exit(code=1)

    console.print("[green]Configuración encontrada.[/green]")

    settings = load_settings(config_path)
    database_path = settings.paths.database

    if database_path.is_file():
        tables = database_tables(database_path)
        console.print("[green]Base de datos encontrada.[/green]")
        console.print(f"Tablas: {', '.join(tables) or 'ninguna'}")
    else:
        console.print("[yellow]Base de datos todavía no inicializada.[/yellow]")


@config_app.command("show")
def show_config() -> None:
    """Muestra la configuración predeterminada."""
    config_path = default_config_path(Path.cwd())

    if not config_path.is_file():
        raise typer.BadParameter(f"No existe: {config_path}")

    settings = load_settings(config_path)

    table = Table(title="Configuración de SUPRDL")
    table.add_column("Sección")
    table.add_column("Clave")
    table.add_column("Valor")

    table.add_row("paths", "database", str(settings.paths.database))
    table.add_row("paths", "cache", str(settings.paths.cache))
    table.add_row("paths", "downloads", str(settings.paths.downloads))
    table.add_row("paths", "library", str(settings.paths.library))
    table.add_row("paths", "reports", str(settings.paths.reports))

    table.add_row(
        "application",
        "log_level",
        settings.application.log_level,
    )
    table.add_row(
        "application",
        "workers",
        str(settings.application.workers),
    )
    table.add_row(
        "application",
        "default_profile",
        settings.application.default_profile,
    )

    table.add_row(
        "matching",
        "automatic_accept_threshold",
        str(settings.matching.automatic_accept_threshold),
    )
    table.add_row(
        "matching",
        "review_threshold",
        str(settings.matching.review_threshold),
    )

    table.add_row(
        "spotify",
        "client_id_env",
        settings.spotify.client_id_env,
    )
    table.add_row(
        "spotify",
        "client_secret_env",
        settings.spotify.client_secret_env,
    )

    console.print(table)


@db_app.command("init")
def init_database() -> None:
    """Inicializa la base de datos local."""
    config_path = default_config_path(Path.cwd())

    if not config_path.is_file():
        raise typer.BadParameter(f"No existe: {config_path}")

    settings = load_settings(config_path)
    database_path = settings.paths.database

    initialize_database(database_path)

    console.print(f"[green]Base inicializada:[/green] {database_path}")


@db_app.command("status")
def database_status() -> None:
    """Muestra el estado de la base de datos local."""
    config_path = default_config_path(Path.cwd())

    if not config_path.is_file():
        raise typer.BadParameter(f"No existe: {config_path}")

    settings = load_settings(config_path)
    database_path = settings.paths.database

    if not database_path.is_file():
        console.print("[yellow]La base de datos todavía no existe.[/yellow]")
        raise typer.Exit(code=1)

    tables = database_tables(database_path)

    console.print(f"Base de datos: {database_path}")
    console.print(f"Tablas: {', '.join(tables) or 'ninguna'}")


if __name__ == "__main__":
    app()
