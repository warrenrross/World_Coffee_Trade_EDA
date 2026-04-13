# Project Memory — Global Coffee Trade EDA

A running log of every major decision, problem, and solution encountered during exploratory
data analysis of global coffee trade. Useful for resuming work, onboarding collaborators, or
understanding where the data pipeline came from.

The findings from this work feed into an interactive D3 visualization:
**[Global Coffee Trade Flows](https://warrenrross.github.io/World_Coffee_Trade)** — [warrenrross/World_Coffee_Trade](https://github.com/warrenrross/World_Coffee_Trade)

---

## Tools & Workflow

### AI-assisted development
This project was built collaboratively with **Claude Code** (Anthropic, `claude-sonnet-4-6`), an
agentic AI coding assistant running in the terminal. Claude Code read files, edited code, ran
shell commands, committed to git, and pushed to GitHub — all from natural-language conversation.
The `CLAUDE.md` file in this directory is specifically formatted to give future Claude Code
sessions full context without manual re-onboarding.

### Authoring environment
- **Claude Code CLI** — primary coding agent (file edits, git, shell)
- **Python 3.13** — data pipeline and notebook execution
- **Jupyter Lab / Notebook** — EDA notebooks (`coffee_trade_eda.ipynb`, `coffee_bilateral_trade_eda.ipynb`)
- **Jupytext** — syncs each `.ipynb` to a `.py` (percent format) and `.md` for clean git diffs
- **nbstripout** — strips notebook outputs before every commit (via `.gitattributes`)
- **nbdime** — notebook-aware diff and merge tool
- **Git** — version control; commits and pushes via Claude Code

---

## Phase 1 — Data Acquisition

### FAOSTAT (country-level totals)
- **Source**: https://www.fao.org/faostat/en/#data/TCL
- **Method**: Downloaded the bulk normalized ZIP from `https://bulks-faostat.fao.org/production/Trade_CropsLivestock_E_All_Data_(Normalized).zip` (last updated Dec 23, 2025)
- **Filter**: Item code `656` = "Coffee, green". Retained Import Quantity, Import Value, Export Quantity, Export Value.
- **Result**: `coffee_green_trade_FAOSTAT.csv` — 53,892 rows, 279 countries, 1961–2024.
- **Limitation discovered**: FAOSTAT only provides country-level totals. It does not identify trade partners. You cannot reconstruct "how much of Brazil's exports went to Germany" from this data alone.

### BACI (bilateral trade)
- **Source**: CEPII BACI HS92 v202601 — https://www.cepii.fr/DATA_DOWNLOAD/baci/data/BACI_HS92_V202601.zip
- **Filter**: HS codes `090111` (coffee, not roasted, not decaffeinated) and `090112` (coffee, not roasted, decaffeinated). Summed across both codes per year/exporter/importer pair.
- **Unit conversion**: Raw values are in thousands USD; divide by 1000 to get millions USD.
- **Result**: `coffee_bilateral_trade_BACI.csv` — 136,768 rows, 229 exporters, 233 importers, 1995–2024.
- **Why BACI over Comtrade directly**: BACI reconciles mirror data (what country A reports exporting vs. what country B reports importing) into a single harmonized figure. More reliable for global coverage.

### FAO vs. BACI comparison
- FAO reports ~55% higher total volume than BACI for the overlapping 1995–2024 period.
- Reason: FAO captures re-exports and uses a different methodology; BACI is stricter about origin/destination.
- Decision: BACI is the primary source for bilateral analysis. FAO provides the longer 1961–1994 history not available in BACI.

---

## Phase 2 — EDA Notebooks

Two Jupyter notebooks built for exploration. Each is synced to a `.py` script and `.md` doc via
Jupytext. Live HTML reports are served via GitHub Pages.

### `coffee_bilateral_trade_eda.ipynb` — BACI data
- **Location**: `notebooks/coffee_bilateral_trade_eda.ipynb`
- Bilateral heatmaps (exporter × importer × year)
- Three `geopandas` choropleth maps: exports, imports, net trade position
- Herfindahl–Hirschman Index (HHI) concentration metric per year
- Unit value trend analysis (`Value_1000USD * 1000 / Quantity_tonnes`), trimmed to [100, 50000] USD/t to remove outliers
- `ydata-profiling` automated HTML report
- `sweetviz` visual summary report
- Live reports:
  - [Profile report](https://warrenrross.github.io/World_Coffee_Trade_EDA/reports/coffee_bilateral_profile_report.html)
  - [Sweetviz report](https://warrenrross.github.io/World_Coffee_Trade_EDA/reports/coffee_bilateral_sweetviz_report.html)

**Dependency note**: All pip installs use the `#!pip3 install` syntax so cells can be uncommented and run directly in Jupyter without modifying the notebook structure.

### `coffee_trade_eda.ipynb` — FAOSTAT data
- **Location**: `notebooks/coffee_trade_eda.ipynb` (to be migrated from source)
- Country-level export/import trends over time
- Missing data and flag distribution analysis
- Top exporters and importers by value and volume
- Export unit value trends
- `ydata-profiling` and `sweetviz` reports

---

## Version Control Setup

### Stack
nbdime + Jupytext + nbstripout — see `jupyter_version_control_spec.md` for full setup.

### Key decisions
- **Jupytext format**: `notebooks///ipynb` + `scripts///py:percent` + `docs///md` — three parallel representations of each notebook
- **nbstripout via `.gitattributes`**: outputs stripped automatically at `git add` time; no manual step required
- **`.gitignore`**: `data_raw/` excluded (50MB+ binary source files); `*_profile_report.html` and `*_sweetviz_report.html` excluded from all paths except `reports/` (tracked for GitHub Pages)
- **`reports/` re-inclusion**: gitignore uses `!reports/` + `!reports/*` negation pattern — `!reports/` alone is insufficient because the file-level pattern still matches inside the directory

### Repository location
`data_raw/` holds original `.xls` and `.xlsm` source files (gitignored). Rationale: binary formats don't diff, source files are large (50MB+), and the public download portals (FAOSTAT, USDA PSD) are canonical. The preprocessed CSVs in `data/` are what the notebooks actually use and are tracked normally.
