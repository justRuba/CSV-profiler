
from pathlib import Path
import json

def write_json(report: dict, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")

def write_markdown(report: dict, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    lines: list[str] = []
    lines.append("# CSV Profiling Report\n")
    lines.append(f"- Rows: **{report.get('rows', 0)}**")
    columns = report.get("columns", [])
    missing = report.get("missing", {})

    if columns:
        lines.append("\n## Columns and Missing Values\n")
        lines.append("| Column | Missing |")
        lines.append("|--------|--------|")
        for col in columns:
            lines.append(f"| {col} | {missing.get(col, 0)} |")

    path.write_text("\n".join(lines))
