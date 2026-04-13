# Data Dictionary — BACI Country Population
**File:** `baci_country_population.csv`
**Rows:** 6,930 (231 countries × 30 years, 1995–2024)
**Generated:** April 2026

---

## Columns

| Column | Type | Example | Description |
|---|---|---|---|
| `ISO3` | string | `BRA` | ISO 3166-1 alpha-3 country code. Taken directly from the BACI dataset. Used as the join key to BACI trade data. |
| `Country_Name` | string | `Brazil` | Country display name as it appears in BACI. May differ slightly from World Bank naming conventions (e.g. BACI uses "Viet Nam", World Bank uses "Vietnam"). The `ISO3` field is the reliable join key — do not join on name. |
| `Year` | integer | `2024` | Calendar year. Covers the full BACI HS92 v202601 range: 1995–2024. |
| `Population` | float | `215313498` | Total resident population. Integer values stored as float due to NaN representation in pandas. No decimal population values exist — any `.0` suffix is an artifact of the data type. |
| `Population_Source` | string | `World Bank` | Indicates how the population value was obtained. Three possible values — see Source Classification below. |

---

## Source Classification

### `World Bank`
**90.0% of rows (6,240 rows)**

- **Indicator:** `SP.POP.TOTL` — Population, total
- **Provider:** World Bank Open Data
- **Download URL:** `https://api.worldbank.org/v2/en/indicator/SP.POP.TOTL?downloadformat=csv`
- **File used:** `API_SP.POP.TOTL_DS2_en_csv_v2_58.csv` (inside the downloaded ZIP)
- **Version:** World Bank data release April 2026
- **Coverage:** 266 country/territory entries × years 1960–2024
- **Definition:** De facto population — counts all residents regardless of legal status or citizenship. Includes refugees settled in the country but excludes short-term visitors.
- **Join method:** Matched on ISO3 code (`Country Code` in World Bank file = `ISO3` in BACI). No name-based matching was used.
- **Year range used:** 1995–2024 only (columns outside this range discarded).

### `Estimated (territory)`
**7.7% of rows (537 rows) — 18 territories**

World Bank does not publish `SP.POP.TOTL` data for these 18 small territories and island dependencies. Population was estimated using a compound growth model:

```
Population(year) = Population(base_year) × (1 + annual_growth_rate)^(year - base_year)
```

The base year population and growth rate for each territory were sourced from the CIA World Factbook and/or the respective territory's official statistics office. The table below documents each territory's parameters:

| ISO3 | Territory | Base Pop (2010) | Annual Rate | Notes |
|---|---|---|---|---|
| `AIA` | Anguilla | 18,000 | +1.0% | CIA World Factbook |
| `BES` | Bonaire, Sint Eustatius & Saba | 25,000 | +1.0% | Combined three islands |
| `BLM` | Saint Barthélemy | 9,000 | +0.5% | INSEE France estimates |
| `CCK` | Cocos (Keeling) Islands | 600 | 0.0% | Australian Dept. of Infrastructure |
| `COK` | Cook Islands | 17,500 | -0.5% | Cook Islands Statistics Office; declining due to emigration |
| `CXR` | Christmas Island | 2,200 | 0.0% | Australian Dept. of Infrastructure |
| `FLK` | Falkland Islands (Malvinas) | 3,200 | +0.5% | Falkland Islands Government |
| `IOT` | British Indian Ocean Territory | 4,000 | 0.0% | Military/civilian personnel; approximate |
| `MSR` | Montserrat | 5,000 | +0.5% | Montserrat Statistics Dept. (post-1995 eruption recovery) |
| `MYT` | Mayotte | 175,000 | +3.0% | INSEE France; high growth rate reflects rapid population increase |
| `NFK` | Norfolk Island | 2,500 | -0.5% | Australian Bureau of Statistics |
| `NIU` | Niue | 1,600 | -1.0% | Niue Statistics; declining due to emigration to New Zealand |
| `PCN` | Pitcairn | 50 | 0.0% | One of the world's smallest populations; stable |
| `SHN` | Saint Helena | 6,000 | +0.5% | Saint Helena Government Statistics |
| `SPM` | Saint Pierre and Miquelon | 6,200 | 0.0% | INSEE France |
| `TKL` | Tokelau | 1,500 | 0.0% | Tokelau National Statistics; stable |
| `WLF` | Wallis and Futuna | 11,500 | -0.5% | INSEE France; declining due to emigration |

