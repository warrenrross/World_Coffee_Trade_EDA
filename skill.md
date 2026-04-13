# Skill Index — Global Coffee Trade EDA

A reference of every technical skill applied in this project, organized by domain. Useful as a
learning roadmap or as a checklist when building a similar data analysis from scratch.

---

## 1. Data Sourcing & Acquisition

### Finding the right dataset
- Understanding the difference between **country-level aggregate trade** (FAOSTAT) and **bilateral trade** (BACI/Comtrade) — and why bilateral data is necessary to answer questions like "how much of Brazil's exports go to Germany"
- Identifying **HS codes** (Harmonized System commodity codes) for a specific product — here, `090111` and `090112` for unroasted green coffee
- Understanding **BACI's mirror-data reconciliation**: why BACI is preferred over raw Comtrade (it resolves discrepancies between what exporters report vs. what importers report)

### Downloading & filtering large datasets
- Working with **bulk ZIP downloads** containing multi-hundred-MB CSVs
- Filtering multi-commodity datasets to a specific product by item code or HS code using pandas
- Aggregating across multiple related HS codes (summing `090111` + `090112` per year/pair)

---

## 2. Data Processing (Python / Pandas)

### Reshaping and aggregating
- `groupby` aggregations across multiple dimensions (year × exporter × importer)
- Computing **derived metrics**: net trade position (`exports - imports`), country-level totals from bilateral data, unit value (`Value_1000USD * 1000 / Quantity_tonnes`)
- Unit conversions: thousands USD → millions USD, tonnes → thousand tonnes

### Outlier handling
- Trimming unit value to `[100, 50000]` USD/t before trend analysis — raw data contains division-by-zero artifacts and mis-reported quantities
- Using percentile inspection (`.describe()`, `.quantile()`) to identify appropriate trim bounds

### Regional aggregate filtering (FAOSTAT-specific)
- FAOSTAT includes regional aggregate rows (World, Africa, Asia, Europe, etc.) alongside country rows
- Filter by excluding rows where the country name contains: `'World'`, `'Africa'`, `'Asia'`, `'Europe'`, `'America'`, `'Oceania'`, `'Low-income'`, `'OECD'`

### Market concentration analysis
- **HHI (Herfindahl–Hirschman Index)**: `(shares**2).sum() * 10000` applied per year across exporter or importer totals
- Interpreting HHI: <1500 = competitive, 1500–2500 = moderate concentration, >2500 = highly concentrated

### Data dictionary & documentation
- Writing column-level documentation including units, source, and value ranges
- Including sample data (top flows, percentile distributions) in documentation

---

## 3. Exploratory Data Analysis

### Automated profiling
- `ydata-profiling` (formerly pandas-profiling) — generates a comprehensive HTML report covering distributions, correlations, missing values, and sample data for every column
- `sweetviz` — generates a visual HTML comparison report; useful for comparing subsets (e.g. HS 090111 vs. 090112)
- Both tools produce large HTML files (~1–5MB); store in `reports/` and serve via GitHub Pages rather than committing outputs inline

### Visualization
- `matplotlib` / `seaborn` for custom charts: trend lines, bar charts, heatmaps
- `geopandas` for geographic choropleth maps — join on ISO3 codes (`iso_a3` in Natural Earth shapefiles)
- Saving figures as PNGs to `figures/<notebook_name>/` with descriptive stable names (never auto-generated names like `output_1_0.png`)

### Log scale vs. linear scale
- When one country (Brazil, ~$11B net) dominates the range, a linear color scale makes 90% of other countries look identical
- **Log transform**: `t = log(value / anchor) / log(max / anchor)` distributes perceptual difference across the actual distribution
- Use `NEUTRAL_BAND` anchoring (e.g. ±$1M) to avoid sign noise for near-balanced countries

### Map joins
- BACI uses ISO3 codes (`Exporter_ISO3`, `Importer_ISO3`)
- GeoPandas Natural Earth uses `iso_a3`
- Some territories have `-99` for `iso_a3` in Natural Earth — handle separately if needed

---

## 4. Jupyter Notebook Version Control

### Stack: nbdime + Jupytext + nbstripout

| Tool | Role |
|---|---|
| Jupytext | Syncs `.ipynb` ↔ `.py` (percent format) ↔ `.md` |
| nbstripout | Strips cell outputs before every `git add` (via `.gitattributes`) |
| nbdime | Notebook-aware `git diff` and `git merge` locally |

### Daily workflow
1. Edit `.ipynb` in Jupyter
2. Jupytext auto-updates paired `.py` (in `scripts/`) and `.md` (in `docs/`)
3. `git add` → nbstripout removes outputs automatically
4. Review diffs in `.py` (clean code); use `.md` for narrative; use `.ipynb` only when output context matters

### Pairing a new notebook
```bash
jupytext --set-formats "notebooks///ipynb,scripts///py:percent,docs///md" notebooks/<name>.ipynb
jupytext --sync notebooks/<name>.ipynb
```

### gitignore pattern for reports
```
*_profile_report.html
*_sweetviz_report.html
!reports/
!reports/*
```
`!reports/` alone is insufficient — the file-level pattern still matches inside the directory.
`!reports/*` is required to un-ignore the files themselves.

See `jupyter_version_control_spec.md` for full setup instructions.

---

## 5. Git & Repository Management

### Structuring a data analysis repo
- Separating `data/` (tracked CSVs), `data_raw/` (gitignored binaries), `notebooks/`, `scripts/`, `docs/`, `figures/`, `reports/`
- Gitignoring large binary source files (`.xls`, `.xlsm`) while tracking preprocessed CSVs
- Tracking figures in git for reproducibility (`figures/<notebook_name>/<descriptive_name>.png`)

### GitHub Pages for reports
- Enable Pages on the repo (Settings → Pages → deploy from `main`, root)
- Store HTML reports in `reports/` and use gitignore negation to include them
- Reports are served at `<user>.github.io/<repo>/reports/<filename>.html`
