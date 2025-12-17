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
    stats = report.get("stats", {})

    if columns:
        lines.append("\n## Columns Overview\n")
        lines.append("| Column | Missing | Type | Unique | Min | Max |")
        lines.append("|--------|--------|------|--------|-----|-----|")
        for col in columns:
            col_stats = stats.get(col, {})
            lines.append(
                f"| {col} | {missing.get(col, 0)} | "
                f"{col_stats.get('type', '')} | {col_stats.get('unique', '')} | "
                f"{col_stats.get('min', '')} | {col_stats.get('max', '')} |"
            )

    path.write_text("\n".join(lines))


def print_summary(profile: dict) -> None:
    print("\n=== CSV Basic Profile Summary ===")
    print(f"Total rows: {profile.get('rows', 0)}")
    print(f"Total columns: {len(profile.get('columns', []))}")

    print("\nColumns and missing values:")
    for col in profile.get("columns", []):
        missing = profile.get("missing", {}).get(col, 0)
        stats = profile.get("stats", {}).get(col, {})
        print(f"- {col}: missing={missing}, type={stats.get('type')}, unique={stats.get('unique')}, min={stats.get('min')}, max={stats.get('max')}")

    if "notes" in profile:
        print("\nNotes:")
        for note in profile["notes"]:
            print(f"* {note}")
