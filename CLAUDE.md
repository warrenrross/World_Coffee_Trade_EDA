# CLAUDE.md

This file provides guidance to Claude Code when working in this repository.

## Project Overview

EDA notebooks for the global coffee trade project. Two data sources:

1. **BACI/CEPII** — Bilateral coffee trade flows 1995–2024 (`data/coffee_bilateral_trade_BACI.csv`), HS codes 090111 and 090112, 136,768 rows
2. **FAOSTAT** — Raw country-level production/trade `.xls` files in `data/` (gitignored via `*.xls`); preprocessed CSV to be added to `data/`

## Running Notebooks

```bash
# Must be served over HTTP if notebooks use any fetch/CDN resources
jupyter notebook
# or
jupyter lab
```

## Jupytext Workflow

See `jupyter_version_control_spec.md` for full setup. Quick reference:

- Edit `.ipynb` in Jupyter — Jupytext auto-syncs `.py` (scripts/) and `.md` (docs/)
- `nbstripout` strips outputs before every commit automatically (via `.gitattributes`)
- Review diffs in `.py`; use `.md` for narrative; `.ipynb` only when outputs matter
- After adding a new notebook: `jupytext --set-formats "notebooks///ipynb,scripts///py:percent,docs///md" notebooks/<name>.ipynb && jupytext --sync notebooks/<name>.ipynb`

## Repository Structure

```
data/               — CSVs and data dictionaries (.xls/.xlsm present locally but gitignored)
notebooks/          — .ipynb files (source of truth)
scripts/            — Jupytext-synced .py (percent format)
docs/               — Jupytext-synced .md (narrative docs)
figures/<notebook>/ — Saved PNGs, named descriptively
reports/            — HTML EDA reports (served via GitHub Pages)
```

## Key Data Notes

- BACI `Unit_Value_USD_per_t = (Value_1000USD * 1000) / Quantity_tonnes`; trim to [100, 50000] for trend analysis
- FAOSTAT: filter out regional aggregates (rows where country contains 'World', 'Africa', 'Asia', etc.)
- USDA PSD units are 1000 × 60kg bags

---

## Session Log

### Session 1 — Repo setup and BACI EDA migration

**Completed:**
- Created `warrenrross/World_Coffee_Trade_EDA` and connected local repo
- Migrated BACI EDA notebook + Jupytext-synced `.py`/`.md`, figures, data, and config from the old `Perplexity/Coffee_bean_trade_BACI/` working folder
- Configured nbdime + Jupytext + nbstripout; verified `jupytext --sync` runs clean
- Added HTML profile and sweetviz reports to `reports/` for GitHub Pages
- Created `README.md`, `CLAUDE.md`, `memory.md`, `skill.md`
- Moved `jupyter_version_control_spec.md` here from the Trade Flows repo
- Updated Trade Flows repo (`warrenrross/World_Coffee_Trade`) README and `memory.md` to link back here
- Flattened `data/` — removed `data/baci/` and `data_raw/` subdirectories; all files now sit at `data/` root; `.xls`/`.xlsm` gitignored by extension

**Architectural decisions:**
- `data/` is flat — no source subdirectories. File prefixes (`coffee_bilateral_trade_*`) provide enough namespacing without folders.
- Binary source files (`.xls`, `.xlsm`) live in `data/` locally but are gitignored by extension — no separate `data_raw/` directory needed.
- `reports/` gitignore uses both `!reports/` and `!reports/*` — the directory-level negation alone does not un-ignore files inside it.
- FOA notebook (`coffee_trade_eda.ipynb`) was intentionally left in its original location (`Perplexity/Coffee_bean_trade_FOA/`) — to be migrated in a future session.

**Pending / next session:**
- Continue EDA analysis and notebook development

### Session 2 — New data sources, per capita analysis, Tableau validation

**Completed:**
- Added three new data sources to `data/`: population (World Bank via `baci_country_population.csv`), temperature (Berkeley Earth via `baci_country_temperature.csv`), and shipping/oil price (`global_shipping_oil_price.csv`) — each with data dictionaries
- Built `scripts/per_capita_imports.py` — standalone script that joins BACI trade + population, computes USD per capita imports by country per year, writes to `data/per_capita_imports_by_country_year.csv`
- Developed Tableau calculated field logic for per capita imports: `SUM([Value_1000USD]) * 1000 / [Population]`
- Built `notebooks/explor_joining_data.ipynb` (+ Jupytext-synced `.py`/`.md`) — step-by-step walkthrough of the groupby → join → per capita logic with spot-check table for Tableau validation and year filter cell

**Architectural decisions:**
- Tableau calculated field uses `[Population]` directly (not `AVG` or `SUM`) because population is connected via a Tableau Relationship, preserving country-year granularity natively
- `per_capita_imports.py` uses `AVG([Population])` equivalent logic: left join on ISO3+Year so population is a 1:1 match per country-year row after groupby
- Notebooks must be authored via the `.py` file first — writing `.ipynb` directly causes Jupytext sync errors on open because the paired `.py` timestamp lags. Correct workflow: edit `.py` → `jupytext --sync scripts/<name>.py`

**Known issues:**
- 40 importer rows have no population match (small territories / ISO3 mismatches between BACI and World Bank). These show null per capita in both Python and Tableau.
