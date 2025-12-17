
def count_missing(rows: list[dict[str, str]]) -> dict[str, int]:
    if not rows:
        return {}
    missing_count = {key: 0 for key in rows[0]}
    for row in rows:
        for key in row:
            value = row[key].strip()
            if value == "":
                missing_count[key] += 1
    return missing_count

def detect_type(values: list[str]) -> str:
    non_empty = [v for v in values if v.strip() != ""]
    if not non_empty:
        return "unknown"
    try:
        for v in non_empty:
            int(v)
        return "int"
    except ValueError:
        try:
            for v in non_empty:
                float(v)
            return "float"
        except ValueError:
            return "str"

def basic_profile(rows: list[dict[str, str]]) -> dict:
    if not rows:
        return {"rows": 0, "columns": [], "missing": {}, "notes": ["Empty dataset"]}

    n_rows = len(rows)
    columns = list(rows[0].keys())
    missing = count_missing(rows)

    column_stats = {}

    for col in columns:
        values = [row[col].strip() for row in rows if row[col].strip() != ""]
        if values:
            # Convert numbers if possible
            col_type = detect_type(values)
            if col_type == "int":
                num_values = [int(v) for v in values]
            elif col_type == "float":
                num_values = [float(v) for v in values]
            else:
                num_values = values

            column_stats[col] = {
                "type": col_type,
                "unique": len(set(values)),
                "min": min(num_values) if col_type in ("int", "float") else None,
                "max": max(num_values) if col_type in ("int", "float") else None,
            }
        else:
            column_stats[col] = {
                "type": "unknown",
                "unique": 0,
                "min": None,
                "max": None,
            }

    return {
        "rows": n_rows,
        "columns": columns,
        "missing": missing,
        "stats": column_stats,
    }
