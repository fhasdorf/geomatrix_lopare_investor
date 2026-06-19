"""Public — Project Map. Phase 0 placeholder."""

import streamlit as st

from app._theme import inject_theme

st.set_page_config(page_title="Project Map — Lopare", layout="wide")
inject_theme()

st.title("Project Map")
st.info("Folium map with concession polygon and categorized drill holes — coming in Phase 2.")
