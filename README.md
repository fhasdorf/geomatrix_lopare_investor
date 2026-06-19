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
