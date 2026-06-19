# Claude-Code-Briefing: Phase 0.3 — Lokales Skeleton für `geomatrix_lopare_investor`

**Stand:** 2026-06-19
**Repo:** `geomatrix_lopare_investor` (lokal: `E:\Code\geomatrix_lopare_investor`)
**Ziel:** Komplette Verzeichnisstruktur und lauffähiges Streamlit-Skeleton anlegen, sodass `streamlit run app/streamlit_app.py` eine 5-Seiten-App mit Dunkelblau-Tech-Theme und Platzhalter-Inhalten zeigt.

---

## Voraussetzungen (Frank prüft vor Start)

- [ ] Ordner ist umbenannt zu `E:\Code\geomatrix_lopare_investor`
- [ ] `planungsdokument_1.md` liegt im Ordner
- [ ] Python 3.11+ im venv verfügbar, aktiviert oder gleich neu anlegen
- [ ] Sibling-Repo `E:\Code\geomatrix_core` existiert (für späteren `-e`-Install)

---

## Aufgabe

Lege folgende Struktur an. **Verify-First**: nach jedem Block prüfe ich mit `tree` oder `ls`, dass alles passt, bevor ich weiter arbeite. Stop, wenn etwas unklar ist.

### 1. Verzeichnisstruktur

```
geomatrix_lopare_investor/
├── README.md
├── pyproject.toml
├── requirements.txt
├── .gitignore
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml.example       # Vorlage, gitignored
├── app/
│   ├── __init__.py
│   ├── streamlit_app.py
│   ├── _theme.py
│   ├── _access.py
│   ├── _map_helpers.py
│   └── pages/
│       ├── 1_Project_Map.py
│       ├── 2_Opportunity.py
│       ├── 3_Dashboard.py
│       ├── 4_Contact.py
│       └── 9_Disclaimer.py
├── content/
│   ├── opportunity_en.md
│   ├── opportunity_de.md
│   ├── disclaimer_en.md
│   └── disclaimer_de.md
├── data/
│   └── public/
│       └── .gitkeep
├── tools/
│   └── .gitkeep
└── tests/
    └── .gitkeep
```

**Wichtig:** `data/public/.gitkeep`, `tools/.gitkeep`, `tests/.gitkeep` als leere Files anlegen, damit die Ordner im Git landen. Inhalt für `data/public/` kommt in Phase 1, `tests/test_no_raw_grades.py` ebenfalls Phase 1.

### 2. File-Inhalte

#### `.gitignore`

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
.venv/
venv/
env/
.pytest_cache/
*.egg-info/
build/
dist/

# Streamlit
.streamlit/secrets.toml

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# App-Runtime
lead_log.jsonl
*.log

# Notebooks scratch
*.ipynb_checkpoints/
```

#### `pyproject.toml`

```toml
[project]
name = "geomatrix-lopare-investor"
version = "0.0.1"
description = "Lopare Project — Investor-facing Streamlit app (teaser + pitch companion)"
requires-python = ">=3.11"
readme = "README.md"
authors = [{ name = "Frank Hasdorf", email = "frank@geomatrix.consulting" }]

[tool.setuptools.packages.find]
where = ["."]
include = ["app*"]

