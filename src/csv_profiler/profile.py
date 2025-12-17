
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

def basic_profile(rows: list[dict[str, str]]) -> dict:

    if not rows:
        return {"rows": 0, "columns": [], "missing": {}, "notes": ["Empty dataset"]}

    n_rows = len(rows)
    columns = list(rows[0].keys())
    missing = count_missing(rows)

    return {
        "rows": n_rows,
        "columns": columns,
        "missing": missing,
    }
