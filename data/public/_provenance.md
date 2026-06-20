# Data Provenance — Lopare Investor Snapshot

**Snapshot date:** 2026-06-19
**Update policy:** Point-in-time snapshot, no continuous updates planned
**Export variant:** A (MRE-derived B₂O₃ thresholds)

## Source

- **Repository:** `geomatrix_lopare` (ARCore-internal DD app, private)
- **Export script:** `tools/export_to_investor.py`
- **Underlying authoritative source:** CSA Global Pty Ltd, "ARC Core Lopare
  Boron-Lithium Project — Mineral Resource Estimate", Report R268.2022,
  30 July 2022. Author: Michael Cronwright.

## Files in this snapshot

| File | SHA-256 |
|------|---------|
| `collars_categorized.parquet` | `dac474ce8414126665dd8ebc7f603f73121ff672379bebf5c65646f0ee85b192` |
| `concession_lopare.geojson` | `a650bada3148516b8a0351a9d39d40e3415fc09b207dccc88acff108cf1369fe` |
| `methodology.md` | `f2a21588557484431f020f55908d5a44bee2f92cc85e91f8cd1effb451e11893` |

## Hole-ID pseudonymization

Real operational hole IDs (`ARC20DD001`, `LOP_001`, etc.) are mapped to
year-based pseudonyms (`2020-01`, `pre-01`, etc.) in this export. The
mapping file (`hole_id_mapping.parquet`) lives **exclusively in the DD repo**
and is never transferred here.

## Methodology

See `methodology.md` for cut-off thresholds, conversion factors, and
categorization rules.
