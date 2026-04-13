# ---
# jupyter:
#   jupytext:
#     formats: notebooks///ipynb,scripts///py:percent,docs///md
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
# # Coffee Bilateral Trade — EDA
# Exploratory Data Analysis on BACI/CEPII bilateral coffee trade data  
# **Source:** [BACI — CEPII](https://www.cepii.fr/DATA_DOWNLOAD/baci/doc/baci_webpage.html) · Version 202601 · HS92 revision  
# **HS Codes:** `090111` (green/unroasted) · `090112` (decaffeinated unroasted)  
# **Coverage:** 229 exporters × 233 importers · 1995–2024 · 136,768 bilateral flows

# %% [markdown]
# ## 0. Dependencies

# %%
# #!pip3 install pandas numpy matplotlib seaborn plotly
# #!pip3 install ydata-profiling
# #!pip3 install sweetviz
# #!pip3 install geopandas
# #!pip3 install ipywidgets
# #!pip3 install pycountry

# %% [markdown]
# ## 1. Load Data

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# ── Load ──────────────────────────────────────────────────────────────────────
df = pd.read_csv('../data/coffee_bilateral_trade_BACI.csv', dtype={'HS_Code': str})
df['Value_1000USD']   = pd.to_numeric(df['Value_1000USD'],   errors='coerce')
df['Quantity_tonnes'] = pd.to_numeric(df['Quantity_tonnes'], errors='coerce')

# Derived: unit value (USD per tonne)
df['Unit_Value_USD_per_t'] = (df['Value_1000USD'] * 1000) / df['Quantity_tonnes']

print(f'Shape: {df.shape}')
df.head(8)

# %% [markdown]
# ## 2. Basic Overview

# %%
print('=== dtypes ===')
print(df.dtypes)
print()
print('=== Missing values ===')
print(df.isnull().sum())
print()
print('=== HS code split ===')
print(df['HS_Code'].value_counts())
print()
print('=== Year range ===')
print(f"  {df['Year'].min()} – {df['Year'].max()} ({df['Year'].nunique()} years)")
print()
print('=== Unique countries ===')
print(f"  Exporters: {df['Exporter_Name'].nunique()}")
print(f"  Importers: {df['Importer_Name'].nunique()}")

# %%
# Descriptive statistics
df[['Value_1000USD', 'Quantity_tonnes', 'Unit_Value_USD_per_t']].describe().round(2)

# %% [markdown]
# ## 3. Automated HTML Report — ydata-profiling

# %%
from ydata_profiling import ProfileReport

profile = ProfileReport(
    df,
    title='Coffee Bilateral Trade — BACI Profile Report',
    explorative=True,
    minimal=False   # set True if the report takes too long on large datasets
)

profile.to_file('coffee_bilateral_profile_report.html')
print('Saved: coffee_bilateral_profile_report.html')

profile.to_notebook_iframe()

# %% [markdown]
# ## 4. Automated HTML Report — Sweetviz

# %%
import sweetviz as sv

sv_report = sv.analyze(df, target_feat='Value_1000USD')
sv_report.show_html('coffee_bilateral_sweetviz_report.html', open_browser=True)
print('Saved: coffee_bilateral_sweetviz_report.html')

# %% [markdown]
# ## 5. Global Trade Volume Over Time

# %%
annual = df.groupby('Year').agg(
    Total_Value=('Value_1000USD', 'sum'),
    Total_Quantity=('Quantity_tonnes', 'sum'),
    Num_Flows=('Value_1000USD', 'count')
).reset_index()

fig, axes = plt.subplots(3, 1, figsize=(14, 12), sharex=True)

for ax, col, label, color in [
    (axes[0], 'Total_Value',    'Total Value (billion USD)',  '#2196F3'),
    (axes[1], 'Total_Quantity', 'Total Quantity (million t)', '#4CAF50'),
    (axes[2], 'Num_Flows',      'Number of Bilateral Flows',  '#FF5722'),
]:
    scale = 1e6 if 'Value' in col else (1e6 if 'Quantity' in col else 1)
    ax.fill_between(annual['Year'], annual[col] / scale, alpha=0.2, color=color)
    ax.plot(annual['Year'], annual[col] / scale, color=color, linewidth=2.2)
    ax.set_ylabel(label)
    ax.grid(axis='y', linestyle='--', alpha=0.4)
    sns.despine(ax=ax)

