"""Echarts chart configurations for the Lopare Investor Dashboard.

All functions return dict configs ready for streamlit_echarts.st_echarts().
Theme colors match the Dunkelblau-Tech palette used elsewhere in the app.
"""

from __future__ import annotations

from app._data import (
    load_collars,
    load_eu_context,
    load_market_boron,
    load_market_lithium,
)

# ---- Theme tokens ----
THEME = {
    "bg_transparent": "transparent",
    "text_primary": "#F0F4F8",
    "text_secondary": "#C5D2DC",
    "text_tertiary": "#7DA7D9",
    "accent_cyan": "#3DD9D6",
    "accent_gold": "#FFB547",
    "accent_blue": "#7DA7D9",
    "grid_subtle": "rgba(61, 217, 214, 0.08)",
    "tooltip_bg": "rgba(20, 40, 71, 0.95)",
}

CATEGORY_COLORS = {
    "Bonanza":     "#FFB547",
    "High-grade":  "#3DD9D6",
    "Mineralized": "#7DA7D9",
    "Trace":       "#5A6B7E",
    "Pending":     "#C5D2DC",
}


def _base_options() -> dict:
    """Common echarts options for dark theme consistency."""
    return {
        "backgroundColor": THEME["bg_transparent"],
        "textStyle": {
            "color": THEME["text_secondary"],
            "fontFamily": "Inter, sans-serif",
        },
        "tooltip": {
            "backgroundColor": THEME["tooltip_bg"],
            "borderColor": THEME["accent_cyan"],
            "borderWidth": 1,
            "textStyle": {"color": THEME["text_primary"]},
        },
    }


# ---- Chart 1: Program overview (drill holes by year × Li-category) ----

def chart_program_overview() -> dict:
    df = load_collars()
    pivot = (
        df.groupby(["year_bucket", "li_category"])
          .size()
          .unstack(fill_value=0)
    )
    cat_order = ["Bonanza", "High-grade", "Mineralized", "Trace", "Pending"]
    cat_order = [c for c in cat_order if c in pivot.columns]

    series = [
        {
            "name": cat,
            "type": "bar",
            "stack": "total",
            "emphasis": {"focus": "series"},
            "data": pivot[cat].tolist(),
            "itemStyle": {"color": CATEGORY_COLORS[cat]},
        }
        for cat in cat_order
    ]

    return {
        **_base_options(),
        "title": {
            "text": "Drill program by campaign and lithium category",
            "left": "left",
            "textStyle": {"color": THEME["text_primary"], "fontSize": 14, "fontWeight": "normal"},
        },
        "legend": {
            "data": cat_order,
            "textStyle": {"color": THEME["text_secondary"]},
            "bottom": 0,
        },
        "grid": {"left": "5%", "right": "5%", "top": "15%", "bottom": "15%", "containLabel": True},
        "xAxis": {
            "type": "category",
            "data": pivot.index.tolist(),
            "axisLine": {"lineStyle": {"color": THEME["text_tertiary"]}},
            "axisLabel": {"color": THEME["text_secondary"]},
        },
        "yAxis": {
            "type": "value",
            "name": "Drill holes",
            "nameTextStyle": {"color": THEME["text_tertiary"]},
            "splitLine": {"lineStyle": {"color": THEME["grid_subtle"]}},
            "axisLabel": {"color": THEME["text_secondary"]},
        },
        "series": series,
    }


# ---- Chart 2: Pie — drill holes by Li category ----

def chart_li_category_pie() -> dict:
    df = load_collars()
    counts = df["li_category"].value_counts().to_dict()
    cat_order = ["Bonanza", "High-grade", "Mineralized", "Trace", "Pending"]

    data = [
        {"value": counts.get(cat, 0), "name": cat,
         "itemStyle": {"color": CATEGORY_COLORS[cat]}}
        for cat in cat_order if counts.get(cat, 0) > 0
    ]

    return {
        **_base_options(),
        "title": {
            "text": "Drill holes by lithium best-intercept category",
            "left": "left",
            "textStyle": {"color": THEME["text_primary"], "fontSize": 14, "fontWeight": "normal"},
        },
        "legend": {
            "orient": "vertical",
            "right": 10,
            "top": "center",
            "textStyle": {"color": THEME["text_secondary"]},
        },
        "series": [{
            "name": "Category",
            "type": "pie",
            "radius": ["45%", "70%"],
            "center": ["35%", "55%"],
            "data": data,
            "label": {
                "color": THEME["text_secondary"],
                "formatter": "{b}: {c} ({d}%)",
            },
            "labelLine": {"lineStyle": {"color": THEME["text_tertiary"]}},
        }],
    }


# ---- Chart 3: Lithium price 5-year trend ----

