"""CSS theme injection for the Lopare Investor app.

Glassmorphism polish on top of the Dunkelblau-Tech base. CSS variables make
color tweaks easy — change a single :root value and the whole app shifts.

Streamlit selectors used here ([data-testid=...]) are stable as of Streamlit
1.43. If they break after an upgrade, check Streamlit's release notes and
update the selectors below.
"""

import streamlit as st


_THEME_CSS = """
<style>
/* ---------- Font import ---------- */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;600;700&display=swap');

/* ---------- Design tokens ---------- */
:root {
    --bg-deep: #0A1628;
    --bg-card: rgba(20, 40, 71, 0.45);
    --bg-sidebar: rgba(10, 22, 40, 0.92);
    --accent-cyan: #3DD9D6;
    --accent-gold: #FFB547;
    --accent-light-blue: #7DA7D9;
    --text-primary: #F0F4F8;
    --text-secondary: #C5D2DC;
    --text-tertiary: #7DA7D9;
    --border-subtle: rgba(61, 217, 214, 0.15);
    --border-emphasis: rgba(61, 217, 214, 0.35);
}

/* ---------- App background with subtle radial gradients ---------- */
[data-testid="stApp"] {
    background:
        radial-gradient(ellipse 90% 70% at 0% 0%, rgba(61, 217, 214, 0.08), transparent 55%),
        radial-gradient(ellipse 80% 60% at 100% 100%, rgba(255, 181, 71, 0.05), transparent 55%),
        var(--bg-deep);
    background-attachment: fixed;
}

/* ---------- Hide Streamlit's default header chrome ---------- */
[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stToolbar"] {
    right: 1rem;
}

/* ---------- Typography ---------- */
html, body, [data-testid="stApp"] {
    font-family: 'Inter', sans-serif;
    color: var(--text-secondary);
}

h1 {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    letter-spacing: -0.025em;
    color: var(--text-primary);
}

h2, h3 {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
    letter-spacing: -0.015em;
    color: var(--text-primary);
}

[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li {
    font-family: 'Inter', sans-serif;
    color: var(--text-secondary);
    line-height: 1.65;
}

[data-testid="stMarkdownContainer"] strong {
    color: var(--text-primary);
}

/* st.caption renders inside this container — make it the secondary blue */
[data-testid="stCaptionContainer"] {
    color: var(--text-tertiary) !important;
    font-family: 'Inter', sans-serif;
}

/* Fallback for small tags in markdown */
small {
    color: var(--text-tertiary);
}

/* ---------- Dividers ---------- */
hr,
[data-testid="stDivider"] hr {
    border-color: var(--border-subtle);
    border-style: solid;
}

/* ---------- KPI Tiles (st.metric) — Glassmorphism ---------- */
[data-testid="stMetric"] {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    padding: 18px 20px;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    transition: border-color 180ms ease, transform 180ms ease;
}

[data-testid="stMetric"]:hover {
    border-color: var(--border-emphasis);
    transform: translateY(-1px);
}

[data-testid="stMetricLabel"] {
    font-family: 'Inter', sans-serif;
    font-size: 12px;
    font-weight: 500;
    color: var(--text-tertiary);
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

[data-testid="stMetricValue"] {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 30px;
    font-weight: 600;
    color: var(--text-primary);
    line-height: 1.2;
}

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"] {
    background: var(--bg-sidebar);
    border-right: 1px solid var(--border-subtle);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
    color: var(--text-secondary);
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: var(--text-primary);
}

/* Radio button group (Color-by, Tile style) */
[data-testid="stSidebar"] [data-testid="stRadio"] label {
    color: var(--text-secondary);
}

/* ---------- Map iframe container ---------- */
.element-container iframe {
    border-radius: 12px;
    border: 1px solid var(--border-subtle);
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.2);
}

/* ---------- Streamlit's built-in alert boxes (st.info, st.warning) ---------- */
[data-testid="stAlert"] {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 10px;
    backdrop-filter: blur(6px);
    -webkit-backdrop-filter: blur(6px);
}

/* ---------- Tables (st.dataframe, st.table) ---------- */
[data-testid="stTable"] table,
[data-testid="stDataFrame"] {
    font-family: 'Inter', sans-serif;
    font-size: 13px;
}

/* ---------- Links ---------- */
a {
    color: var(--accent-cyan);
    text-decoration: none;
    border-bottom: 1px solid transparent;
    transition: border-color 150ms ease;
}

a:hover {
    border-bottom-color: var(--accent-cyan);
}
</style>
"""


def inject_theme() -> None:
    """Inject the full CSS theme. Idempotent — safe to call on every page."""
    st.markdown(_THEME_CSS, unsafe_allow_html=True)
