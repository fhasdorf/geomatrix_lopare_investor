"""Public — Disclaimer. Phase 0 placeholder, loads from content/disclaimer_en.md."""

from pathlib import Path

import streamlit as st

from app._theme import inject_theme

st.set_page_config(page_title="Disclaimer — Lopare", layout="wide")
inject_theme()

content_path = Path(__file__).parents[2] / "content" / "disclaimer_en.md"
if content_path.exists():
    st.markdown(content_path.read_text(encoding="utf-8"))
else:
    st.title("Disclaimer")
    st.info("Full disclaimer text coming in Phase 3, anwaltlich freigegeben vor Go-Live.")