def chart_lithium_price() -> dict:
    df = load_market_lithium()
    return {
        **_base_options(),
        "title": {
            "text": "Battery-grade lithium carbonate (LCE) — annual average",
            "subtext": "USD per metric ton, global benchmark",
            "left": "left",
            "textStyle": {"color": THEME["text_primary"], "fontSize": 14, "fontWeight": "normal"},
            "subtextStyle": {"color": THEME["text_tertiary"], "fontSize": 11},
        },
        "grid": {"left": "5%", "right": "5%", "top": "20%", "bottom": "10%", "containLabel": True},
        "xAxis": {
            "type": "category",
            "data": df["year"].astype(str).tolist(),
            "axisLine": {"lineStyle": {"color": THEME["text_tertiary"]}},
            "axisLabel": {"color": THEME["text_secondary"]},
        },
        "yAxis": {
            "type": "value",
            "name": "USD/t",
            "nameTextStyle": {"color": THEME["text_tertiary"]},
            "splitLine": {"lineStyle": {"color": THEME["grid_subtle"]}},
            "axisLabel": {
                "color": THEME["text_secondary"],
                "formatter": "{value}",
            },
        },
        "series": [{
            "name": "LCE price",
            "type": "line",
            "smooth": True,
            "data": df["price_usd_per_t"].tolist(),
            "lineStyle": {"color": THEME["accent_cyan"], "width": 3},
            "itemStyle": {"color": THEME["accent_cyan"]},
            "areaStyle": {
                "color": {
                    "type": "linear", "x": 0, "y": 0, "x2": 0, "y2": 1,
                    "colorStops": [
                        {"offset": 0, "color": "rgba(61, 217, 214, 0.4)"},
                        {"offset": 1, "color": "rgba(61, 217, 214, 0.0)"},
                    ],
                }
            },
        }],
    }


# ---- Chart 4: Boron price 5-year trend ----

def chart_boron_price() -> dict:
    df = load_market_boron()
    return {
        **_base_options(),
        "title": {
            "text": "Boric acid — annual average",
            "subtext": "USD per metric ton, European benchmark",
            "left": "left",
            "textStyle": {"color": THEME["text_primary"], "fontSize": 14, "fontWeight": "normal"},
            "subtextStyle": {"color": THEME["text_tertiary"], "fontSize": 11},
        },
        "grid": {"left": "5%", "right": "5%", "top": "20%", "bottom": "10%", "containLabel": True},
        "xAxis": {
            "type": "category",
            "data": df["year"].astype(str).tolist(),
            "axisLine": {"lineStyle": {"color": THEME["text_tertiary"]}},
            "axisLabel": {"color": THEME["text_secondary"]},
        },
        "yAxis": {
            "type": "value",
            "name": "USD/t",
            "nameTextStyle": {"color": THEME["text_tertiary"]},
            "splitLine": {"lineStyle": {"color": THEME["grid_subtle"]}},
            "axisLabel": {"color": THEME["text_secondary"]},
        },
        "series": [{
            "name": "Boric acid price",
            "type": "line",
            "smooth": True,
            "data": df["price_usd_per_t"].tolist(),
            "lineStyle": {"color": THEME["accent_gold"], "width": 3},
            "itemStyle": {"color": THEME["accent_gold"]},
            "areaStyle": {
                "color": {
                    "type": "linear", "x": 0, "y": 0, "x2": 0, "y2": 1,
                    "colorStops": [
                        {"offset": 0, "color": "rgba(255, 181, 71, 0.4)"},
                        {"offset": 1, "color": "rgba(255, 181, 71, 0.0)"},
                    ],
                }
            },
        }],
    }


# ---- Chart 5: EU context — Lopare LCE vs. EU annual demand ----
# Two separate visuals because of the 31x scale difference; charting them together
# requires log scale which is confusing for investor audiences.

def chart_eu_demand_bars() -> dict:
    """Two bars: EU annual demand 2030 vs. CRMA extraction target."""
    ctx = load_eu_context()
    return {
        **_base_options(),
        "title": {
            "text": "EU lithium landscape (2030 baseline)",
            "subtext": "Annual values, LCE basis (kilotonnes)",
            "left": "left",
            "textStyle": {"color": THEME["text_primary"], "fontSize": 14, "fontWeight": "normal"},
            "subtextStyle": {"color": THEME["text_tertiary"], "fontSize": 11},
        },
        "grid": {"left": "5%", "right": "5%", "top": "22%", "bottom": "10%", "containLabel": True},
        "xAxis": {
            "type": "category",
            "data": [
                "EU annual demand 2030",
                "CRMA extraction target (10%)",
                "Current EU extraction (est.)",
            ],
            "axisLine": {"lineStyle": {"color": THEME["text_tertiary"]}},
            "axisLabel": {"color": THEME["text_secondary"], "interval": 0,
                          "fontSize": 11, "lineHeight": 14, "width": 100, "overflow": "break"},
        },
        "yAxis": {
            "type": "value",
            "name": "kilotonnes LCE/year",
            "nameTextStyle": {"color": THEME["text_tertiary"]},
            "splitLine": {"lineStyle": {"color": THEME["grid_subtle"]}},
            "axisLabel": {"color": THEME["text_secondary"]},
        },
        "series": [{
            "name": "kt LCE/year",
            "type": "bar",
            "data": [
                {"value": ctx["eu_demand_2030_lce_kt_per_year"],
                 "itemStyle": {"color": THEME["accent_cyan"]}},
                {"value": ctx["eu_demand_2030_lce_kt_per_year"] * ctx["crma_extraction_target_pct"] / 100,
                 "itemStyle": {"color": THEME["accent_gold"]}},
                {"value": ctx["eu_current_extraction_lce_kt_per_year"],
                 "itemStyle": {"color": THEME["accent_blue"]}},
            ],
            "label": {
                "show": True,
                "position": "top",
                "color": THEME["text_secondary"],
                "formatter": "{c} kt",
            },
            "barWidth": "50%",
        }],
    }