**Limitations of estimated values:**
- Growth rates are held constant across the full 1995–2024 window. Real populations fluctuate with migration, natural disasters, and policy changes.
- Base year (2010) was chosen as the midpoint of the range to minimize compound error in both directions.
- These territories account for a negligible share of global coffee trade and their population figures have minimal impact on any per-capita calculations.

### `Estimated (historical entity)`
**Included in the 7.7% above — 2 entities**

Two ISO3 codes in BACI represent political entities that no longer exist. Population was estimated for years they were active:

| ISO3 | Entity | Active Years in Dataset | Method |
|---|---|---|---|
| `ANT` | Netherlands Antilles | 1995–2010 | Linear interpolation from ~185,000 (1995) to ~198,000 (2010), based on Dutch Central Bureau of Statistics historical records. Dissolved October 10, 2010 — split into Curaçao (`CUW`), Sint Maarten (`SXM`), and the special municipalities of Bonaire, Sint Eustatius, and Saba (`BES`). Years 2011–2024 left as `No data`. |
| `SCG` | Serbia and Montenegro | 1995–2005 | Linear growth from ~10,500,000 (1995) to ~10,600,000 (2005) based on UN population estimates for the combined territory. Dissolved June 2006 — split into Serbia (`SRB`) and Montenegro (`MNE`). Years 2006–2024 left as `No data`. |

### `No data`
**2.2% of rows (153 rows) — 6 entities**

These entries have `null` population and cannot be estimated meaningfully:

| ISO3 | Entity | Reason |
|---|---|---|
| `ATF` | French Southern & Antarctic Territories | Uninhabited except for rotating research station staff (~100–200 at any time). No permanent civilian population. |
| `PUS` | US Miscellaneous Pacific Islands | Uninhabited or near-uninhabited atolls (Howland, Baker, Jarvis, Johnston, Midway, Wake). No permanent population. |
| `S19` | Other Asia, nes | BACI catch-all code for unspecified Asian trade flows that could not be attributed to a specific country. Not a geographic entity. |
| `ZA1` | Southern African Customs Union | Active in BACI only through 1999. Represents an aggregate of South Africa, Botswana, Lesotho, Namibia, and Eswatini before BACI disaggregated them. All five countries have individual records with full World Bank data. |
| `ANT` | Netherlands Antilles (2011–2024) | Entity dissolved October 2010. Successor states (`CUW`, `SXM`, `BES`) carry population data from 2011 onward. |
| `SCG` | Serbia and Montenegro (2006–2024) | Entity dissolved June 2006. Successor states (`SRB`, `MNE`) carry population data from 2006 onward. |

---

## How to Join to BACI Trade Data

```python
import pandas as pd

trade = pd.read_csv('coffee_bilateral_trade_BACI.csv')
pop   = pd.read_csv('baci_country_population.csv')

# Join exporter population
trade = trade.merge(
    pop.rename(columns={'ISO3':'Exporter_ISO3', 'Population':'Exporter_Population'}),
    on=['Exporter_ISO3','Year'], how='left'
)

# Join importer population
trade = trade.merge(
    pop.rename(columns={'ISO3':'Importer_ISO3', 'Population':'Importer_Population'}),
    on=['Importer_ISO3','Year'], how='left'
)
```

To compute **per-capita trade value** (e.g. USD of coffee exports per person):
```python
trade['Export_Per_Capita_USD'] = (trade['Value_1000USD'] * 1000) / trade['Exporter_Population']
```

---

## Known Limitations

1. **World Bank 2024 data**: The most recent year may be preliminary or estimated by the World Bank itself, particularly for countries with delayed census reporting.
2. **Name mismatches**: BACI uses CEPII's naming conventions; World Bank uses its own. The ISO3 join is reliable. Never join on `Country_Name` alone.
3. **Territory estimates are approximations**: The 18 estimated territories collectively represent well under 0.1% of global coffee trade volume. For population-weighted analyses these values are negligible but are included for completeness.
4. **Historical entities**: `ANT` and `SCG` have partial coverage by design — only years when those political entities existed.
5. **Non-country aggregates** (`S19`, `ZA1`): These appear in BACI as origin/destination codes but have no meaningful population equivalent. Exclude them from per-capita calculations.