axes[2].set_xlabel('Year')
fig.suptitle('Global Coffee Bilateral Trade — Annual Totals (1995–2024)',
             fontsize=14, fontweight='bold', y=1.01)
plt.tight_layout()
plt.savefig('baci_global_trend.png', dpi=150, bbox_inches='tight')
plt.show()

# %% [markdown]
# ## 6. Top Exporters & Importers (2023)

# %%
YEAR = 2023
TOP_N = 20
recent = df[df['Year'] == YEAR]

top_exp = recent.groupby('Exporter_Name')['Value_1000USD'].sum().nlargest(TOP_N).reset_index().sort_values('Value_1000USD')
top_imp = recent.groupby('Importer_Name')['Value_1000USD'].sum().nlargest(TOP_N).reset_index().sort_values('Value_1000USD')

fig, axes = plt.subplots(1, 2, figsize=(18, 9))

for ax, data, col, title, color in [
    (axes[0], top_exp, 'Exporter_Name', f'Top {TOP_N} Exporters — {YEAR}', '#FF5722'),
    (axes[1], top_imp, 'Importer_Name', f'Top {TOP_N} Importers — {YEAR}', '#2196F3'),
]:
    bars = ax.barh(data[col], data['Value_1000USD'] / 1e6, color=color, alpha=0.85, edgecolor='white')
    ax.set_xlabel('Total Value (billion USD)')
    ax.set_title(title, fontsize=13, fontweight='bold')
    for bar in bars:
        w = bar.get_width()
        ax.text(w + 0.02, bar.get_y() + bar.get_height() / 2,
                f'${w:.2f}B', va='center', fontsize=8)
    sns.despine(ax=ax)

