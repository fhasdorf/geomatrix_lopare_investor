# Lopare Investor Data — Methodology

Generated: 2026-06-20 08:28
Source: ARCore Lopare DD database (CSA Global MRE Report R268.2022, Mineral Resource Estimate as of 30 July 2022)

## Categorization

Drill hole categories reflect the highest single-sample assay grade observed
within the hole ("best intercept"). Categories are derived from MRE-validated
cut-offs and reporting thresholds.

### Lithium (Li2O equivalent)

| Category    | Li2O range          | Li (element) range |
|-------------|---------------------|--------------------|
| Trace       | < 400 ppm           | < 186 ppm          |
| Mineralized | 400-600 ppm         | 186-279 ppm        |
| High-grade  | 600-1000 ppm        | 279-465 ppm        |
| Bonanza     | > 1000 ppm          | > 465 ppm          |
| Pending     | assay results pending |                  |

Cut-off `400 ppm Li2O` corresponds to the MRE reporting cut-off (CSA Global
R268.2022, Table 1). Conversion factor Li -> Li2O = x 2.153.

### Boron (B2O3 equivalent) — Variant A (MRE-derived thresholds)

| Category    | B2O3 range      | B (element) range |
|-------------|------------------|--------------------|
| Trace       | < 0.85%          | < 2640 ppm |
| Mineralized | 0.85-1.00%       | 2640-3106 ppm |
| High-grade  | 1.00-4.00%       | 3106-12423 ppm |
| Bonanza     | > 4.00%          | > 12423 ppm |
| Pending     | assay results pending |              |

Cut-offs follow CSA Global R268.2022 B2O3 reporting tiers. Conversion factor
B -> B2O3 = x 3.2202.

### Hole identifiers

Drill holes are presented with year-based identifiers (e.g. `2020-01`,
`2022-04`, `pre-01`) instead of operational hole IDs to preserve campaign
context while protecting detailed program structure.

## Data integrity

- Coordinates rounded to 5 decimal places (~1 m precision)
- No numeric assay values, sample counts, or depths are included in this export
- All categorical labels (Trace / Mineralized / High-grade / Bonanza / Pending)
  are deterministically derived from the MRE thresholds documented above

## Source
CSA Global Pty Ltd, "ARC Core Lopare Boron-Lithium Project — Mineral Resource
Estimate", Report R268.2022, 30 July 2022. Author: Michael Cronwright.
