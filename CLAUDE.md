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
