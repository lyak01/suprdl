from __future__ import annotations

import platform
from importlib.metadata import version as package_version

import typer
from rich.console import Console

app = typer.Typer(
    name="suprdl",
    help="Gestor modular de bibliotecas de audio.",
    no_args_is_help=True,
)

console = Console()


@app.command("version")
def show_version() -> None:
    """Muestra la versión instalada de suprdl."""
    console.print(f"suprdl {package_version('suprdl')}")


@app.command()
def doctor() -> None:
    """Comprueba el estado básico del entorno local."""
    console.print("[green]Entorno básico disponible.[/green]")
    console.print(f"Python: {platform.python_version()}")
    console.print(f"suprdl: {package_version('suprdl')}")


if __name__ == "__main__":
    app()
