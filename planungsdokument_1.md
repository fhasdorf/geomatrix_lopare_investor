# Planungsdokument: Lopare Investor-App (`geomatrix_lopare_investor`)
*Stand: 19.06.2026 — Technische Umsetzungs-Roadmap. Begleitend zu `_briefing_investor_app_2026-06-19.md` (nicht-technische Klärungen).*

---

## 1. Architektur-Übersicht

```
┌────────────────────────────────────────────────────────────────┐
│ geomatrix_lopare (intern, DD-App)                              │
│   └── data/processed/   ← Roh-Assays, Konzession, Collars     │
│                                                                │
│                       ↓ tools/export_to_investor.py            │
│                       ↓ (manuelle Pipeline mit Stop-Gates)    │
│                                                                │
│ geomatrix_lopare_investor (NEU, public-facing)                │
│   └── data/public/      ← kategorisierte, gerundete Files     │
│                                                                │
└────────────────────────────────────────────────────────────────┘
                       ↓ Streamlit Cloud
                       ↓
              ┌────────────────────┐
              │ Custom Domain      │  z.B. invest.lopare-project.com
              │ (ARCore-Branding)  │
              └────────────────────┘

geomatrix_core (Sibling-Repo, von beiden Apps genutzt)
   ├── maps/    (Folium-Helper, CRS, Polygon-Loader)
   ├── ui/      (Theme, Card-Komponenten)
   └── charts/  (Echarts-Wrapper, NEU für Investor-App)
```

**Entwurfsprinzipien:**
- **Code-Isolation**: Investor-Repo enthält keinen einzigen Risk-Register-, DD-Report- oder Datenqualitäts-Code.
- **Daten-Isolation**: Investor-Repo enthält ausschließlich kategorisierte, gerundete, geprüfte Datenfiles. Keine rohen Assay-Werte, nirgends.
- **Shared Components**: Gemeinsame UI- und Map-Komponenten leben in `geomatrix_core`, beide Apps importieren sie.
- **Manuelle Datenfreigabe**: Export von DD- nach Investor-Repo läuft über ein dediziertes Skript mit Stop-Gates — nie automatisch.

---

## 2. Repo-Setup

### Repo-Struktur

```
geomatrix_lopare_investor/
├── README.md
├── pyproject.toml
├── requirements.txt
├── .gitignore
├── .streamlit/
│   ├── config.toml              # Dunkelblau-Tech-Theme
│   └── secrets.toml             # gitignored: access_secret, pitch_token, smtp_*
├── app/
│   ├── streamlit_app.py         # Entry-Point, Landing-Page
│   ├── _theme.py                # CSS-Injection für Polish
│   ├── _access.py               # Magic-Link-Auth-Logik
│   ├── _map_helpers.py          # Investor-spezifische Karten-Konfiguration
│   └── pages/
│       ├── 1_Project_Map.py     # public
│       ├── 2_Opportunity.py     # public
│       ├── 3_Dashboard.py       # gated
│       ├── 4_Contact.py         # public
│       └── 9_Disclaimer.py      # public
├── data/
│   └── public/
│       ├── concession_lopare.geojson         # 1:1 aus DD-Repo
│       ├── collars_categorized.parquet        # kategorisiert, ohne Gehalte
│       ├── assay_categories.parquet           # Best Intercept Cat. pro Hole
│       ├── market_prices_li.parquet           # Public-Marktdaten
│       └── market_prices_b.parquet
├── content/
│   ├── opportunity_de.md         # Story-Text (mehrsprachig vorbereitet)
│   ├── opportunity_en.md
│   ├── disclaimer_de.md
│   └── disclaimer_en.md
├── tools/
│   └── (keine Daten-Tools — Daten kommen aus DD-Repo)
└── tests/
    └── test_no_raw_grades.py    # CI-Check: keine Roh-Gehalte in data/public/
```

### Neuer Branch in `geomatrix_lopare` (DD-Repo)

```
geomatrix_lopare/
└── tools/
    └── export_to_investor.py    # NEU: Pipeline DD → Investor
```

### Neue Module in `geomatrix_core`

```
geomatrix_core/
├── charts/                       # NEU
│   ├── __init__.py
│   ├── echarts_base.py          # ECharts-Wrapper, Theme-Integration
│   ├── price_chart.py           # Wiederverwendbarer Preis-Chart
│   └── scenario_chart.py        # Bull/Base/Bear Renderer
└── ui/
    └── investor_theme.py         # NEU: Dunkelblau-Tech-Palette + CSS
```

