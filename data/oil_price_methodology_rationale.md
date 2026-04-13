# Global Shipping Oil Price Dataset – Methodology Rationale

## Overview

This document explains the reasoning behind the construction of a global oil price proxy designed to approximate **shipping-relevant fuel costs** from 1995–2024. The goal is not to perfectly replicate any single published index, but to create a **transparent, defensible, and practically useful approximation**.

---

## 1) Why No Single Global Oil Price Exists

Oil is not a uniform commodity. Prices vary based on:

- **Quality** (light vs heavy crude)
- **Sulfur content** (sweet vs sour)
- **Geography** (transport costs and logistics)
- **Market structure** (regional supply/demand)

Because of this, there is no true “global price.” Instead, markets rely on **benchmarks**.

---

## 2) Why Multiple Benchmarks Are Required

Three benchmarks were selected to represent global oil markets:

- Brent → Global seaborne trade
- WTI → North American production and inland pricing
- Dubai → Middle East and Asia-bound flows

### Rationale
- Shipping is a **global activity**
- Oil flows between continents
- A single benchmark (e.g., WTI) introduces regional bias

---

## 3) Why Brent Is Weighted Most Heavily

Brent is the dominant benchmark for internationally traded crude because:

- It is **waterborne** (not landlocked)
- It reflects **global marginal pricing**
- It is widely used in contracts across Europe, Africa, and Asia

Thus, it receives the highest weight in the model.

---

## 4) Why Dubai Is Included

Dubai captures:

- Middle Eastern exports
- Asia-bound oil flows (China, India)

This is critical because:

- Asia is the largest oil demand center
- Shipping routes are heavily tied to these flows

---

## 5) Why WTI Still Matters

Despite being landlocked:

- The U.S. is one of the largest producers globally
- Gulf Coast refining and exports influence global pricing
- WTI impacts spreads and arbitrage conditions

Thus, it is included at a lower weight.

---

## 6) Why Fixed Weights Were Used

Weights were set to:

- Brent: 50%
- Dubai: 30%
- WTI: 20%

### Rationale
- Simple and transparent
- Stable across time
- Avoids overfitting or reliance on incomplete trade data

Dynamic weighting would increase complexity without clear benefit for a supplemental dataset.

---

## 7) Why a Shipping Adjustment Is Applied

Shipping fuel is not crude oil—it is derived from:

- Heavy crude
- Residual fuel oil (bunker fuel)

These are typically cheaper than light crude.

### Adjustment:
- Subtract a constant value (−$5/barrel)

### Purpose:
- Approximate heavy crude discount
- Improve relevance to shipping cost modeling

---

## 8) Why Daily Data Is Used

Daily data enables:

- Accurate annual highs and lows
- Better capture of volatility
- Avoidance of smoothing effects from monthly averages

This is critical for:
- Risk analysis
- Understanding extreme events (e.g., 2008, 2020)

---

## 9) Why Annual Aggregation Is Still Used

Despite using daily data:

- The final dataset is annual for simplicity
- Suitable for:
  - macro models
  - long-term trend analysis
  - integration into other datasets

---

## 10) Why External Benchmarks Are Used for Validation

Two key references:

- World Bank oil price
- OPEC basket price

### Role:
- Not targets
- Used to confirm:
  - trend alignment
  - reasonable price levels

### Acceptable deviation:
- ±5–10%

---

## 11) Why This Approach Fits Shipping Analysis

Shipping costs are influenced by:

- Global oil flows (not regional isolation)
- Heavy fuel usage
- Trade route dynamics

This model captures:

- Global pricing structure (via Brent)
- Regional demand (via Dubai)
- Production influence (via WTI)
- Fuel type realism (via adjustment)

---

## 12) Key Tradeoffs

### What is gained:
- Simplicity
- Transparency
- Reproducibility
- Broad global representation

### What is sacrificed:
- Refinery-level precision
- Exact bunker fuel pricing
- Dynamic trade flow modeling

---

## 13) Final Positioning

This dataset should be understood as:

> A **practical global proxy for shipping-relevant oil prices**, grounded in real market structure but simplified for analytical use.

It is:
- More realistic than a single benchmark
- More transparent than institutional composites
- Sufficiently accurate for cross-country and longitudinal analysis

---

## 14) Summary

- No true global oil price exists
- Multiple benchmarks are required
- Brent anchors global trade
- Dubai captures Asia
- WTI captures U.S. influence
- A small adjustment improves shipping realism
- External indices validate but do not define the model