plt.suptitle(f'Coffee Trade by Country — {YEAR} (Value, USD billion)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('baci_top_countries.png', dpi=150, bbox_inches='tight')
plt.show()

# %% [markdown]
# ## 7. Top Bilateral Flows — Heatmap (2023)

# %%
TOP_PAIR_N = 15

# Get top exporters and importers
top_exp_names = recent.groupby('Exporter_Name')['Value_1000USD'].sum().nlargest(TOP_PAIR_N).index.tolist()
top_imp_names = recent.groupby('Importer_Name')['Value_1000USD'].sum().nlargest(TOP_PAIR_N).index.tolist()

# Pivot to matrix
heat_data = (
    recent[recent['Exporter_Name'].isin(top_exp_names) & recent['Importer_Name'].isin(top_imp_names)]
    .groupby(['Exporter_Name', 'Importer_Name'])['Value_1000USD']
    .sum()
    .unstack(fill_value=0)
    / 1e3   # → millions USD
)

# Sort rows/cols by total
heat_data = heat_data.loc[
    heat_data.sum(axis=1).sort_values(ascending=False).index,
    heat_data.sum(axis=0).sort_values(ascending=False).index
]

fig, ax = plt.subplots(figsize=(14, 10))
sns.heatmap(
    heat_data,
    fmt='.0f',
    annot=True,
    cmap='YlOrRd',
    linewidths=0.4,
    ax=ax,
    annot_kws={'size': 8},
    cbar_kws={'label': 'Value (million USD)'}
)
ax.set_title(f'Bilateral Coffee Trade Flows — {YEAR} (Top {TOP_PAIR_N} × {TOP_PAIR_N}, million USD)',
             fontsize=13, fontweight='bold')
ax.set_xlabel('Importer')
ax.set_ylabel('Exporter')
ax.tick_params(axis='x', rotation=45)
ax.tick_params(axis='y', rotation=0)
plt.tight_layout()
plt.savefig('baci_flow_heatmap.png', dpi=150, bbox_inches='tight')
plt.show()

# %% [markdown]
# ## 8. Value Distribution

# %%
fig, axes = plt.subplots(1, 2, figsize=(15, 5))

for ax, col, title, color in [
    (axes[0], 'Value_1000USD',   'Trade Value (log₁₀, 1000 USD)', '#2196F3'),
    (axes[1], 'Quantity_tonnes', 'Quantity (log₁₀, tonnes)',       '#4CAF50'),
]:
    vals = df[col].dropna()
    vals_pos = vals[vals > 0]
    log_vals = np.log10(vals_pos)
    ax.hist(log_vals, bins=60, color=color, alpha=0.8, edgecolor='white')

    for pct, ls in [(50, '--'), (90, ':'), (99, '-.')]: 
        v = np.percentile(log_vals, pct)
        ax.axvline(v, color='black', linestyle=ls, linewidth=1.2,
                   label=f'p{pct} = {10**v:,.0f}')
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.set_xlabel('log₁₀(Value)')
    ax.set_ylabel('Count')
    ax.legend(fontsize=9)
    sns.despine(ax=ax)

plt.suptitle('Distribution of Bilateral Flow Sizes', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('baci_distributions.png', dpi=150, bbox_inches='tight')
plt.show()

# %% [markdown]
# ## 9. Unit Value (Price per Tonne) Over Time — Top Exporters

# %%
TOP_EXP_UV = 10

top_exp_global = (
    df.groupby('Exporter_Name')['Value_1000USD'].sum()
    .nlargest(TOP_EXP_UV).index.tolist()
)

uv_trend = (
    df[
        df['Exporter_Name'].isin(top_exp_global) &
        df['Unit_Value_USD_per_t'].between(100, 50000)  # trim extreme outliers
    ]
    .groupby(['Year', 'Exporter_Name'])['Unit_Value_USD_per_t']
    .median()
    .reset_index()
)

fig, ax = plt.subplots(figsize=(15, 7))
palette = sns.color_palette('tab10', n_colors=TOP_EXP_UV)

for country, color in zip(top_exp_global, palette):
    sub = uv_trend[uv_trend['Exporter_Name'] == country].sort_values('Year')
    ax.plot(sub['Year'], sub['Unit_Value_USD_per_t'],
            label=country, color=color, linewidth=1.8)

ax.set_title('Median Export Unit Value (USD/tonne) — Top 10 Exporters',
             fontsize=13, fontweight='bold')
ax.set_xlabel('Year')
ax.set_ylabel('USD per tonne')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
ax.legend(loc='upper left', fontsize=9, ncol=2)
ax.grid(axis='y', linestyle='--', alpha=0.4)
sns.despine(ax=ax)
plt.tight_layout()
plt.savefig('baci_unit_value_trend.png', dpi=150, bbox_inches='tight')
plt.show()

# %% [markdown]
# ## 10. HS Code Split Over Time

# %%
hs_trend = (
    df.groupby(['Year', 'HS_Code'])['Value_1000USD']
    .sum()
    .unstack(fill_value=0)
    / 1e6
)

hs_labels = {
    '090111': '090111 — Green (not roasted, not decaf)',
    '090112': '090112 — Decaffeinated, not roasted',
}

fig, ax = plt.subplots(figsize=(14, 6))
hs_trend.plot(kind='area', stacked=True, ax=ax,
              color=['#4CAF50', '#FF9800'], alpha=0.75)

handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, [hs_labels.get(l, l) for l in labels], fontsize=9)
ax.set_title('Trade Value by HS Code Over Time (billion USD)', fontsize=13, fontweight='bold')
ax.set_xlabel('Year')
ax.set_ylabel('Value (billion USD)')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:.1f}B'))
sns.despine(ax=ax)
plt.tight_layout()
plt.savefig('baci_hs_split.png', dpi=150, bbox_inches='tight')
plt.show()

# %% [markdown]
# ## 11. Map — Export Volume by Country (2023)

# %%
import geopandas as gpd

# Natural Earth 110m countries (geopandas >= 1.0 removed built-in datasets)
world = gpd.read_file("https://naturalearth.s3.amazonaws.com/110m_cultural/ne_110m_admin_0_countries.zip")
world = world.rename(columns={'ISO_A3': 'iso_a3'})

# Aggregate exporter totals for 2023
exp_2023 = (
    df[df['Year'] == YEAR]
    .groupby(['Exporter_ISO3'])['Value_1000USD']
    .sum()
    .reset_index()
    .rename(columns={'Exporter_ISO3': 'iso_a3', 'Value_1000USD': 'Export_Value_M'})
)
exp_2023['Export_Value_M'] /= 1e3  # → millions USD

world_exp = world.merge(exp_2023, on='iso_a3', how='left')

