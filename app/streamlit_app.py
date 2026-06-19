"""Landing page (public). Phase 0 skeleton — Lorem-Ipsum placeholders."""

import streamlit as st

from app._theme import inject_theme

st.set_page_config(
    page_title="Lopare Project — Strategic Lithium & Boron",
    page_icon="⛰️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_theme()

# Hero
st.markdown("# Lopare")
st.markdown(
    "### Strategic Lithium & Boron Project in the EU's Doorstep"
)
st.caption(
    "87.7 km² licensed exploration area · 70+ drill holes · CRMA-aligned commodities"
)

st.divider()

# KPI tiles — Phase 0 placeholders, Phase 2 will style these as glassmorphism cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Licensed area", "87.7 km²")
col2.metric("Drill program", "70+ holes")
col3.metric("Primary commodities", "Li · B")
col4.metric("Jurisdiction", "BiH (EU candidate)")

st.divider()

st.markdown("## Investment Thesis")
st.markdown(
    "*One-liner placeholder — will be replaced with ARCore-approved copy in Phase 3.*"
)

st.markdown("### Why Lopare")
why1, why2, why3 = st.columns(3)
with why1:
    st.markdown("**EU-aligned supply**")
    st.caption("CRMA-listed commodities, sourced inside the EU's strategic perimeter.")
with why2:
    st.markdown("**Multi-commodity upside**")
    st.caption("Lithium plus boron plus co-products — diversified revenue model.")
with why3:
    st.markdown("**Advanced exploration stage**")
    st.caption("MRE work completed by CSA Global; ready for next-phase studies.")

st.divider()
st.caption(
    "This is a non-binding overview. Forward-looking statements subject to disclaimer."
)
