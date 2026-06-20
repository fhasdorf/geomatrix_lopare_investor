"""Public — Project Map. Phase 2a: real map with categorized markers."""

import streamlit as st
from streamlit_folium import st_folium

from app._data import load_collars, get_concession_area_km2
from app._map_helpers import build_map, render_legend
from app._theme import inject_theme

st.set_page_config(page_title="Project Map — Lopare", layout="wide")
inject_theme()

# Sidebar controls
with st.sidebar:
    st.markdown("### Map controls")
    color_by_label = st.radio(
        "Color markers by",
        ["Lithium", "Boron"],
        index=0,
        horizontal=True,
    )
    color_by = "li" if color_by_label == "Lithium" else "b"

    tile_style = st.radio(
        "Base map",
        ["Dark", "Satellite"],
        index=0,
        horizontal=True,
    )

    st.markdown("---")
    st.markdown(render_legend(color_by), unsafe_allow_html=True)

# Header
st.title("Project Map")
st.caption(
    f"Lopare license area · {get_concession_area_km2():.1f} km² · "
    f"{len(load_collars())} drill holes (best-intercept categorization)"
)

# Map
m = build_map(color_by=color_by, tile_style=tile_style)
st_folium(
    m,
    use_container_width=True,
    height=620,
    returned_objects=[],  # don't return click events — keeps app fast
)

# Footnote
st.caption(
    "Categories reflect the highest single-sample assay grade observed within "
    "each hole. Numeric assay values are not displayed. See the Disclaimer page "
    "for methodology and source references."
)