fig, ax = plt.subplots(figsize=(18, 9))
world.plot(ax=ax, color='#f0f0f0', edgecolor='#cccccc', linewidth=0.4)
world_exp[world_exp['Export_Value_M'].notna()].plot(
    column='Export_Value_M',
    ax=ax,
    cmap='YlOrBr',
    legend=True,
    legend_kwds={'label': 'Export Value (million USD)', 'orientation': 'horizontal',
                 'shrink': 0.5, 'pad': 0.02},
    missing_kwds={'color': '#f0f0f0'},
    edgecolor='#888888',
    linewidth=0.3
)
ax.set_title(f'Coffee Export Value by Country — {YEAR}', fontsize=14, fontweight='bold')
ax.axis('off')
plt.tight_layout()
plt.savefig('baci_map_exports.png', dpi=150, bbox_inches='tight')
plt.show()

# %% [markdown]
# ## 12. Map — Import Volume by Country (2023)

# %%
imp_2023 = (
    df[df['Year'] == YEAR]
    .groupby(['Importer_ISO3'])['Value_1000USD']
    .sum()
    .reset_index()
    .rename(columns={'Importer_ISO3': 'iso_a3', 'Value_1000USD': 'Import_Value_M'})
)
imp_2023['Import_Value_M'] /= 1e3  # → millions USD

world_imp = world.merge(imp_2023, on='iso_a3', how='left')

fig, ax = plt.subplots(figsize=(18, 9))
world.plot(ax=ax, color='#f0f0f0', edgecolor='#cccccc', linewidth=0.4)
world_imp[world_imp['Import_Value_M'].notna()].plot(
    column='Import_Value_M',
    ax=ax,
    cmap='Blues',
    legend=True,
    legend_kwds={'label': 'Import Value (million USD)', 'orientation': 'horizontal',
                 'shrink': 0.5, 'pad': 0.02},
    missing_kwds={'color': '#f0f0f0'},
    edgecolor='#888888',
    linewidth=0.3
)
ax.set_title(f'Coffee Import Value by Country — {YEAR}', fontsize=14, fontweight='bold')
ax.axis('off')
plt.tight_layout()
plt.savefig('baci_map_imports.png', dpi=150, bbox_inches='tight')
plt.show()

# %% [markdown]
# ## 13. Map — Net Trade Position by Country (2023)
# Positive (orange/red) = net exporter. Negative (blue) = net importer.

# %%
exports_by_country = (
    df[df['Year'] == YEAR]
    .groupby('Exporter_ISO3')['Value_1000USD'].sum()
    .rename('Exports')
)
imports_by_country = (
    df[df['Year'] == YEAR]
    .groupby('Importer_ISO3')['Value_1000USD'].sum()
    .rename('Imports')
)

net = pd.concat([exports_by_country, imports_by_country], axis=1).fillna(0)
net['Net_M'] = (net['Exports'] - net['Imports']) / 1e3  # millions USD
net = net.reset_index().rename(columns={'index': 'iso_a3',
                                         'Exporter_ISO3': 'iso_a3'})
# Handle index name
if 'Exporter_ISO3' in net.columns:
    net = net.rename(columns={'Exporter_ISO3': 'iso_a3'})
net.index.name = None
net = net.reset_index(drop=True)
net.columns = [c if c != 'index' else 'iso_a3' for c in net.columns]

world_net = world.merge(net[['iso_a3', 'Net_M']] if 'iso_a3' in net.columns
                        else net.rename(columns={net.columns[0]: 'iso_a3'})[['iso_a3','Net_M']],
                        on='iso_a3', how='left')

fig, ax = plt.subplots(figsize=(18, 9))
world.plot(ax=ax, color='#f0f0f0', edgecolor='#cccccc', linewidth=0.4)
world_net[world_net['Net_M'].notna()].plot(
    column='Net_M',
    ax=ax,
    cmap='RdBu_r',
    legend=True,
    legend_kwds={'label': 'Net Trade Position (million USD, positive = net exporter)',
                 'orientation': 'horizontal', 'shrink': 0.5, 'pad': 0.02},
    missing_kwds={'color': '#f0f0f0'},
    edgecolor='#888888',
    linewidth=0.3
)
ax.set_title(f'Coffee Net Trade Position by Country — {YEAR}', fontsize=14, fontweight='bold')
ax.axis('off')
plt.tight_layout()
plt.savefig('baci_map_net_trade.png', dpi=150, bbox_inches='tight')
plt.show()

