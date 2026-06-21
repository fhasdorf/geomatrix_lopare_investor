"""Public — Investor Dashboard. Phase 5: Charts, KPIs, EU context."""

import pandas as pd
import streamlit as st
from streamlit_echarts import st_echarts

from app._charts import (
    chart_boron_price,
    chart_eu_demand_bars,
    chart_li_category_pie,
    chart_lithium_price,
    chart_program_overview,
)
from app._data import RESOURCE_SNAPSHOT, load_eu_context
from app._i18n import init_lang, render_lang_toggle
from app._theme import inject_theme

st.set_page_config(page_title="Dashboard — Lopare", layout="wide")
inject_theme()
init_lang()
render_lang_toggle()

# ----- Hero / KPI Strip -----
st.markdown("# Investor Dashboard")
st.caption(
    "Resource highlights, drill program structure, and the European market "
    "context for lithium and boron."
)

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Mineral Resource", f"{RESOURCE_SNAPSHOT['total_mt']:,} Mt")
k2.metric("Avg. Li₂O grade", f"{RESOURCE_SNAPSHOT['avg_li2o_ppm']} ppm")
k3.metric("Avg. B₂O₃ grade", f"{RESOURCE_SNAPSHOT['avg_b2o3_pct']}%")
k4.metric("Licensed area", f"{RESOURCE_SNAPSHOT['concession_km2']} km²")

st.caption(
    f"Source: {RESOURCE_SNAPSHOT['source']}. "
    f"B-rich subtotal: {RESOURCE_SNAPSHOT['boron_subtotal_mt']} Mt at "
    f"{RESOURCE_SNAPSHOT['boron_subtotal_grade_pct']}% B₂O₃."
)

st.divider()

# ----- Drill Program Section -----
st.markdown("## Drill program structure")
col1, col2 = st.columns([3, 2])
with col1:
    st_echarts(options=chart_program_overview(), height="420px")
with col2:
    st_echarts(options=chart_li_category_pie(), height="420px")

st.caption(
    "Categories reflect the highest single-sample assay grade observed within "
    "each hole. See Disclaimer for full methodology and cut-off thresholds."
)

st.divider()

# ----- European Market Context -----
ctx = load_eu_context()
st.markdown("## European market context")

st.markdown(
    f"Lopare's in-situ lithium content — calculated from MRE figures — is "
    f"approximately **{ctx['lopare_lce_mt']:.2f} Mt LCE**. Against the "
    f"European Commission's 2030 baseline demand projection of "
    f"**{ctx['eu_demand_2030_lce_kt_per_year']} kt LCE per year**, this is "
    f"equivalent to roughly **"
    f"{ctx['lopare_lce_mt'] * 1000 / ctx['eu_demand_2030_lce_kt_per_year']:.0f} years**"
    f" of EU lithium demand at official baseline assumptions. Industry "
    f"forecasts (e.g. Fastmarkets) project higher demand scenarios, in which "
    f"this coverage is correspondingly lower."
)

st_echarts(options=chart_eu_demand_bars(), height="360px")

st.caption(
    f"EU demand baseline: {ctx['eu_demand_2030_source']}. "
    "CRMA: Regulation (EU) 2024/1252 establishes a 2030 target of 10% "
    "domestic extraction, 40% domestic processing, and 25% recycling of "
    "strategic raw materials."
)

st.markdown(
    f"On the boron side, the European Union is approximately "
    f"**{ctx['eu_boron_import_dependency_pct']}% import-dependent** — "
    f"primarily from Türkiye (Eti Maden). Boron is a CRMA-listed critical "
    f"raw material with applications in energy storage, wind technology, "
    f"and specialty glass."
)

st.divider()

# ----- Commodity Prices -----
st.markdown("## Commodity prices — five-year context")
col_li, col_b = st.columns(2)
with col_li:
    st_echarts(options=chart_lithium_price(), height="340px")
    st.caption(
        "Lithium prices reflect cyclical inventory dynamics; the 2022 peak and "
        "subsequent correction reflect upstream supply expansions catching up "
        "with surging EV demand. Structural demand growth continues to be "
        "driven by EV adoption and grid storage. Sources: Trading Economics, "
        "Intratec, USGS."
    )
with col_b:
    st_echarts(options=chart_boron_price(), height="340px")
    st.caption(
        "Boric acid prices show steady, low-volatility growth driven by stable "
        "demand from glass, ceramics, agriculture, and emerging electronics "
        "applications. Concentrated supply (Türkiye, USA) supports pricing "
        "discipline. Sources: USGS Mineral Commodity Summaries, Intratec."
    )

st.divider()

# ----- Peer Context -----
st.markdown("## Peer context — sediment-hosted lithium projects")

peer_data = pd.DataFrame([
    {"Project": "Lopare",          "Country": "Bosnia and Herzegovina",
     "Stage": "Mineral Resource (CSA Global)", "In-situ LCE (Mt)": 1.83, "Boron co-product": "Yes"},
    {"Project": "Rhyolite Ridge",  "Country": "Nevada, USA",
     "Stage": "Construction approved", "In-situ LCE (Mt)": 7.7, "Boron co-product": "Yes"},
    {"Project": "Thacker Pass",    "Country": "Nevada, USA",
     "Stage": "Under construction", "In-situ LCE (Mt)": 13.7, "Boron co-product": "No"},
])
st.dataframe(peer_data, use_container_width=True, hide_index=True)
st.caption(
    "Comparison limited to sediment-hosted lithium projects with completed "
    "resource estimates. In-situ LCE figures are derived from publicly available "
    "resource statements; methodologies and cut-offs differ between projects. "
    "The presence of boron as a co-product is a Lopare/Rhyolite Ridge "
    "characteristic; Thacker Pass is included as a pure-Li sediment-hosted peer."
)

st.divider()

# ----- Sources -----
st.markdown("## Data sources")
sources_md = "\n".join(
    f"- [{s['label']}]({s['url']})" for s in ctx["sources"]
)
sources_md += (
    f"\n- CSA Global Pty Ltd, Report R268.2022, 30 July 2022 "
    f"(Mineral Resource Estimate, primary source for drill data and resource numbers)"
)
st.markdown(sources_md)

st.caption(
    f"Market data snapshot as of {ctx['snapshot_date']}. Lithium and boron "
    "price series reflect annual averages; intra-year volatility is significant. "
    "This dashboard is a point-in-time presentation and is not updated continuously."
)
