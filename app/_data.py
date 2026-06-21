"""Centralized data loaders for public Investor data with Streamlit caching."""

from __future__ import annotations

import json
from pathlib import Path

import geopandas as gpd
import pandas as pd
import streamlit as st

from app._i18n import get_lang

DATA_DIR = Path(__file__).parent.parent / "data" / "public"
CONTENT_DIR = Path(__file__).parent.parent / "content"


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


# ---- Language-dependent content loaders ----

@st.cache_data
def _load_content_file(name: str, lang: str) -> str:
    """Generic markdown content loader by name and language."""
    path = CONTENT_DIR / f"{name}_{lang}.md"
    return path.read_text(encoding="utf-8")


def load_opportunity() -> str:
    """Loads opportunity content in the currently active language."""
    return _load_content_file("opportunity", get_lang())


def load_disclaimer() -> str:
    """Loads disclaimer content in the currently active language."""
    return _load_content_file("disclaimer", get_lang())


# ---- Market data loaders ----

@st.cache_data
def load_market_lithium() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "market_lithium.csv")


@st.cache_data
def load_market_boron() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "market_boron.csv")


@st.cache_data
def load_eu_context() -> dict:
    with open(DATA_DIR / "market_eu_context.json", encoding="utf-8") as f:
        return json.load(f)


# Resource-Snapshot-Konstanten (aus MRE-Report, hardcoded für Dashboard-KPIs)
RESOURCE_SNAPSHOT = {
    "total_mt": 1286,
    "avg_li2o_ppm": 574,
    "avg_b2o3_pct": 0.75,
    "concession_km2": 87.7,
    "boron_subtotal_mt": 1.3,
    "boron_subtotal_grade_pct": 5.61,
    "source": "CSA Global R268.2022 (30 July 2022)",
}