---

## 3. Datenpipeline DD → Investor (kritischer Punkt)

### Konzept: Grade Categorization mit Kombi 1+3

Der Export-Schritt kategorisiert die rohen Assay-Werte in 4 Stufen, basierend auf:
- **Cut-off-Grade aus dem MRE** (Quelle 3 — falls bekannt und freigegeben)
- **Statistischer Verteilung im Dataset** (Quelle 1 — Quartile)

**Kategorisierungs-Logik** (in `tools/export_to_investor.py`):

```python
# Pseudocode — finale Schwellen mit ARCore validieren
def categorize_grade_li(grade_pct_li2o, cutoff_mre=0.5, q75=None, q90=None):
    if grade_pct_li2o < cutoff_mre:
        return "trace"          # unter MRE Cut-off
    elif grade_pct_li2o < q75:
        return "mineralized"    # Standard, über Cut-off
    elif grade_pct_li2o < q90:
        return "high_grade"     # Top 25%
    else:
        return "bonanza"        # Top 10%
```

Quartile werden einmalig aus dem Roh-Dataset berechnet und in einem **Methodology-Sheet** für ARCore dokumentiert (als interner Audit-Trail).

### Was wird exportiert (pro Datei)

**`concession_lopare.geojson`**: 1:1 aus DD-Repo, EPSG:4326, keine Änderung.

**`collars_categorized.parquet`** (eine Zeile pro Bohrloch):
```
hole_id              : str  (pseudonymisiert, z.B. "DH-001" statt "ARC21DD007")
year_drilled         : int
depth_m_rounded      : int  (gerundet auf 10m)
lon                  : float  (gerundet auf 4 Nachkommastellen, ~10m Präzision)
lat                  : float
campaign             : str  ("Historical" / "Recent")
```

**`assay_categories.parquet`** (eine Zeile pro Bohrloch + Element):
```
hole_id              : str
element              : str  ("Li" oder "B")
best_intercept_cat   : str  ("trace" / "mineralized" / "high_grade" / "bonanza")
intercept_length_m   : int  (gerundet auf 5m)
```

**Was NICHT exportiert wird:**
- ❌ Roh-Gehalte (% Li₂O, % B₂O₃)
- ❌ Survey-Daten (Down-Hole-Pfad)
- ❌ Original Hole-IDs
- ❌ Exakte Tiefen
- ❌ Probennummern, Labor-Codes

### Export-Skript: Stop-Gate-Pattern

```python
# tools/export_to_investor.py (in DD-Repo)

# Phase 1: Lade Rohdaten, berechne Schwellen, zeige Vorschau
# STOP — User muss Schwellen bestätigen

# Phase 2: Kategorisiere, runde, pseudonymisiere
# Schreibe in /tmp/investor_export/
# Zeige Diff-Report: Anzahl Bohrlöcher pro Kategorie

# STOP — User muss Diff-Report bestätigen

# Phase 3: CI-Check ausführen (test_no_raw_grades.py)
# Wenn pass: kopiere nach ../geomatrix_lopare_investor/data/public/
# Wenn fail: Abbruch mit Liste verdächtiger Felder

# STOP — User committet manuell im Investor-Repo
```

### CI-Check: `tests/test_no_raw_grades.py` (im Investor-Repo)

Läuft bei jedem Push automatisch:

```python
# Stellt sicher, dass kein numerischer Wert in den public Parquets
# wie ein realer Grade-Wert aussieht
def test_no_numeric_grade_columns():
    df = pd.read_parquet("data/public/assay_categories.parquet")
    forbidden_columns = ["li_pct", "b_pct", "li2o", "b2o3", "grade"]
    for col in df.columns:
        for forbidden in forbidden_columns:
            assert forbidden not in col.lower(), \
                f"Forbidden column found: {col}"

def test_only_categorical_values():
    df = pd.read_parquet("data/public/assay_categories.parquet")
    allowed = {"trace", "mineralized", "high_grade", "bonanza"}
    assert set(df["best_intercept_cat"].unique()).issubset(allowed)
```

Das ist die letzte Sicherheitsleine, falls beim Export-Skript etwas schiefläuft.

---

## 4. Page-Konzepte

### 4.1 Landing (`streamlit_app.py`) — public

