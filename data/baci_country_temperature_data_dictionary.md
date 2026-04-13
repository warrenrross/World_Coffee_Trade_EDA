# Data Dictionary — BACI Country Average Annual Temperature
**File:** `baci_country_temperature.csv`
**Rows:** 6,930 (231 countries × 30 years, 1995–2024)
**Generated:** April 2026

---

## Columns

| Column | Type | Example | Description |
|---|---|---|---|
| `ISO3` | string | `BRA` | ISO 3166-1 alpha-3 country code. Taken directly from BACI. Join key to trade data. |
| `Country_Name` | string | `Brazil` | Country display name as it appears in BACI. Join on `ISO3`, not on name. |
| `Year` | integer | `2024` | Calendar year. Covers the full BACI range: 1995–2024. |
| `Avg_Temp_C` | float | `25.53` | Annual average surface air temperature in degrees Celsius. Computed as the unweighted mean of 12 monthly average temperatures. |
| `Uncertainty_C` | float | `0.15` | Estimated ±1σ uncertainty in degrees Celsius. Available only for Berkeley Earth rows (1995–2016). ERA5 rows have `null` here — ERA5 is a deterministic reanalysis model rather than a station-interpolation with explicit uncertainty. |
| `Temp_Source` | string | `Berkeley Earth` | Data source. Four possible values — see Source Classification below. |
| `Source_Notes` | string | `BE slug: brazil` | Supplemental notes: the Berkeley Earth file slug used, proxy country name if applicable, or reason for no data. |

---

## Source Classification

### `Berkeley Earth`
**~67% of rows — 231 countries, years 1995–2016**