[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"
```

#### `requirements.txt`

```
streamlit>=1.43
folium>=0.17
streamlit-folium>=0.22
streamlit-echarts>=0.4
pyecharts>=2.0
pandas>=2.0
geopandas>=0.14
pyarrow>=15.0
pyjwt>=2.8

# Lokal: editable Install des Sibling-Repos.
# Für Streamlit Cloud später ersetzen durch:
#   geomatrix-core @ git+https://github.com/fhasdorf/geomatrix_core.git@investor-charts
-e ../geomatrix_core

-e .
```

#### `.streamlit/config.toml`

```toml
[theme]
base = "dark"
primaryColor = "#3DD9D6"
backgroundColor = "#0A1628"
secondaryBackgroundColor = "#142847"
textColor = "#F0F4F8"
font = "sans serif"

[server]
headless = true
```

#### `.streamlit/secrets.toml.example`

```toml
# Kopiere zu .streamlit/secrets.toml und fülle vor Phase 4 aus.

pitch_token = "REPLACE_ME_PITCH_TOKEN"
access_secret = "REPLACE_ME_LONG_RANDOM_HMAC_SECRET"

[smtp]
host = "smtp.sendgrid.net"
port = 587
user = "apikey"
password = "REPLACE_ME"
from_address = "noreply@lopare-project.com"
notify_address = "investors@arcore.ba"
```

#### `README.md`

```markdown
# Lopare Project — Investor App

Public-facing Streamlit app for the Lopare lithium & boron exploration project (Bosnia & Herzegovina). Built for ARCore as a teaser and live-pitch companion.

**Status:** Phase 0 — Skeleton. Not yet deployed.

## Architecture

Separate repo from the internal DD app (`geomatrix_lopare`). Shares UI/map components via the sibling repo `geomatrix_core` (branch `investor-charts`). Data flows one-way through a manual export pipeline with stop-gates — no raw assay values ever reach this repo.

See `planungsdokument_1.md` for the full technical roadmap.

## Local development

```bash
python -m venv .venv
source .venv/Scripts/activate    # Git Bash on Windows
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

## Project structure

- `app/` — Streamlit pages and helpers
- `content/` — Markdown content (multilingual)
- `data/public/` — Categorized, rounded datasets (Phase 1 onwards)
- `tools/` — (empty; data tooling lives in DD repo)
- `tests/` — CI checks (Phase 1)

## Related repos

- `geomatrix_lopare` — internal DD app, source of truth for raw data
- `geomatrix_core` — shared library (maps, UI, charts)
```

#### `app/__init__.py`

Leer.

#### `app/streamlit_app.py`

```python
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
```

#### `app/_theme.py`

```python
"""Theme injection. Phase 0: stub. Phase 2: full CSS for glassmorphism, hero, cards."""

import streamlit as st


def inject_theme() -> None:
    """Inject custom CSS. Phase 0 = no-op placeholder."""
    # Phase 2 will inject Google Fonts (Space Grotesk, Inter, JetBrains Mono),
    # hero background, glassmorphism card styles, CTA button polish.
    st.markdown(
        "<!-- theme CSS placeholder — Phase 2 -->",
        unsafe_allow_html=True,
    )
```

#### `app/_access.py`

```python
"""Magic-Link access control. Phase 0: stub returns True for all (open access).
Phase 4 will implement HMAC-signed tokens, pitch-token URL param, session state."""

import streamlit as st


def has_access() -> bool:
    """Phase 0: always grant access. Phase 4 enforces real auth on gated pages."""
    return True


def require_access() -> None:
    """Call at top of gated pages. Phase 0: no-op."""
    if not has_access():
        st.warning("This area is gated. Request access on the Contact page.")
        st.stop()
```

#### `app/_map_helpers.py`

```python
"""Folium map helpers for the investor app. Phase 0: stub.
Phase 2 will implement the categorized-marker map with gold concession outline."""

# Will import from geomatrix_core.maps once Phase 2 starts.
```

#### `app/pages/1_Project_Map.py`

```python
"""Public — Project Map. Phase 0 placeholder."""

import streamlit as st

from app._theme import inject_theme

st.set_page_config(page_title="Project Map — Lopare", layout="wide")
inject_theme()

st.title("Project Map")
st.info("Folium map with concession polygon and categorized drill holes — coming in Phase 2.")
```

#### `app/pages/2_Opportunity.py`

```python
"""Public — Opportunity / Story. Phase 0 placeholder."""

from pathlib import Path

import streamlit as st

from app._theme import inject_theme

st.set_page_config(page_title="Opportunity — Lopare", layout="wide")
inject_theme()

content_path = Path(__file__).parents[2] / "content" / "opportunity_en.md"
if content_path.exists():
    st.markdown(content_path.read_text(encoding="utf-8"))
else:
    st.title("Opportunity")
    st.info("Story content coming in Phase 3.")
```

#### `app/pages/3_Dashboard.py`

```python
"""Gated — Investor Dashboard. Phase 0 placeholder, no auth yet."""

import streamlit as st

from app._access import require_access
from app._theme import inject_theme

st.set_page_config(page_title="Dashboard — Lopare", layout="wide")
inject_theme()
require_access()  # Phase 4 enforces real gate

st.title("Investor Dashboard")
st.warning(
    "Dashboard with market context, scenario modeling, comparables, and drill-program "
    "summary — coming in Phase 5. Access will be gated via Magic-Link in Phase 4."
)
```

#### `app/pages/4_Contact.py`

```python
"""Public — Contact and access request. Phase 0 placeholder."""

import streamlit as st

from app._theme import inject_theme

st.set_page_config(page_title="Contact — Lopare", layout="wide")
inject_theme()

st.title("Contact")
st.info("Quick-inquiry form and investor-access request — coming in Phase 3 and Phase 4.")
```

#### `app/pages/9_Disclaimer.py`

```python
"""Public — Disclaimer. Phase 0 placeholder, loads from content/disclaimer_en.md."""

from pathlib import Path

import streamlit as st

from app._theme import inject_theme

st.set_page_config(page_title="Disclaimer — Lopare", layout="wide")
inject_theme()

content_path = Path(__file__).parents[2] / "content" / "disclaimer_en.md"
if content_path.exists():
    st.markdown(content_path.read_text(encoding="utf-8"))
else:
    st.title("Disclaimer")
    st.info("Full disclaimer text coming in Phase 3, anwaltlich freigegeben vor Go-Live.")
```

#### `content/opportunity_en.md`

```markdown
# The Lopare Opportunity

*Placeholder — Story content to be drafted in Phase 3, reviewed by ARCore.*

## §1 The Lithium-Boron Thesis

Lorem ipsum dolor sit amet, consectetur adipiscing elit.

## §2 Why the EU Needs Lopare

Reference to CRMA.

## §3 The Lopare Advantage

Multi-commodity, EU-jurisdiction, advanced exploration stage.

## §4 The Path Forward

Exploration → PFS → ESIA → FS → Construction.
```

#### `content/opportunity_de.md`

```markdown
# Die Lopare-Opportunity

*Platzhalter — Story-Inhalt wird in Phase 3 erstellt, ARCore-Review.*
```

#### `content/disclaimer_en.md`

```markdown
# Disclaimer

*Placeholder — to be finalized with legal counsel before Go-Live.*

## Methodology

Drill-hole grades displayed on this site are categorized (Trace / Mineralized / High-grade / Bonanza), not numeric. Thresholds derived from a combination of the MRE cut-off grade and statistical quartiles of the underlying assay dataset.

## Data Sources

Public-facing data is derived from ARCore exploration campaigns 2020–2022 and the CSA Global MRE work. All sensitive values are categorized or rounded.

## Forward-Looking Statements

Lorem ipsum.

## No Offering Statement

This site does not constitute an offer or solicitation.

## Privacy Policy

Lorem ipsum.

## Imprint

ARCore Ulaganja d.o.o. · Seaside Capital Markets · Geomatrix Consulting (technical realization)
```

#### `content/disclaimer_de.md`

```markdown
# Disclaimer

*Platzhalter — vor Go-Live anwaltlich freigegeben.*
```

---

## Definition of Done

- [ ] Alle Files und Ordner aus Abschnitt 1 existieren
- [ ] `streamlit run app/streamlit_app.py` startet ohne Fehler
- [ ] Landing-Page zeigt Hero, 4 KPI-Tiles, "Why Lopare" Drei-Spalten
- [ ] Alle 5 Seiten in der Sidebar erreichbar (1_Project_Map, 2_Opportunity, 3_Dashboard, 4_Contact, 9_Disclaimer)
- [ ] Dunkelblau-Tech-Theme aktiv (Hintergrund `#0A1628`, Akzent `#3DD9D6`)
- [ ] `git init` ausgeführt, **aber** noch nicht committet — Frank macht ersten Commit manuell nach Review
- [ ] `.streamlit/secrets.toml` existiert NICHT (nur `.example`)

## Out of Scope für Phase 0.3

- ❌ Echte Daten in `data/public/` (Phase 1)
- ❌ `tests/test_no_raw_grades.py` (Phase 1)
- ❌ Vollständiges CSS-Theme (Phase 2)
- ❌ Echte Folium-Karte mit Bohrlöchern (Phase 2)
- ❌ Markdown-Content über Lorem-Ipsum hinaus (Phase 3)
- ❌ Magic-Link-Logik (Phase 4)
- ❌ Echarts-Komponenten (Phase 5)
- ❌ Push auf GitHub (Frank macht das nach Review)

---

## Stop-Gate

Nach Abschluss: zeige mir
1. Output von `tree /F` oder `ls -R`
2. Output von `streamlit run app/streamlit_app.py` Start (erste 10 Zeilen + URL)
3. Screenshot der Landing-Page (oder textuelle Beschreibung was du siehst)

Erst dann committen wir und starten Phase 1.
