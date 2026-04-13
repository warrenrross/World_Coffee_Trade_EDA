# Global Shipping Oil Price Dataset — Data Dictionary

## Overview

Annual oil price dataset designed as a supplemental time-series for the BACI bilateral trade dataset (1995–2024). Provides a globally representative, shipping-relevant oil price proxy alongside the three major benchmark crude prices. One row per calendar year, 30 rows total.

---

## File

| Property | Value |
|---|---|
| Filename | `global_shipping_oil_price.csv` |
| Rows | 30 (one per year, 1995–2024) |
| Columns | 13 |
| Units | All prices in USD per barrel |
| Granularity | Annual (aggregated from daily observations) |

---

## Column Definitions

| Column | Type | Unit | Description |
|---|---|---|---|
| `Year` | integer | — | Calendar year (1995–2024) |
| `Ship_Avg` | float | USD/bbl | Annual average global shipping oil price (composite, adjusted) |
| `Ship_High` | float | USD/bbl | Annual high (daily maximum) of the shipping composite |
| `Ship_Low` | float | USD/bbl | Annual low (daily minimum) of the shipping composite |
| `Brent_Avg` | float | USD/bbl | Annual average Brent crude spot price |
| `Brent_High` | float | USD/bbl | Annual high (daily maximum) Brent crude spot price |
| `Brent_Low` | float | USD/bbl | Annual low (daily minimum) Brent crude spot price |
| `WTI_Avg` | float | USD/bbl | Annual average West Texas Intermediate crude spot price |
| `WTI_High` | float | USD/bbl | Annual high (daily maximum) WTI crude spot price |
| `WTI_Low` | float | USD/bbl | Annual low (daily minimum) WTI crude spot price |
| `Dubai_Avg` | float | USD/bbl | Annual average Dubai Fateh crude spot price |
| `Dubai_High` | float | USD/bbl | Annual high of the daily-interpolated Dubai Fateh price |
| `Dubai_Low` | float | USD/bbl | Annual low of the daily-interpolated Dubai Fateh price |

> **Note on WTI 2020:** `WTI_Low` for 2020 is −$36.98, reflecting the April 20, 2020 historic negative price event (futures storage panic during COVID-19 lockdowns). This is a real and verified data point, not an error.

---

## Data Sources

### Brent Crude (daily)
- **Source**: U.S. Energy Information Administration (EIA)
- **Series**: `RBRTE` — Europe Brent Spot Price FOB (Dollars per Barrel)
- **URL**: https://www.eia.gov/dnav/pet/hist_xls/RBRTEd.xls
- **Frequency**: Trading days (Monday–Friday, excluding holidays)
- **Coverage in dataset**: 1995–2024 (full coverage after forward-fill)

### WTI Crude (daily)
- **Source**: U.S. Energy Information Administration (EIA)
- **Series**: `RWTC` — Cushing, OK WTI Spot Price FOB (Dollars per Barrel)
- **URL**: https://www.eia.gov/dnav/pet/hist_xls/RWTCd.xls
- **Frequency**: Trading days
- **Coverage in dataset**: 1995–2024 (full coverage after forward-fill)

### Dubai Fateh Crude (monthly → interpolated daily)
- **Source**: Federal Reserve Bank of St. Louis (FRED)
- **Series**: `POILDUBUSDM` — Global price of Dubai Crude, USD per barrel (Monthly)
- **Original source behind FRED**: IMF Primary Commodity Prices (derived from Platts/Energy Intelligence Group)
- **URL**: https://fred.stlouisfed.org/series/POILDUBUSDM
- **Frequency (original)**: Monthly
- **Frequency (used)**: Daily via linear interpolation between monthly observations
- **Coverage**: 1992–present; dataset uses 1995–2024

---

## Methodology

### Step 1 — Daily data loading
Brent and WTI daily spot prices were loaded from EIA bulk XLS files. Dubai monthly prices were loaded from FRED as CSV and linearly interpolated to a daily calendar series.

### Step 2 — Alignment and cleaning
All three series were merged on calendar date (outer join) and expanded to a full daily calendar using `asfreq('D')`. Weekend and holiday gaps in Brent and WTI were forward-filled by up to 3 calendar days. Rows where any benchmark remained missing after filling were dropped (primarily affected early 1995 before all series overlapped).

### Step 3 — Shipping composite
```
P_shipping     = 0.5 × Brent + 0.3 × Dubai + 0.2 × WTI
P_shipping_adj = P_shipping − 5.0
```
Weights and adjustment per `global_shipping_oil_spec.md`:
- **Brent (50%)**: Dominant benchmark for internationally traded waterborne crude; reflects global marginal pricing.
- **Dubai (30%)**: Captures Middle East exports and Asia-bound flows, the largest global demand center.
- **WTI (20%)**: U.S. production influence; Gulf Coast refining and export pricing.
- **−$5 adjustment**: Approximates the discount from light crude (Brent/WTI) to heavy crude and residual bunker fuel actually burned in shipping.

### Step 4 — Annual aggregation
For each year and each price series, three statistics were computed from the full daily distribution:
- **Avg**: arithmetic mean of all available trading days
- **High**: maximum single-day value
- **Low**: minimum single-day value

---

## Coverage Summary

| Benchmark | Source Frequency | Days in Range | Missing After Fill |
|---|---|---|---|
| Brent | Daily (EIA) | ~7,635 trading days | ~36 (holiday/data gaps, <0.5%) |
| WTI | Daily (EIA) | ~7,635 trading days | ~25 (<0.3%) |
| Dubai | Monthly (FRED → interpolated) | 10,958 calendar days | 0 |

---

## Key Events (Validation)

| Year | Event | Brent_Avg | Ship_Avg |
|---|---|---|---|
| 1998 | Asian financial crisis / oil crash | $12.79 | $7.92 |
| 2008 | Commodity supercycle peak | $97.02 | $90.94 |
| 2014 | OPEC supply glut / shale boom | $98.97 | $91.37 |
| 2020 | COVID-19 demand collapse | $41.89 | $36.53 |

---

## Limitations

- **Dubai interpolation**: Because daily Dubai spot prices are not freely available, monthly FRED values are linearly interpolated. `Dubai_High` and `Dubai_Low` reflect this smoothed series, not true intraday or intraweek volatility. Brent and WTI highs/lows are from actual daily observations.
- **No refinery margin or bunker fuel direct pricing**: The −$5 adjustment is a fixed constant. Real bunker fuel (VLSFO/HFO) prices diverge from crude benchmarks during refinery disruptions or IMO regulation changes (e.g., 2020 sulfur cap).
- **WTI landlocked distortions**: Cushing storage constraints occasionally cause WTI to trade at an anomalous discount or premium to global prices (e.g., April 2020, 2011–2013 Midcontinent glut). These are preserved as real data.
- **Annual granularity**: Suitable for macro-level trade analysis and longitudinal modeling. Not suitable for intra-year or seasonal shipping cost analysis.

---

## Relationship to BACI Trade Dataset

This dataset is a **global-level time series** (one row per year), not country-level. To use in Tableau or trade analysis alongside the BACI bilateral dataset, join on `Year`. Every country-year row in BACI will receive the same oil price values for that year, reflecting global shipping cost conditions rather than country-specific fuel prices.

---

## Version

| Property | Value |
|---|---|
| Built | April 2026 |
| BACI dataset range | 1995–2024 |
| EIA data vintage | April 2026 bulk download |
| FRED data vintage | April 2026 download (series through Feb 2026) |
