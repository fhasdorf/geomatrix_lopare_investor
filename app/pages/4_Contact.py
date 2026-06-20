"""Public — Contact and access request. Phase 0 placeholder."""

import streamlit as st

from app._i18n import init_lang, render_lang_toggle
from app._theme import inject_theme

st.set_page_config(page_title="Contact — Lopare", layout="wide")
inject_theme()
init_lang()
render_lang_toggle()

st.title("Contact")
st.info("Quick-inquiry form and investor-access request — coming in Phase 3 and Phase 4.")
