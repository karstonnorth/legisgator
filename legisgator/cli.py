import asyncio, typer, pathlib, sys
from rich.progress import Progress
from .engine import analyze
from .printer import render
from .config import get_settings

app = typer.Typer(add_completion=False)

@app.command(help="Analyse raw contract/text file")
def file(path: pathlib.Path):
    cfg = get_settings()
    text = path.read_text(encoding="utf-8")
    if len(text.encode()) > cfg.MAX_PAYLOAD_KB * 1024:
        typer.echo("File too large, coward. Trim it.", err=True)
        sys.exit(1)
    with Progress() as bar:
        task = bar.add_task("Crunching…", total=3)
        result = asyncio.run(analyze(text))
        bar.update(task, advance=3)
    render(result)

if __name__ == "__main__":
    app()
