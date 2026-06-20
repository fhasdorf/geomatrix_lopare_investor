"""CI guard: ensures no raw assay grades, statistics, or operational hole IDs
leak into the investor repo's data/public/ directory.

This test is the last line of defense. The first line is the .gitignore.
The second line is the export pipeline in the DD repo
(tools/export_to_investor.py), which only writes categorized data.

If this test ever fails: STOP, do not commit, do not push. The DD pipeline
or the manual transfer step has broken its contract.
"""

from __future__ import annotations

import re
import json
from pathlib import Path

import geopandas as gpd
import pandas as pd
import pytest

PUBLIC_DIR = Path(__file__).parent.parent / "data" / "public"

# Spaltennamen-Muster, die auf Roh-Werte oder Statistiken hindeuten.
SUSPICIOUS_COLUMN_PATTERNS = [
    re.compile(r"(?i)_ppm$"),
    re.compile(r"(?i)_pct$"),
    re.compile(r"(?i)_mean$"),
    re.compile(r"(?i)_median$"),
    re.compile(r"(?i)_min$"),
    re.compile(r"(?i)_max$"),
    re.compile(r"(?i)_count$"),
    re.compile(r"(?i)_std$"),
    re.compile(r"(?i)^Li_(?!category$)"),   # Li_anything außer li_category
    re.compile(r"(?i)^B_(?!category$)"),    # B_anything außer b_category
    re.compile(r"(?i)Li2O"),
    re.compile(r"(?i)B2O3"),
    re.compile(r"(?i)easting"),
    re.compile(r"(?i)northing"),
    re.compile(r"(?i)dist_to_boundary"),
    re.compile(r"(?i)typo_fix"),
    re.compile(r"(?i)Hole_ID$"),            # echte Hole-IDs, nur pseudo_id erlaubt
]

# Spalten, die explizit erlaubt sind (Whitelist-Override).
ALLOWED_COLUMNS = {
    "pseudo_id",
    "year_bucket",
    "lon_wgs84",
    "lat_wgs84",
    "li_category",
    "b_category",
}

# Erlaubte Kategorien-Werte. Alles andere ist verdächtig (z.B. numerische Werte).
ALLOWED_CATEGORY_VALUES = {
    "Trace", "Mineralized", "High-grade", "Bonanza", "Pending", "n/a",
}

# Lopare liegt in BiH bei ~18.8°E, ~44.6°N. Werte außerhalb dieser Box sind verdächtig.
LOPARE_LON_RANGE = (18.0, 19.5)
LOPARE_LAT_RANGE = (44.0, 45.5)


def _public_parquets() -> list[Path]:
    return sorted(PUBLIC_DIR.glob("*.parquet"))


def test_public_dir_exists():
    assert PUBLIC_DIR.exists(), f"data/public/ directory missing at {PUBLIC_DIR}"


def test_expected_files_present():
    """Snapshot file inventory check."""
    expected = {
        "collars_categorized.parquet",
        "concession_lopare.geojson",
        "methodology.md",
    }
    present = {p.name for p in PUBLIC_DIR.iterdir() if p.is_file()}
    missing = expected - present
    assert not missing, f"Missing files in data/public/: {missing}"


@pytest.mark.parametrize("parquet_file", _public_parquets(), ids=lambda p: p.name)
def test_no_suspicious_columns(parquet_file: Path):
    """No column name should match a 'raw data' pattern."""
    df = pd.read_parquet(parquet_file)
    violations = []
    for col in df.columns:
        if col in ALLOWED_COLUMNS:
            continue
        for pattern in SUSPICIOUS_COLUMN_PATTERNS:
            if pattern.search(col):
                violations.append((col, pattern.pattern))
                break
    assert not violations, (
        f"{parquet_file.name} contains suspicious columns:\n"
        + "\n".join(f"  - '{col}' matched pattern '{pat}'" for col, pat in violations)
    )