**Above the fold:**
- Hero-Bereich: Full-Width-Hintergrund (Drohnenbild oder Map-Render), Gradient-Overlay nach unten
- H1: *"Lopare — Strategic Lithium & Boron Project in the EU's Doorstep"*
- Subline: *"87.7 km² licensed exploration area · 70+ drill holes · CRMA-aligned commodities"*
- 2 CTAs: `Explore the project` (scrollt nach unten) / `Request investor briefing` (springt zu Contact)

**Below the fold (in scrollendem Format):**
- 4 KPI-Tiles als Glassmorphism-Cards:
  - Licensed area: 87.7 km²
  - Drill program: 70+ holes
  - Primary commodities: Li · B
  - Jurisdiction: Bosnia & Herzegovina (EU candidate)
- One-Liner Investment Thesis
- 3-Spalten "Why Lopare":
  - *EU-aligned supply* (CRMA)
  - *Multi-commodity upside* (Li + B + co-products)
  - *Advanced exploration stage* (NI 43-101 / JORC-konformer MRE, falls verfügbar)
- Footer mit Disclaimer-Teaser

### 4.2 Project Map (`pages/1_Project_Map.py`) — public

- **Folium-Karte** (Dark + Satellit Toggle, wie in DD-App)
- Concession-Polygon: gold-Outline (`#FFB547`), niedrige Fill-Opacity
- Bohrlöcher als Circle-Marker:
  - Farbe und Größe gemäß `best_intercept_cat` (Trace → klein-grau, Mineralized → mittel-cyan, High-grade → groß-gelb, Bonanza → groß-gold mit Glow)
  - Click-Popup: pseudonymisierte Hole-ID, Jahr, gerundete Tiefe, Best Intercept Category
- Layer-Toggle: Bohrlöcher nach Element (Li / B / kombiniert)
- Legende rechts unten
- Side-Panel links: kurze Erklärung der Kategorien (Methodology-Link → führt zum Disclaimer-Tab)

### 4.3 Opportunity (`pages/2_Opportunity.py`) — public

Story-Page, Markdown-getrieben aus `content/opportunity_en.md`. Strukturiert in 4 Sektionen mit Visualisierungs-Einsprengseln:

**§1 The Lithium-Boron Thesis**
- Markdown-Text
- Embedded Echart: Lithium price 2020–today

**§2 Why the EU Needs Lopare**
- Markdown-Text mit Verweis auf CRMA
- Embedded Echart: EU Battery Demand Forecast 2025–2035

**§3 The Lopare Advantage**
- Markdown-Text
- Embedded Karte: Mini-Map mit Lopare-Pin und Distanzen zu Gigafactories

**§4 The Path Forward**
- Markdown-Text mit Roadmap (Exploration → PFS → ESIA → FS → Construction)
- Timeline-Komponente (Echart oder einfache CSS-Timeline)

### 4.4 Dashboard (`pages/3_Dashboard.py`) — **gated**

Erst sichtbar nach `_access.has_access()` Check. Sonst Redirect auf Contact-Page mit Hinweis "Request access".

**Block A — Market Context:**
- Echart: Lithium-Carbonate price, 5 Jahre, mit "Today"-Marker
- Echart: Boron / Borax price, 5 Jahre
- KPI-Tile: aktueller Spot-Preis, % vs. 12-Monats-Median

**Block B — Scenario Modeling:**
- 4 Slider in einer Sidebar: Li-Preis, B-Preis, Recovery Rate, Annual Production
- Preset-Buttons: `Bull` / `Base` / `Bear`
- Output:
  - Echart Waterfall: Revenue Bull / Base / Bear
  - Echart Donut: Revenue-Mix Li vs. B
  - KPI-Tiles: implizierter Revenue, Margin-Range
- Großer Disclaimer-Hinweis unter den Charts

**Block C — Comparable Projects:**
- Tabelle mit 4–6 vergleichbaren EU-Lithium-Projekten
- Spalten: Project, Country, Stage, Resource (falls public), Market Cap (live über kleine API), Status
- Lopare-Zeile hervorgehoben

**Block D — Drill Program at a Glance:**
- Echart Bar: Anzahl Intercepts pro Kategorie (Bonanza / High-grade / Mineralized / Trace)
- Echart Bar: Verteilung über Kampagnen-Jahre
- Tile: Total drill meters

### 4.5 Contact (`pages/4_Contact.py`) — public, mit Lead-Capture

Zwei Formulare auf einer Seite:

**A — Quick Inquiry** (kein Access-Request):
- Name, Email, Message
- Sendet Email an ARCore-Inbox
- Bestätigung "We'll get back to you within 2 business days"

