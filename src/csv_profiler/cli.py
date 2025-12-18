from pathlib import Path
import subprocess
import sys
import typer

from csv_profiler.io import read_csv_rows
from csv_profiler.profile import basic_profile
from csv_profiler.render import write_json, write_markdown, print_summary

app = typer.Typer(help="CSV Profiler CLI")

def run_profile(path: Path, output: Path = Path("outputs"), fmt: str = "all"):
    if not path.exists():
        typer.echo(f"Error: File {path} does not exist")
        raise typer.Exit(1)
    rows = read_csv_rows(path)
    report = basic_profile(rows)
    output.mkdir(exist_ok=True)

    if fmt in ("json", "all"):
        write_json(report, output / "report.json")
    if fmt in ("md", "all"):
        write_markdown(report, output / "report.md")

    typer.echo(f"Wrote report to {output}")
    print_summary(report)

@app.command()
def profile(
    path: Path = typer.Argument(..., help="Path to CSV file"),
    output: Path = typer.Option(Path("outputs"), "--out-dir", "-o", help="Output folder"),
    fmt: str = typer.Option("both", "--format", "-f", help="Output format: json, md, or both")
):
    """Profile a CSV file"""
    rows = read_csv_rows(path)
    report = basic_profile(rows)
    output.mkdir(exist_ok=True)

    if fmt in ("json", "both"):
        write_json(report, output / "report.json")
    if fmt in ("md", "both"):
        write_markdown(report, output / "report.md")

    typer.echo(f"Wrote report to {output}")
    print_summary(report)


@app.command()
def web():
    """Launch the Streamlit web interface"""
    app_path = Path(__file__).parent / "app.py" 
    typer.echo("Starting Streamlit app...")
    subprocess.run([sys.executable, "-m", "streamlit", "run", str(app_path)])


if __name__ == "__main__":
    app()
