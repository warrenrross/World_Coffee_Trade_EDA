# Global Shipping Oil Price Dataset Specification (1995–2024)

## 1) Objective

Construct an annual dataset including:

### A. Global Shipping Oil Price
- Annual average
- Annual high
- Annual low

### B. Regional Benchmarks
For each:
- Annual average
- Annual high
- Annual low

Benchmarks:
- Brent Crude
- West Texas Intermediate (WTI)
- Dubai Crude

---

## 2) Data Sources

### Primary
- U.S. Energy Information Administration (EIA)
  - Daily spot prices:
    - Brent
    - WTI
    - Dubai

### Optional (Validation)
- World Bank
- IMF
- OPEC Basket

---

## 3) Data Frequency & Cleaning

- Frequency: Daily (USD/barrel)
- Forward-fill ≤ 3 days
- Remove invalid values (0/null)
- Align time index across all series

---

## 4) Global Shipping Price Model

P_shipping = 0.5 * Brent + 0.3 * Dubai + 0.2 * WTI

---

## 5) Shipping Adjustment (Optional)

P_shipping_adj = P_shipping - 5

Represents heavy crude / bunker fuel discount.

---

## 6) Annual Aggregation

For each year:

- Average = mean(P_t)
- High = max(P_t)
- Low = min(P_t)

Apply to:
- Shipping price
- Brent
- WTI
- Dubai

---

## 7) Output Schema

| Year | Ship_Avg | Ship_High | Ship_Low | Brent_Avg | Brent_High | Brent_Low | WTI_Avg | WTI_High | WTI_Low | Dubai_Avg | Dubai_High | Dubai_Low |

---

## 8) Validation

Compare against:
- World Bank oil price
- OPEC basket

Tolerance:
- ±5–10% annually

Check major events:
- 1998 crash
- 2008 spike
- 2014 decline
- 2020 collapse

---

## 9) Assumptions

- Fixed weights
- Constant adjustment (-5)
- Benchmarks represent global trade
- Daily prices approximate transactions

---

## 10) Limitations

- No refinery margin modeling
- No bunker fuel direct pricing
- WTI inland distortions not corrected

---

## 11) Implementation (Pseudo-code)

```python
df["shipping"] = 0.5*brent + 0.3*dubai + 0.2*wti
df["shipping_adj"] = df["shipping"] - 5

annual = df.groupby("year").agg({
    "shipping_adj": ["mean", "max", "min"],
    "brent": ["mean", "max", "min"],
    "wti": ["mean", "max", "min"],
    "dubai": ["mean", "max", "min"]
})
```

---

## 12) Methodology Statement

Global shipping oil prices are estimated using a weighted blend of Brent (50%), Dubai (30%), and WTI (20%) daily spot prices from the EIA. A constant adjustment approximates heavier crude and bunker fuel characteristics. Annual statistics are computed from daily observations.
