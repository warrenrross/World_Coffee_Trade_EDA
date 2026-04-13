# ---
# jupyter:
#   jupytext:
#     notebook_metadata_filter: kernelspec,jupytext
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Per Capita Coffee Imports by Country
# Step-by-step walkthrough of the logic used in `scripts/per_capita_imports.py`.

# %%
import pandas as pd
from pathlib import Path

DATA_DIR = Path.cwd().parent / "data"

trade = pd.read_csv(DATA_DIR / "coffee_bilateral_trade_BACI.csv")
pop   = pd.read_csv(DATA_DIR / "baci_country_population.csv")

print(f"Trade rows: {len(trade):,}")
print(f"Population rows: {len(pop):,}")

# %% [markdown]
# ## Step 1 — Understand the raw trade data
#
# Each row is a **bilateral flow**: one exporter → one importer, one year, one HS code.
# A country like Germany appears once per exporting partner — roughly 229 times per year.
# That is why the same importer name appears many times in the raw data.

# %%
trade.head()

# %%
# Germany in 2023 — one row per exporting country
deu_raw = trade[(trade["Importer_ISO3"] == "DEU") & (trade["Year"] == 2023)]
print(f"Germany 2023 raw rows: {len(deu_raw)}")
deu_raw.head()

# %% [markdown]
# ## Step 2 — Collapse to one row per importer per year
#
# `groupby` on `Importer_ISO3 + Importer_Name + Year`, then sum `Value_1000USD`.
# This gives total imports received by each country in each year.

# %%
imports = (
    trade
    .groupby(["Importer_ISO3", "Importer_Name", "Year"], as_index=False)["Value_1000USD"]
    .sum()
    .rename(columns={"Value_1000USD": "Total_Import_Value_1000USD"})
)

print(f"Rows after groupby: {len(imports):,}")
imports.head()

# %%
# Germany now has exactly one row per year
imports[imports["Importer_ISO3"] == "DEU"].sort_values("Year")

# %% [markdown]
# ## Step 3 — Join population
#
# Population joins on `ISO3 + Year`. Using a left join so all trade rows are kept
# even if a country has no population match.

# %%
pop.head()

# %%
merged = imports.merge(
    pop[["ISO3", "Year", "Population"]],
    left_on=["Importer_ISO3", "Year"],
    right_on=["ISO3", "Year"],
    how="left"
).drop(columns="ISO3")

print(f"Rows with no population match: {merged['Population'].isna().sum()}")
merged.head()

# %% [markdown]
# ## Step 4 — Calculate per capita
#
# `Value_1000USD × 1000` converts to USD, then divide by population.
# Result is **USD spent on coffee imports per person per year**.

# %%
merged["Import_Per_Capita_USD"] = (
    (merged["Total_Import_Value_1000USD"] * 1000) / merged["Population"]
)

result = merged[
    ["Importer_ISO3", "Importer_Name", "Year",
     "Total_Import_Value_1000USD", "Population", "Import_Per_Capita_USD"]
].sort_values(["Year", "Importer_Name"]).reset_index(drop=True)

print(f"Total rows: {len(result):,}")
print(f"Countries: {result['Importer_ISO3'].nunique()}")
print(f"Years: {result['Year'].min()}–{result['Year'].max()}")

# %% [markdown]
# ## Step 5 — Spot-check against Tableau
#
# Use these values to verify your Tableau calculated field.

# %%
spot_check_iso3 = ["CHE", "BEL", "NLD", "DEU", "ITA", "USA", "JPN", "FRA"]

result[
    (result["Importer_ISO3"].isin(spot_check_iso3)) &
    (result["Year"] == 2023)
].sort_values("Import_Per_Capita_USD", ascending=False)

# %% [markdown]
# ## Step 6 — Filter by year
#
# Change `YEAR` to any value between 1995–2024.

# %%
YEAR = 2023

(
    result[result["Year"] == YEAR]
    .sort_values("Import_Per_Capita_USD", ascending=False)
    .reset_index(drop=True).head(20)
)

# %%