# %% [markdown]
# ## 14. Top Bilateral Flows — Sankey-style Bar Chart

# %%
TOP_FLOWS = 25

top_flows = (
    df[df['Year'] == YEAR]
    .groupby(['Exporter_Name', 'Importer_Name'])['Value_1000USD']
    .sum()
    .nlargest(TOP_FLOWS)
    .reset_index()
)
top_flows['Flow'] = top_flows['Exporter_Name'] + ' → ' + top_flows['Importer_Name']
top_flows = top_flows.sort_values('Value_1000USD')

# Color by exporter
unique_exporters = top_flows['Exporter_Name'].unique()
palette = dict(zip(unique_exporters, sns.color_palette('tab10', len(unique_exporters))))
colors = [palette[e] for e in top_flows['Exporter_Name']]

fig, ax = plt.subplots(figsize=(14, 10))
bars = ax.barh(top_flows['Flow'], top_flows['Value_1000USD'] / 1e3,
               color=colors, alpha=0.85, edgecolor='white')

for bar in bars:
    w = bar.get_width()
    ax.text(w + 2, bar.get_y() + bar.get_height() / 2,
            f'${w:.0f}M', va='center', fontsize=8)

# Legend for exporters
legend_patches = [mpatches.Patch(color=c, label=e) for e, c in palette.items()]
ax.legend(handles=legend_patches, title='Exporter', fontsize=8,
          loc='lower right', framealpha=0.8)

ax.set_xlabel('Trade Value (million USD)')
ax.set_title(f'Top {TOP_FLOWS} Bilateral Coffee Trade Flows — {YEAR}',
             fontsize=13, fontweight='bold')
sns.despine(ax=ax)
plt.tight_layout()
plt.savefig('baci_top_flows.png', dpi=150, bbox_inches='tight')
plt.show()


# %% [markdown]
# ## 15. Exporter Market Concentration Over Time (HHI)

# %%
# Herfindahl-Hirschman Index for export market concentration
def hhi(series):
    shares = series / series.sum()
    return (shares ** 2).sum() * 10000  # scale to 0–10000

hhi_exp = (
    df.groupby(['Year', 'Exporter_Name'])['Value_1000USD'].sum()
    .groupby('Year').apply(hhi)
    .reset_index(name='HHI_Export')
)
hhi_imp = (
    df.groupby(['Year', 'Importer_Name'])['Value_1000USD'].sum()
    .groupby('Year').apply(hhi)
    .reset_index(name='HHI_Import')
)

fig, ax = plt.subplots(figsize=(14, 5))
ax.plot(hhi_exp['Year'], hhi_exp['HHI_Export'], color='#FF5722', linewidth=2.2, label='Export concentration (HHI)')
ax.plot(hhi_imp['Year'], hhi_imp['HHI_Import'], color='#2196F3', linewidth=2.2, label='Import concentration (HHI)')

# Reference lines
ax.axhline(1500, color='grey', linestyle='--', linewidth=1, label='Moderate concentration (1500)')
ax.axhline(2500, color='grey', linestyle=':',  linewidth=1, label='High concentration (2500)')

ax.set_title('Coffee Market Concentration Over Time (Herfindahl-Hirschman Index)',
             fontsize=13, fontweight='bold')
ax.set_xlabel('Year')
ax.set_ylabel('HHI (0 = perfectly distributed, 10000 = monopoly)')
ax.legend(fontsize=9)
ax.grid(axis='y', linestyle='--', alpha=0.4)
sns.despine(ax=ax)
plt.tight_layout()
plt.savefig('baci_hhi_concentration.png', dpi=150, bbox_inches='tight')
plt.show()

# %% [markdown]
# ## 16. Summary Table — Most Recent Year

# %%
latest = df['Year'].max()
summary = (
    df[df['Year'] == latest]
    .groupby(['Exporter_Name', 'Importer_Name'])
    .agg(
        Value_1000USD=('Value_1000USD', 'sum'),
        Quantity_tonnes=('Quantity_tonnes', 'sum')
    )
    .reset_index()
)
summary['Unit_Value_USD_t'] = (summary['Value_1000USD'] * 1000 / summary['Quantity_tonnes']).round(2)
summary = summary.sort_values('Value_1000USD', ascending=False)

print(f'Year: {latest} | Bilateral flows: {len(summary):,}')
summary.head(20)

# %%