- **Provider:** Berkeley Earth (https://berkeleyearth.org)
- **Dataset accessed via:** compgeolab temperature-data repository — https://github.com/compgeolab/temperature-data
- **Download URL:** `https://github.com/compgeolab/temperature-data/releases/latest/download/temperature-data.zip`
- **License:** CC-BY-NC (Berkeley Earth data; processed by Leonardo Uieda / compgeolab)
- **Underlying methodology:** Berkeley Earth combines 23 million monthly thermometer measurements from 57,685 weather stations. A kriging-based spatial interpolation is used to produce gridded fields that are then aggregated to country boundaries. Absolute temperatures are reconstructed by adding anomalies to a baseline climatology.
- **File format:** One CSV per country, monthly resolution, going back to ~1750 where data exists. The compgeolab subset converts anomalies to absolute temperatures and removes NaNs.
- **Processing applied here:**
  1. Filtered to years 1995–2016 (the dataset's last year)
  2. Aggregated 12 monthly values per year to an annual mean (`temperature_C` column)
  3. Annual uncertainty computed as mean of monthly `uncertainty_C` values
  4. Matched to BACI ISO3 via a manual slug lookup table (see Proxy section below)
- **Coverage:** 225 country files provided; 203 unique slugs used after deduplication

### `Berkeley Earth (proxy: <slug>)`
**~5% of rows — 18 territories/entities, years 1995–2016**

Used for BACI ISO3 codes that have no direct Berkeley Earth country file. A geographically adjacent or climatically representative country was used as a proxy. The proxy slug is recorded in `Source_Notes`.

| ISO3 | Entity | Proxy Used | Rationale |
|---|---|---|---|
| `ANT` | Netherlands Antilles (hist.) | `dominican-republic` | Caribbean, similar latitude |
| `BLM` | Saint Barthélemy | `france` | French overseas collectivity |
| `BMU` | Bermuda | `united-states` | North Atlantic, closest large dataset |
| `BRN` | Brunei Darussalam | `malaysia` | Borneo island, identical climate zone |
| `CCK` | Cocos (Keeling) Islands | `indonesia` | Eastern Indian Ocean, equatorial |
| `CIV` | Côte d'Ivoire | `ghana` | Adjacent country, same climate zone |
| `COK` | Cook Islands | `fiji` | South Pacific tropical island climate |
| `CUW` | Curaçao | `dominican-republic` | Caribbean, similar latitude |
| `FSM` | Federated States of Micronesia | `fiji` | Western Pacific tropical climate |
| `GIB` | Gibraltar | `spain` | Southern tip of Spain |
| `GUM` | Guam | `virgin-islands` | Tropical Pacific/Caribbean island climate |
| `IOT` | British Indian Ocean Territory | `indonesia` | Central Indian Ocean, equatorial |
| `KIR` | Kiribati | `fiji` | Equatorial Pacific island climate |
| `MDV` | Maldives | `indonesia` | Central Indian Ocean, equatorial |
| `MHL` | Marshall Islands | `fiji` | Tropical Pacific island climate |
| `NFK` | Norfolk Island | `australia` | South Pacific, Australian territory |
| `NRU` | Nauru | `fiji` | Tropical Pacific island |
| `PCN` | Pitcairn Islands | `samoa` | South Pacific tropical |
| `PLW` | Palau | `fiji` | Western Pacific tropical |
| `SCG` | Serbia and Montenegro (hist.) | `serbia` | Direct successor state, same geography |
| `SHN` | Saint Helena | `cameroon` | South Atlantic — West Africa is nearest landmass |
| `SPM` | Saint Pierre and Miquelon | `canada` | Canadian Maritime climate |
| `SSD` | South Sudan | `uganda` | Adjacent country, same climate zone |
| `SWZ` / `SWZ` mapped to | `swaziland` | Direct match (BE uses old name) | — |
| `TCA` | Turks and Caicos | `turks-and-caicas-islands` | Direct match |
| `TKL` | Tokelau | `samoa` | Polynesian Pacific |
| `TUV` | Tuvalu | `fiji` | Tropical Pacific island |
| `VUT` | Vanuatu | `fiji` | Melanesian Pacific island chain |
| `WLF` | Wallis and Futuna | `samoa` | Polynesian Pacific |

### `ERA5 (Open-Meteo)`
**~27% of rows — 228 countries, years 2017–2024**

Used for all years 2017–2024. The Berkeley Earth compgeolab dataset ends at 2016; this source fills the gap.

- **Underlying data:** ERA5 reanalysis produced by ECMWF (European Centre for Medium-Range Weather Forecasts) for the Copernicus Climate Change Service
- **API:** Open-Meteo Historical Weather API — https://open-meteo.com/en/docs/historical-weather-api
- **Endpoint:** `https://archive-api.open-meteo.com/v1/archive`
- **Variable:** `temperature_2m_mean` — daily mean 2-metre surface air temperature (°C)
- **Spatial resolution:** ERA5 native resolution is ~31 km (0.25°). The API returns the grid cell containing the requested coordinate.
- **Coordinate used:** Country geographic centroid from the RestCountries API (https://restcountries.com/v3.1/all). Manual centroids applied for historical entities and territories not in RestCountries (Netherlands Antilles, Serbia & Montenegro, SACU aggregate).
- **Processing applied here:**
  1. Daily `temperature_2m_mean` queried for 2017-01-01 to 2024-12-31 at country centroid
  2. NaN days dropped
  3. 365/366 daily values averaged to produce one annual mean per year
- **Limitation — point estimate:** ERA5 temperatures are extracted at a single point (country centroid), not spatially averaged across the country boundary. For large, climatically diverse countries (Russia, Canada, USA, Brazil, China, Australia), the centroid point temperature may differ meaningfully from a true area-weighted national average. Berkeley Earth data for 1995–2016 is a full spatial average and is therefore more representative for large countries.
- **Uncertainty:** Not reported. ERA5 is a deterministic reanalysis product; ensemble spread is not available through the Open-Meteo interface.

### `No data`
**1.1% of rows (74 rows) — 3 entities**

| ISO3 | Entity | Reason |
|---|---|---|
| `PUS` | US Miscellaneous Pacific Islands | Uninhabited atolls (Howland, Baker, Jarvis, Johnston, Midway, Wake). No meaningful national temperature. |
| `S19` | Other Asia, nes | Non-geographic BACI aggregate code. No physical location. |
| `ZA1` | Southern African Customs Union (≤1999) | BACI aggregate for Botswana, Lesotho, Namibia, South Africa, and Eswatini before disaggregation. No single temperature value is meaningful; use the individual country records. |

---

## Consistency Note: Berkeley Earth vs. ERA5 Transition at 2016/2017

The two sources use different methodologies. At the 2016→2017 boundary, a discontinuity may appear for some countries — particularly those where:
- Berkeley Earth's station-based interpolation and ERA5 reanalysis differ in their baseline climatology
- The proxy used for 1995–2016 introduces a systematic offset versus the ERA5 centroid point used for 2017–2024

**Where this matters most:** Small islands and territories using proxy countries for the BE period (e.g. Maldives using the Indonesia proxy) will show a step change at 2017. For these cases, ERA5 centroid values are likely more accurate since they reflect the territory's actual location.

**Recommended use:** For trend analysis across 1995–2024, treat the sources as continuous for most sovereign countries. For small territories, use caution across the 2016/2017 seam or restrict analysis to one source period.

---

## How to Join to BACI Trade Data

```python
import pandas as pd

trade = pd.read_csv('coffee_bilateral_trade_BACI.csv')
temp  = pd.read_csv('baci_country_temperature.csv')

# Join exporter temperature
trade = trade.merge(
    temp.rename(columns={'ISO3':'Exporter_ISO3', 'Avg_Temp_C':'Exporter_Avg_Temp_C'})[
        ['Exporter_ISO3','Year','Exporter_Avg_Temp_C']
    ],
    on=['Exporter_ISO3','Year'], how='left'
)

# Join importer temperature
trade = trade.merge(
    temp.rename(columns={'ISO3':'Importer_ISO3', 'Avg_Temp_C':'Importer_Avg_Temp_C'})[
        ['Importer_ISO3','Year','Importer_Avg_Temp_C']
    ],
    on=['Importer_ISO3','Year'], how='left'
)
```

---

## Known Limitations

1. **Annual mean hides seasonal variation.** A single annual average does not capture monsoons, frost seasons, or growing season temperatures relevant to coffee cultivation. For agriculture-focused analysis, monthly or seasonal breakdowns would be more appropriate.
2. **ERA5 centroid point vs. area average.** For large countries, the centroid point may not represent national average temperature. Brazil's centroid (~-10°, -53°) is in the Amazon and reads warmer than a true national average that would include the cooler south.
3. **Proxy countries for small territories.** The 18 territories using proxies will have systematically biased temperatures if the proxy country's climate differs meaningfully from the territory's actual climate.
4. **2016/2017 source transition.** Slight methodological discontinuity between Berkeley Earth (station-based spatial average) and ERA5 (reanalysis point estimate). See Consistency Note above.
5. **ERA5 2024 data.** The 2024 ERA5 data used here reflects the full calendar year. ERA5 data for very recent months undergoes revision; 2024 values may be slightly updated in future releases.
