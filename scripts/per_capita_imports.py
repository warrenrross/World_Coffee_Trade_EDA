import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
OUT_FILE = DATA_DIR / "per_capita_imports_by_country_year.csv"

trade = pd.read_csv(DATA_DIR / "coffee_bilateral_trade_BACI.csv")
pop   = pd.read_csv(DATA_DIR / "baci_country_population.csv")

# Sum imports by importer country + year
imports = (
    trade
    .groupby(["Importer_ISO3", "Importer_Name", "Year"], as_index=False)["Value_1000USD"]
    .sum()
    .rename(columns={"Value_1000USD": "Total_Import_Value_1000USD"})
)

# Join population on ISO3 + Year
merged = imports.merge(
    pop[["ISO3", "Year", "Population"]],
    left_on=["Importer_ISO3", "Year"],
    right_on=["ISO3", "Year"],
    how="left"
)

# Per capita in USD
merged["Import_Per_Capita_USD"] = (
    (merged["Total_Import_Value_1000USD"] * 1000) / merged["Population"]
)

result = merged[[
    "Importer_ISO3", "Importer_Name", "Year",
    "Total_Import_Value_1000USD", "Population", "Import_Per_Capita_USD"
]].sort_values(["Year", "Importer_Name"])

result.to_csv(OUT_FILE, index=False)

print(f"Wrote {len(result):,} rows to {OUT_FILE}")
print(f"Rows with no population match: {result['Population'].isna().sum()}")
print(f"Years: {result['Year'].min()}–{result['Year'].max()}")
print(f"Countries: {result['Importer_ISO3'].nunique()}")