**B — Request Investor Access** (Magic-Link-Generierung):
- Name, Firma, Email, Investor-Type (Family Office / Fund / Strategic / Other)
- On Submit:
  1. Generiere Magic-Link-Token (UUID + HMAC mit `access_secret`)
  2. Speichere in `lead_log.jsonl` (gitignored, lokal/persisted)
  3. Sende Email an User mit Link (24h gültig)
  4. Sende Notification-Email an ARCore mit Lead-Daten
  5. Zeige Bestätigung: "Check your inbox"

### 4.6 Disclaimer (`pages/9_Disclaimer.py`) — public

Volltext aus `content/disclaimer_en.md`. Sektionen:
- Methodology (insb. Grade Categorization Disclaimer)
- Data Sources
- Forward-Looking Statements
- No Offering Statement
- Privacy Policy
- Imprint (ARCore, Seaside, Geomatrix)

---

## 5. Access-Modell (Magic-Link-Auth)

### Mechanik

**`_access.py`** verwaltet drei Auth-Modi parallel:

1. **Pitch-Token via URL**:
```
   https://invest.lopare-project.com/?access=PITCH_TOKEN_HERE
```
   Wenn URL-Param `access` mit `st.secrets["pitch_token"]` matcht, Session sofort als authentifiziert markiert. Für Frank beim Live-Pitch.

2. **Magic-Link via Email**:
```
   https://invest.lopare-project.com/?token=<jwt_or_hmac_signed_token>
```
   Token enthält Email + Issued-At + Expiry. Bei Match: Session authentifiziert für 7 Tage (Streamlit-Session-Cookie).

3. **Session-State** (innerhalb des Browsers):
   Einmal authentifiziert, bleibt `session_state["access_granted"] = True` bis der Tab geschlossen wird.

### Was wir NICHT brauchen

- Keine User-Datenbank (Tokens sind self-contained mit HMAC-Signatur)
- Kein Passwort-Reset-Flow
- Kein Logout (Tab schließen reicht)
- Keine 2FA (Investor-App ist Teaser, nicht Data Room)

### Email-Versand

**SMTP via `st.secrets`** (z.B. SendGrid Free Tier, 100 Mails/Tag — reicht für Investor-Volumen):
```toml
[smtp]
host = "smtp.sendgrid.net"
port = 587
user = "apikey"
password = "..."
from_address = "noreply@lopare-project.com"
notify_address = "investors@arcore.ba"
```

Alternativ Resend.com (modernere DX) oder einfach Gmail-SMTP für die ersten Wochen.

### Token-Implementierung (sketch)

```python
import hmac, hashlib, json, base64, time

def generate_magic_link(email: str, secret: str, ttl_hours: int = 24) -> str:
    payload = {"email": email, "exp": int(time.time()) + ttl_hours * 3600}
    payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()
    sig = hmac.new(secret.encode(), payload_b64.encode(), hashlib.sha256).hexdigest()
    return f"{payload_b64}.{sig}"

def verify_token(token: str, secret: str) -> dict | None:
    try:
        payload_b64, sig = token.split(".")
        expected_sig = hmac.new(secret.encode(), payload_b64.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(sig, expected_sig):
            return None
        payload = json.loads(base64.urlsafe_b64decode(payload_b64))
        if payload["exp"] < time.time():
            return None
        return payload
    except Exception:
        return None
```

---

## 6. Visual Layer: Dunkelblau-Tech-Theme

### Streamlit-Konfiguration

**`.streamlit/config.toml`**:
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

### CSS-Injection (`app/_theme.py`)

Lädt Google Fonts (`Space Grotesk`, `Inter`, `JetBrains Mono`), überschreibt Streamlit-Defaults:
- Hero-Section mit Background-Image-Slot + Gradient-Overlay
- Card-Komponente (Glassmorphism: `backdrop-filter: blur(8px)`, subtle border)
- KPI-Tile-Komponente
- CTA-Button-Style (cyan glow on hover)
- Sidebar-Polish

CSS wird per `st.markdown(<style>...</style>, unsafe_allow_html=True)` injiziert, einmal in `streamlit_app.py` und einmal pro Page (Streamlit-Reset).

Konkretes CSS kommt in Phase 4 — zu früh hier ist Premature Detail.

### Echarts-Theme

**`geomatrix_core/charts/echarts_base.py`** liefert ein JSON-Theme mit der Dunkelblau-Tech-Palette für alle Charts:

