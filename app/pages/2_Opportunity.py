"""Public — Opportunity / Story. Phase 3: sprachabhängiger Story-Content."""

import streamlit as st

from app._data import load_opportunity
from app._i18n import init_lang, render_lang_toggle
from app._theme import inject_theme

st.set_page_config(page_title="Opportunity — Lopare", layout="wide")
inject_theme()
init_lang()
render_lang_toggle()

content = load_opportunity()
st.markdown(content)
