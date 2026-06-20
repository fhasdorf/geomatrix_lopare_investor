"""Public — Disclaimer. Phase 3: sprachabhängig."""

import streamlit as st

from app._data import load_disclaimer
from app._i18n import init_lang, render_lang_toggle
from app._theme import inject_theme

st.set_page_config(page_title="Disclaimer — Lopare", layout="wide")
inject_theme()
init_lang()
render_lang_toggle()

content = load_disclaimer()
st.markdown(content)
