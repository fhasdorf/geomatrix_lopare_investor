"""Landing page (public). Phase 2a: real data in KPI tiles."""

import streamlit as st

from app._data import (
    get_category_counts,
    get_concession_area_km2,
    get_total_holes,
)
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
st.markdown("### Strategic Lithium & Boron Project in the EU's Doorstep")

# Pull aggregates once
total_holes = get_total_holes()
area_km2 = get_concession_area_km2()
li_counts = get_category_counts("li")

st.caption(
    f"{area_km2:.1f} km² licensed exploration area · "
    f"{total_holes} drill holes · CRMA-aligned commodities"
)

st.divider()

# KPI tiles
col1, col2, col3, col4 = st.columns(4)
col1.metric("Licensed area", f"{area_km2:.1f} km²")
col2.metric("Drill holes", str(total_holes))
col3.metric("Primary commodities", "Li · B")
col4.metric("Jurisdiction", "BiH (EU candidate)")

st.divider()

# Investment Thesis (Lorem-Ipsum bleibt, kommt in Phase 3)
st.markdown("## Investment Thesis")
st.markdown(
    "*One-liner placeholder — will be replaced with ARCore-approved copy in Phase 3.*"
)

# Mini lithium distribution
st.markdown("### Lithium grade distribution across the drill program")
li_bonanza = li_counts.get("Bonanza", 0)
li_highgrade = li_counts.get("High-grade", 0)
li_mineralized = li_counts.get("Mineralized", 0)
li_trace = li_counts.get("Trace", 0)
li_pending = li_counts.get("Pending", 0)
li_evaluated = total_holes - li_pending
li_significant = li_bonanza + li_highgrade

st.markdown(
    f"Of {li_evaluated} evaluated holes, **{li_significant} ({li_significant/li_evaluated*100:.0f}%)** "
    f"returned High-grade or Bonanza lithium intercepts. "
    f"{li_pending} holes remain pending."
)

# Simple horizontal bar via st.columns proportional widths
# (a real chart comes in Phase 5; this is the cheap version)
cat_data = [
    ("Bonanza",     li_bonanza,     "#FFB547"),
    ("High-grade",  li_highgrade,   "#3DD9D6"),
    ("Mineralized", li_mineralized, "#7DA7D9"),
    ("Trace",       li_trace,       "#5A6B7E"),
    ("Pending",     li_pending,     "#FFFFFF"),
]

bar_html = '<div style="display:flex;height:32px;border-radius:4px;overflow:hidden;margin:8px 0">'
for label, count, color in cat_data:
    if count == 0:
        continue
    pct = count / total_holes * 100
    border = "border:1px solid #3DD9D6;" if label == "Pending" else ""
    bar_html += (
        f'<div style="flex:{count};background:{color};{border}'
        f'display:flex;align-items:center;justify-content:center;'
        f'color:#0A1628;font-weight:600;font-size:12px" '
        f'title="{label}: {count} holes ({pct:.0f}%)">'
        f'{count if pct >= 8 else ""}</div>'
    )
bar_html += "</div>"

st.markdown(bar_html, unsafe_allow_html=True)

# Legend row
legend_cols = st.columns(5)
for col, (label, count, color) in zip(legend_cols, cat_data):
    col.markdown(
        f'<div style="font-size:12px;color:#7DA7D9">'
        f'<span style="display:inline-block;width:10px;height:10px;'
        f'background:{color};border-radius:50%;margin-right:6px"></span>'
        f'{label}: <b>{count}</b></div>',
        unsafe_allow_html=True,
    )

st.divider()

# "Why Lopare" Drei-Spalten (unverändert)
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
