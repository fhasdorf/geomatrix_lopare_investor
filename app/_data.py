"""Centralized data loaders for public Investor data with Streamlit caching."""

from __future__ import annotations

import json
from pathlib import Path

import geopandas as gpd
import pandas as pd
import streamlit as st

DATA_DIR = Path(__file__).parent.parent / "data" / "public"


@st.cache_data
def load_collars() -> pd.DataFrame:
    """Categorized drill collars. 71 holes, 6 columns. No raw assay values."""
    return pd.read_parquet(DATA_DIR / "collars_categorized.parquet")


@st.cache_data
def load_concession_geojson() -> dict:
    """Concession polygon as GeoJSON dict (Folium-ready). EPSG:4326."""
    with open(DATA_DIR / "concession_lopare.geojson", encoding="utf-8") as f:
        return json.load(f)


@st.cache_data
def load_concession_gdf() -> gpd.GeoDataFrame:
    """Concession polygon as GeoDataFrame (for bounds calculation, area metrics)."""
    return gpd.read_file(DATA_DIR / "concession_lopare.geojson")


@st.cache_data
def load_methodology() -> str:
    """Methodology Markdown for inline rendering."""
    return (DATA_DIR / "methodology.md").read_text(encoding="utf-8")


# ---- Aggregate helpers (für KPI-Tiles) ----

@st.cache_data
def get_total_holes() -> int:
    return len(load_collars())


@st.cache_data
def get_category_counts(element: str) -> dict[str, int]:
    """Returns counts per category for 'li' or 'b'.
    Order: Bonanza > High-grade > Mineralized > Trace > Pending (natürliche Story-Reihenfolge)."""
    df = load_collars()
    col = f"{element}_category"
    if col not in df.columns:
        raise ValueError(f"Column {col} not in collars data")
    counts = df[col].value_counts().to_dict()
    order = ["Bonanza", "High-grade", "Mineralized", "Trace", "Pending"]
    return {k: counts.get(k, 0) for k in order}


@st.cache_data
def get_concession_area_km2() -> float:
    """Reads 'area_km2_native' property from the GeoJSON feature."""
    gj = load_concession_geojson()
    return float(gj["features"][0]["properties"].get("area_km2_native", 87.7))
