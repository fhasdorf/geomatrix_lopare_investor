"""Folium map construction for the Investor app.

Marker color scheme is element-agnostic — same scale for Li and B, so users
can toggle between elements without re-learning the legend.
"""

from __future__ import annotations

from typing import Literal

import folium
import pandas as pd

from app._data import load_collars, load_concession_geojson

# Category color palette (theme-consistent: dunkelblau-tech accents)
CATEGORY_COLORS: dict[str, str] = {
    "Trace":       "#5A6B7E",  # muted blue-grey: present but below threshold
    "Mineralized": "#7DA7D9",  # light blue: within MRE resource range
    "High-grade":  "#3DD9D6",  # theme cyan: primary target of the deposit
    "Bonanza":     "#FFB547",  # theme gold: exceptional grades
    "Pending":     "#FFFFFF",  # white outline (no fill): not yet evaluated
}

CATEGORY_ORDER: list[str] = ["Bonanza", "High-grade", "Mineralized", "Trace", "Pending"]

# Tile providers — both free, no API key required
TILE_PROVIDERS: dict[str, dict] = {
    "Dark": {
        "tiles": "cartodbdark_matter",
        "attr": "© CartoDB © OpenStreetMap contributors",
    },
    "Satellite": {
        "tiles": (
            "https://server.arcgisonline.com/ArcGIS/rest/services/"
            "World_Imagery/MapServer/tile/{z}/{y}/{x}"
        ),
        "attr": "Tiles © Esri — Source: Esri, Maxar, Earthstar Geographics",
    },
}

# Concession polygon style
CONCESSION_STYLE = {
    "color":       "#FFB547",  # gold outline
    "weight":      2.5,
    "fillColor":   "#FFB547",
    "fillOpacity": 0.08,
    "opacity":     0.9,
}


def build_map(
    color_by: Literal["li", "b"] = "li",
    tile_style: Literal["Dark", "Satellite"] = "Dark",
) -> folium.Map:
    """Construct a Folium map with concession polygon + categorized drill markers.

    Args:
        color_by: which element drives marker color ('li' or 'b')
        tile_style: 'Dark' or 'Satellite'

    Returns:
        Folium Map object, ready for streamlit_folium.st_folium()
    """
    concession = load_concession_geojson()
    collars = load_collars()

    # Center on concession centroid (rough — first vertex of polygon)
    coords = concession["features"][0]["geometry"]["coordinates"][0]
    center_lat = sum(c[1] for c in coords) / len(coords)
    center_lon = sum(c[0] for c in coords) / len(coords)

    tile_cfg = TILE_PROVIDERS[tile_style]
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=13,
        tiles=tile_cfg["tiles"],
        attr=tile_cfg["attr"],
        control_scale=True,
    )

    # Concession polygon
    folium.GeoJson(
        concession,
        name="License area",
        style_function=lambda _: CONCESSION_STYLE,
        tooltip=folium.GeoJsonTooltip(
            fields=["name"],
            aliases=["License:"],
            sticky=False,
        ),
    ).add_to(m)

    # Drill markers
    category_col = f"{color_by}_category"
    for _, row in collars.iterrows():
        cat = row[category_col]
        color = CATEGORY_COLORS.get(cat, "#888888")
        is_pending = cat == "Pending"

        popup_html = _build_popup(row)

        if is_pending:
            # Pending: hollow ring (white outline, transparent fill)
            folium.CircleMarker(
                location=[row["lat_wgs84"], row["lon_wgs84"]],
                radius=6,
                color=color,
                weight=2,
                fill=True,
                fill_color="#000000",
                fill_opacity=0.0,
                popup=folium.Popup(popup_html, max_width=260),
                tooltip=f"{row['pseudo_id']} (Pending)",
            ).add_to(m)
        else:
            folium.CircleMarker(
                location=[row["lat_wgs84"], row["lon_wgs84"]],
                radius=6,
                color=color,
                weight=1,
                fill=True,
                fill_color=color,
                fill_opacity=0.85,
                popup=folium.Popup(popup_html, max_width=260),
                tooltip=f"{row['pseudo_id']} — {cat}",
            ).add_to(m)

    return m


def _build_popup(row: pd.Series) -> str:
    """Lightweight HTML popup with hole metadata."""
    return f"""
    <div style="font-family:system-ui,sans-serif;font-size:13px;line-height:1.5">
        <div style="font-weight:600;font-size:14px;margin-bottom:4px">
            {row['pseudo_id']}
        </div>
        <div style="color:#5A6B7E;margin-bottom:6px">
            Campaign: {row['year_bucket']}
        </div>
        <div><b>Lithium:</b> {row['li_category']}</div>
        <div><b>Boron:</b> {row['b_category']}</div>
    </div>
    """


def render_legend(color_by: Literal["li", "b"]) -> str:
    """Returns inline HTML for a category legend (used in the sidebar or below the map)."""
    element_label = "Lithium" if color_by == "li" else "Boron"
    rows = []
    for cat in CATEGORY_ORDER:
        color = CATEGORY_COLORS[cat]
        if cat == "Pending":
            swatch = (
                f'<span style="display:inline-block;width:14px;height:14px;'
                f'border:2px solid {color};border-radius:50%;margin-right:8px;'
                f'vertical-align:middle"></span>'
            )
        else:
            swatch = (
                f'<span style="display:inline-block;width:14px;height:14px;'
                f'background:{color};border-radius:50%;margin-right:8px;'
                f'vertical-align:middle"></span>'
            )
        rows.append(
            f'<div style="margin:4px 0;font-size:13px">{swatch}{cat}</div>'
        )
    return (
        f'<div style="padding:8px 0">'
        f'<div style="font-weight:600;margin-bottom:6px">{element_label} category</div>'
        + "".join(rows) +
        f'</div>'
    )