```python
INVESTOR_THEME = {
    "backgroundColor": "transparent",
    "textStyle": {"fontFamily": "Inter, sans-serif", "color": "#F0F4F8"},
    "color": ["#3DD9D6", "#FFB547", "#4ADE80", "#F472B6", "#A78BFA"],
    "title": {"textStyle": {"fontFamily": "Space Grotesk", "color": "#F0F4F8"}},
    "grid": {"borderColor": "#1F3A5F"},
    "axisLine": {"lineStyle": {"color": "#7A8FA6"}},
    # ...
}
```

Alle Charts in der App registrieren dieses Theme einmalig, Konsistenz garantiert.

---

## 7. Dependencies

**`requirements.txt`**:
```
streamlit>=1.43
folium>=0.17
streamlit-folium>=0.22
streamlit-echarts>=0.4
pyecharts>=2.0
pandas>=2.0
geopandas>=0.14
pyarrow>=15.0
pyjwt>=2.8        # für Magic-Link-Tokens (alternativ self-rolled mit hmac)
geomatrix-core @ git+https://github.com/fhasdorf/geomatrix_core.git@investor-charts
-e .
```

Neu vs. DD-App: `streamlit-echarts`, `pyecharts`, `pyjwt`.
Entfallen vs. DD-App: `ezdxf`, `pdfplumber`, `pydeck`, `openpyxl` (alles DD-Tools).

---

## 8. Deployment

### Streamlit Cloud

- Repo: `geomatrix_lopare_investor` (GitHub, privat — auch wenn die App public ist, Code privat halten)
- Branch: `main` für Production
- Branch: `staging` für Test-Deployment (kostenlos zweites Deployment)
- Plan: **Teams-Plan nötig**, sobald Custom Domain gewünscht (~$20/Monat)

### Custom Domain

CNAME-Eintrag z.B. `invest.lopare-project.com` → `share.streamlit.io`. SSL-Cert automatisch via Streamlit.

### Secrets-Setup (Streamlit Cloud Dashboard)

```toml
pitch_token = "FRANK_PITCH_2026_XXXX"
access_secret = "HMAC_SECRET_KEY_LONG_RANDOM_STRING"

[smtp]
host = "..."
port = 587
user = "..."
password = "..."
from_address = "noreply@lopare-project.com"
notify_address = "investors@arcore.ba"
```

---

## 9. Umsetzungs-Phasen

### Phase 0 — Vorbereitung (parallel zu ARCore-Klärungen)

1. Repo `geomatrix_lopare_investor` auf GitHub anlegen (privat)
2. Repo `geomatrix_core` Branch `investor-charts` anlegen
3. Lokale Struktur nach Abschnitt 2 aufbauen
4. Streamlit Cloud-Account: zweites Deployment vorbereitet (noch ohne Domain)
5. SendGrid / Resend-Account anlegen, SMTP-Test

### Phase 1 — Datenpipeline (DD-seitig)

1. `tools/export_to_investor.py` in DD-Repo schreiben
2. Mit ARCore Schwellen für Kategorien validieren
3. Erstes Export-Run mit Stop-Gates
4. `tests/test_no_raw_grades.py` schreiben
5. Erste public Files in `data/public/` committen
6. **STOP-Gate**: Frank reviewt exportierte Files manuell vor Commit

### Phase 2 — Skelett + Theme

1. Streamlit-Skeleton mit Landing-Page (Lorem-Ipsum-Inhalt)
2. Theme-CSS (`_theme.py`) entwickeln, an Echtgerät testen
3. Folium-Karte mit kategorisierten Bohrlöchern (`pages/1_Project_Map.py`)
4. **Demo an ARCore**: nur Map und Hero, Feedback einholen

### Phase 3 — Public-Pages

1. Opportunity-Page (`pages/2_Opportunity.py`)
2. Contact-Page (`pages/4_Contact.py`, ohne Auth)
3. Disclaimer-Page (`pages/9_Disclaimer.py`)
4. Content-Markdown-Files (`content/*_en.md`) — vermutlich Initial-Draft durch Frank, Review durch ARCore

### Phase 4 — Access-Layer

1. `_access.py` mit Magic-Link-Logik
2. Email-Sending via SMTP
3. Lead-Logging (`lead_log.jsonl`)
4. Pitch-Token-Mechanik
5. Tests: Token generieren, verifizieren, abgelaufenen Token ablehnen

