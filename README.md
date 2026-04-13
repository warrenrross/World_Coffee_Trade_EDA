# World Coffee Trade — EDA

Exploratory data analysis of global coffee trade flows using the BACI/CEPII bilateral trade dataset (1995–2024).

---

## Companion project

The findings from this analysis feed into an interactive visualization:

**[Global Coffee Trade Flows](https://warrenrross.github.io/World_Coffee_Trade)** — an interactive D3.js world map of bilateral coffee trade flows, year by year.
Source: [warrenrross/World_Coffee_Trade](https://github.com/warrenrross/World_Coffee_Trade)

---

## Live reports

Full automated EDA reports, served via GitHub Pages:

| Report | Tool |
|---|---|
| [BACI Profile Report](https://warrenrross.github.io/World_Coffee_Trade_EDA/reports/coffee_bilateral_profile_report.html) | ydata-profiling |
| [BACI Sweetviz Report](https://warrenrross.github.io/World_Coffee_Trade_EDA/reports/coffee_bilateral_sweetviz_report.html) | sweetviz |

---

## Overview

This repo contains the EDA notebook, data, and figures for the BACI bilateral coffee trade dataset — 136,768 rows of country-pair trade flows across 229 exporters and 233 importers, covering HS codes `090111` (Arabica) and `090112` (Robusta).

Key analyses:
- Global trade volume and value trends (1995–2024)
- Top exporter/importer rankings and choropleth maps
- Bilateral flow heatmaps
- HS code (Arabica vs. Robusta) split
- Unit value trends and outlier handling
- Herfindahl–Hirschman Index (HHI) market concentration over time

---

## Data

| File | Source | Description |
|---|---|---|
| `coffee_bilateral_trade_BACI.csv` | [CEPII BACI](http://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=37) | Bilateral trade flows 1995–2024, 136,768 rows, HS 090111 + 090112 |
| `baci_country_population.csv` | World Bank | Annual population by ISO3 country, 1995–2024 |
| `baci_country_temperature.csv` | Berkeley Earth | Annual avg temperature by country, 1995–2024 |
| `global_shipping_oil_price.csv` | Various | Annual shipping index + Brent/WTI/Dubai oil prices, 1995–2024 |
| `per_capita_imports_by_country_year.csv` | Derived | BACI + population joined; USD per capita imports by country per year |

Raw `.xls` and `.xlsm` files are excluded from git (see `.gitignore`).

---

## Repository structure

```
data/               — CSVs and data dictionaries (.xls/.xlsm present but gitignored)
notebooks/          — .ipynb source notebooks
scripts/            — Jupytext-synced .py (percent format)
docs/               — Jupytext-synced .md (narrative)
figures/<notebook>/ — Exported PNGs, named descriptively
reports/            — HTML EDA reports (served via GitHub Pages)
```

---

## Setup

```bash
pip install pandas numpy matplotlib seaborn plotly geopandas \
            ydata-profiling sweetviz jupytext nbdime nbstripout
```

```bash
jupyter notebook
# or
jupyter lab
```

---

## Jupytext workflow

Each notebook is kept in sync with a `.py` script and a `.md` doc via [Jupytext](https://jupytext.readthedocs.io). Outputs are stripped before every commit by [nbstripout](https://github.com/kynan/nbstripout).

- **Always author via `.py`** — write or edit `scripts/<name>.py`, then `jupytext --sync scripts/<name>.py` generates the `.ipynb` and `.md`. Writing the `.ipynb` directly causes a sync timestamp error on open.
- Review diffs in `.py`; read narrative in `.md`
- `nbstripout` runs automatically on `git add`

See [`jupyter_version_control_spec.md`](jupyter_version_control_spec.md) for full setup and daily workflow.
