"""Public — Opportunity / Story. Phase 0 placeholder."""

from pathlib import Path

import streamlit as st

from app._theme import inject_theme

st.set_page_config(page_title="Opportunity — Lopare", layout="wide")
inject_theme()

content_path = Path(__file__).parents[2] / "content" / "opportunity_en.md"
if content_path.exists():
    st.markdown(content_path.read_text(encoding="utf-8"))
else:
    st.title("Opportunity")
    st.info("Story content coming in Phase 3.")
