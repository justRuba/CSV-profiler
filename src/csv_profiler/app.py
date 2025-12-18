import streamlit as st
from csv_profiler.io import read_csv_rows
from csv_profiler.profile import basic_profile
from csv_profiler.render import write_json, write_markdown
from io import StringIO
import csv
from pathlib import Path
import tempfile

st.set_page_config(page_title="CSV Profiler", layout="wide")
st.title("CSV Profiler")
st.caption("Upload CSV → Profile → Export")

uploaded = st.sidebar.file_uploader("Upload CSV", type=["csv"])

if uploaded:
    text = uploaded.getvalue().decode("utf-8") 
    rows = list(csv.DictReader(StringIO(text)))

if st.button("Generate Profile") and uploaded:
    profile = basic_profile(rows)
    st.session_state["profile"] = profile

if "profile" in st.session_state:
    profile = st.session_state["profile"]

    st.write(f"**Rows:** {profile['rows']}")
    st.write(f"**Columns:** {profile['columns']}")

    st.subheader("Missing Values")
    st.table(profile["missing"])

    if "stats" in profile:
        st.subheader("Column Statistics")
        stats_data = []
        for col, stats in profile["stats"].items():
            stats_data.append({
                "Column": col,
                "Type": stats.get("type"),
                "Unique": stats.get("unique"),
                "Min": stats.get("min"),
                "Max": stats.get("max")
            })
        st.table(stats_data)

    tmp_json = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
    write_json(profile, tmp_json.name)
    st.download_button(
        label="Download JSON",
        data=open(tmp_json.name, "rb").read(),
        file_name="report.json",
        mime="application/json"
    )

    tmp_md = tempfile.NamedTemporaryFile(delete=False, suffix=".md")
    write_markdown(profile, tmp_md.name)
    st.download_button(
        label="Download Markdown",
        data=open(tmp_md.name, "rb").read(),
        file_name="report.md",
        mime="text/markdown"
    )
