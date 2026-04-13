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

**Source:** [BACI — Base pour l'Analyse du Commerce International](http://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=37), CEPII

| Column | Description |
|---|---|
| `Year` | 1995–2024 |
| `Exporter_ISO3` / `Importer_ISO3` | Country codes |
| `HS_Code` | 090111 (Arabica) or 090112 (Robusta) |
| `Value_1000USD` | Trade value in thousands of USD |
| `Quantity_tonnes` | Trade quantity in metric tonnes |

Derived: `Unit_Value_USD_per_t = (Value_1000USD × 1000) / Quantity_tonnes`

Raw `.xls` and `.xlsm` files are excluded from git (see `.gitignore`). The working CSV is `data/baci/coffee_bilateral_trade_BACI.csv`.

---

## Repository structure

```
data/baci/          — BACI bilateral trade CSV + data dictionaries
data/fao/           — Preprocessed FAOSTAT CSV (to be added)
data/usda/          — USDA PSD coffee CSV (to be added)
data_raw/           — Raw binary source files (gitignored)
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

- Edit in Jupyter → Jupytext auto-updates `scripts/` and `docs/`
- Review diffs in `.py`; read narrative in `.md`
- `nbstripout` runs automatically on `git add`

See [`jupyter_version_control_spec.md`](jupyter_version_control_spec.md) for full setup and daily workflow.
