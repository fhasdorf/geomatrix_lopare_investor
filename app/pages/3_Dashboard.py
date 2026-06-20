"""Gated — Investor Dashboard. Phase 0 placeholder, no auth yet."""

import streamlit as st

from app._access import require_access
from app._i18n import init_lang, render_lang_toggle
from app._theme import inject_theme

st.set_page_config(page_title="Dashboard — Lopare", layout="wide")
inject_theme()
init_lang()
render_lang_toggle()
require_access()  # Phase 4 enforces real gate

st.title("Investor Dashboard")
st.warning(
    "Dashboard with market context, scenario modeling, comparables, and drill-program "
    "summary — coming in Phase 5. Access will be gated via Magic-Link in Phase 4."
)