### Phase 5 — Gated Dashboard

1. `pages/3_Dashboard.py` mit Access-Check
2. Echarts-Komponenten in `geomatrix_core/charts/` entwickeln
3. Markt-Preisdaten beschaffen (Trading Economics CSV-Download oder USGS-API)
4. Scenario-Modeling-Logik (4 Slider → 3 Charts)
5. Comparable Projects: Recherche und Tabelle

### Phase 6 — Staging-Deployment

1. Push auf `staging`-Branch
2. Streamlit Cloud Staging-URL: kompletter End-to-End-Test
3. Test-Magic-Link an eigene Email
4. Test-Pitch-Token-URL
5. ARCore-Review-Termin

### Phase 7 — Production-Cutover

1. Anwaltliche Disclaimer-Freigabe (siehe Briefing Abschnitt B.2)
2. Custom Domain konfigurieren
3. Production-Secrets setzen
4. `main`-Branch push, Live-Test
5. ARCore freigibt offiziell
6. Lead-Capture-Workflow live (Email-Routing testen)
7. **Soft Launch**: erst an einen kleinen Investor-Kreis kommuniziert, eine Woche beobachten, dann breiter

---

## 10. Was dieses Dokument bewusst offen lässt

- **Konkretes CSS für Theme** — kommt in Phase 2 als Lieferartefakt
- **Content der Opportunity-Page** — strategischer Marketing-Inhalt, von Frank+ARCore geschrieben
- **Konkrete Bull/Base/Bear-Annahmen** — von ARCore zu liefern
- **Comparable Projects-Liste** — Recherche-Schritt, mit ARCore-Input
- **Custom Domain Name** — siehe Briefing Abschnitt A.4
- **Anwalt für Disclaimer** — siehe Briefing Abschnitt B.2
- **Drohnenfotos** — siehe Briefing Abschnitt D.5

---

## 11. Risiken & Mitigationen

| Risiko | Schweregrad | Mitigation |
|---|---|---|
| Roh-Gehalte landen versehentlich in Investor-Repo | **Hoch** | CI-Check (Test im Phase 1), manueller Review-Schritt im Export-Skript, gitignore-Pattern |
| Magic-Link-Token leakt (Email-Forwarding) | Mittel | TTL auf 24h begrenzt, kein Refresh, Audit-Log über Token-Usage |
| Streamlit Cloud Cold-Start beim Live-Pitch | Mittel | 5min vorm Pitch selbst öffnen ("Warm-up"); Backup-PDF parat |
| Investor erwartet Echtzeit-Daten, App zeigt veraltete | Mittel | "Last updated: YYYY-MM-DD" Marker auf jeder Daten-Page |
| Streamlit-Limitationen für hochwertigen Look | Mittel | CSS-Injection, externer Designer für Hero-Asset falls nötig |
| Compliance-Verstoß durch ungeprüfte Forward-Looking Statements | **Hoch** | Anwaltliche Freigabe vor Go-Live (Briefing B.2), Disclaimer prominent auf jeder Page mit Zahlen |
| ARCore-internes Veto nach Soft-Launch | Mittel | Soft Launch an kleinen Kreis vor breiter Kommunikation |

---

## 12. Definition of Done für Go-Live

- [ ] Alle Datenfreigaben aus Briefing-Abschnitt C grün
- [ ] Disclaimer anwaltlich geprüft und eingebunden
- [ ] CI-Check `test_no_raw_grades.py` grün
- [ ] Pitch-Token funktioniert
- [ ] Magic-Link via Email an externe Test-Adresse erfolgreich
- [ ] Custom Domain aktiv mit SSL
- [ ] ARCore-CEO oder gleichwertige Person hat die App durchgeklickt und schriftlich freigegeben
- [ ] Backup-PDF der Pitch-Inhalte vorbereitet
- [ ] Frank kann die App im Notfall in <5 Min auf Wartungsseite stellen

---

## Anhang: Referenzen

- Sachstand der DD-App: `_sachstand_2026-06-19.md`
- Nicht-technisches Briefing: `_briefing_investor_app_2026-06-19.md`
- DD-App-Handover (Modi-Switch, verworfen zugunsten getrenntes Repo): `_handover_investor_view_2026-06-19.md`
- Streamlit ECharts: https://github.com/andfanilo/streamlit-echarts
- EU Critical Raw Materials Act: https://single-market-economy.ec.europa.eu/sectors/raw-materials/areas-specific-interest/critical-raw-materials_en