@pytest.mark.parametrize("parquet_file", _public_parquets(), ids=lambda p: p.name)
def test_no_unexpected_numeric_columns(parquet_file: Path):
    """The only allowed numeric columns are geo coordinates."""
    df = pd.read_parquet(parquet_file)
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    unexpected = [c for c in numeric_cols if c not in {"lon_wgs84", "lat_wgs84"}]
    assert not unexpected, (
        f"{parquet_file.name} has unexpected numeric columns: {unexpected}. "
        f"Only 'lon_wgs84' and 'lat_wgs84' are allowed."
    )


def test_collars_categorized_schema():
    """collars_categorized.parquet must have exactly the 6 expected columns."""
    path = PUBLIC_DIR / "collars_categorized.parquet"
    if not path.exists():
        pytest.skip("collars_categorized.parquet not present")
    df = pd.read_parquet(path)
    expected_cols = {
        "pseudo_id", "year_bucket", "lon_wgs84", "lat_wgs84",
        "li_category", "b_category",
    }
    assert set(df.columns) == expected_cols, (
        f"Schema mismatch. Expected {expected_cols}, got {set(df.columns)}"
    )


def test_coordinates_in_lopare_range():
    """Coordinates should be in BiH/Lopare area, not somewhere else."""
    path = PUBLIC_DIR / "collars_categorized.parquet"
    if not path.exists():
        pytest.skip("collars_categorized.parquet not present")
    df = pd.read_parquet(path)
    assert df["lon_wgs84"].between(*LOPARE_LON_RANGE).all(), (
        f"Longitudes outside Lopare range {LOPARE_LON_RANGE}"
    )
    assert df["lat_wgs84"].between(*LOPARE_LAT_RANGE).all(), (
        f"Latitudes outside Lopare range {LOPARE_LAT_RANGE}"
    )


def test_category_values_are_legal():
    """li_category and b_category may only contain known string labels."""
    path = PUBLIC_DIR / "collars_categorized.parquet"
    if not path.exists():
        pytest.skip("collars_categorized.parquet not present")
    df = pd.read_parquet(path)
    for col in ["li_category", "b_category"]:
        illegal = set(df[col].dropna().unique()) - ALLOWED_CATEGORY_VALUES
        assert not illegal, f"Column '{col}' has illegal values: {illegal}"


def test_pseudo_ids_are_pseudonymized():
    """pseudo_id must follow the year-based pattern, no operational hole IDs."""
    path = PUBLIC_DIR / "collars_categorized.parquet"
    if not path.exists():
        pytest.skip("collars_categorized.parquet not present")
    df = pd.read_parquet(path)
    valid_pattern = re.compile(r"^(20\d{2}|pre)-\d{2}$")
    invalid = [pid for pid in df["pseudo_id"] if not valid_pattern.match(pid)]
    assert not invalid, (
        f"Operational hole IDs detected (only YYYY-NN or pre-NN allowed): "
        f"{invalid[:5]}..."
    )


def test_geojson_in_lopare_bbox():
    """concession_lopare.geojson must cover the Lopare area."""
    path = PUBLIC_DIR / "concession_lopare.geojson"
    if not path.exists():
        pytest.skip("concession_lopare.geojson not present")
    gdf = gpd.read_file(path)
    assert str(gdf.crs).upper() == "EPSG:4326", f"Unexpected CRS: {gdf.crs}"
    minx, miny, maxx, maxy = gdf.total_bounds
    assert LOPARE_LON_RANGE[0] < minx < LOPARE_LON_RANGE[1]
    assert LOPARE_LON_RANGE[0] < maxx < LOPARE_LON_RANGE[1]
    assert LOPARE_LAT_RANGE[0] < miny < LOPARE_LAT_RANGE[1]
    assert LOPARE_LAT_RANGE[0] < maxy < LOPARE_LAT_RANGE[1]
