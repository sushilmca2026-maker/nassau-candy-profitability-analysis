# Product Line Profitability & Margin Performance Analysis for Nassau Candy Distributor

## Abstract

This study analyzes the uploaded Nassau Candy Distributor transaction dataset to distinguish revenue scale from profitable growth. The analysis validates 10,194 rows, calculates gross margin and unit economics, ranks products and divisions, measures revenue and profit concentration, diagnoses cost and margin risk, and connects products to the supplied factory mapping. The portfolio generated $141,783.63 in sales and $93,442.80 in gross profit, equivalent to a 65.9% blended gross margin. Chocolate produced 92.9% of sales and 95.1% of profit. Five of 15 products (33.3%) generated approximately 92.9% of revenue and 95.1% of gross profit, indicating meaningful dependency on a narrow product set. The results support focused pricing and cost reviews for low-margin products while protecting the high-contribution chocolate portfolio.

## Introduction

For a distributor, sales volume is an incomplete measure of performance. Products with high revenue can still weaken the portfolio when their costs rise faster than their selling prices. A profitability view must therefore combine revenue, cost, gross profit, margin percentage, unit economics, and concentration. This project provides that view through a reproducible Python analysis and an interactive Streamlit application.

## Business Problem

The organization lacks a consistent way to answer four management questions: which products truly drive gross profit, whether high-sales products also deliver healthy margins, how profitability differs across divisions, and which products represent margin risk. Without these measures, pricing, sourcing, and rationalization decisions remain reactive.

## Dataset Description

The uploaded CSV contains 10,194 rows and 18 fields. The fields describe order and shipment dates, shipping mode, customer and geography, division, region, product, sales, units, gross profit, and cost. The data contains 15 products across three divisions: Chocolate, Sugar, and Other. Order dates span 1 January 2025 to 31 December 2025. The supplied shipment dates span 2027 to 2029, which creates an apparent date inconsistency; shipment dates were retained for traceability but the dashboard's main time filter uses Order Date.

## Data Cleaning

The workflow checks that all required fields exist, parses dates with day-first semantics, converts numeric fields safely, trims categorical labels, rejects missing or non-positive sales and units, detects duplicate rows, and records the number of removed records. In this file, all 10,194 rows passed the validation rules. There were no duplicate rows and no missing values after cleaning. A `Calculated Gross Profit` and `Profit Check Difference` field are also retained to make the supplied gross-profit calculation auditable.

## Exploratory Data Analysis

The cleaned data contains $141,783.63 in sales, $93,442.80 in gross profit, and 38,654 units. The resulting blended gross margin is 65.9%. The distribution is highly concentrated in Chocolate. Chocolate produces $131,692.90 in sales and $88,824.62 in gross profit, while Other produces $9,663.25 in sales and $4,333.45 in profit. Sugar is a small share of the file, with $427.48 in sales and $284.73 in gross profit.

## Profitability Methodology

For each transaction and aggregated product, gross margin is calculated as Gross Profit divided by Sales. Profit per unit is Gross Profit divided by Units. Revenue and profit contribution express each product's share of the filtered portfolio. Margin volatility is the standard deviation of transaction-level margin by product. Zero denominators are handled explicitly to prevent crashes. Product classifications use portfolio medians rather than arbitrary hard-coded thresholds: negative or zero margin, high sales and low margin, high profit and high margin, low sales and low profit, or monitor.

## Product Analysis

The five chocolate bars dominate the portfolio. Wonka Bar -Scrumdiddlyumptious leads gross profit at $19,357.50 with a 69.4% margin. Wonka Bar - Triple Dazzle Caramel follows with $18,610.20 and a 65.3% margin. Wonka Bar - Milk Chocolate contributes $17,443.37 at a 64.9% margin. Wonka Bar - Nutty Crunch Surprise combines a 71.3% margin with $16,819.95 of gross profit, making it the strongest unit-margin product among the major revenue products.

The main margin-risk products are concentrated outside the core chocolate bars. Lickable Wallpaper generates $7,860.00 in sales but a 50.0% margin. Kazookles is particularly weak, with $1,205.75 in sales, $92.75 in profit, and a 7.7% margin. Wonka Gum generates a small $597.50 in sales at a 52.0% margin. The evidence supports a pricing and cost review rather than an automatic discontinuation decision, because the dataset does not contain demand elasticity or strategic assortment information.

## Division Analysis

| Division | Sales | Gross Profit | Gross Margin | Revenue Contribution | Profit Contribution |
|---|---:|---:|---:|---:|---:|
| Chocolate | $131,692.90 | $88,824.62 | 67.4% | 92.9% | 95.1% |
| Other | $9,663.25 | $4,333.45 | 44.8% | 6.8% | 4.6% |
| Sugar | $427.48 | $284.73 | 66.6% | 0.3% | 0.3% |

Chocolate is both the strongest division and the largest dependency. Other has a materially lower margin and should receive the first diagnostic attention. Sugar shows a healthy aggregate margin but its very small scale limits the confidence of strategic conclusions.

## Pareto Analysis

Five products are required to reach approximately 80% of revenue, with cumulative revenue reaching 92.9% at that point. The same five products reach 95.1% of gross profit. This means the portfolio's profit concentration is at least as high as its revenue concentration. Operational interruptions, cost shocks, or pricing errors affecting those five chocolate products could therefore have an outsized impact on total profit.

## Cost Diagnostics

The dashboard provides sales-versus-cost and cost-versus-margin scatter plots. The most important diagnostic outlier is Kazookles, which combines low margin with meaningful cost relative to its sales. The Other division as a whole has a 44.8% margin, below Chocolate and Sugar. Risk flags are generated from observed portfolio medians and are recalculated for the active dashboard selection. The dashboard also ensures that the `Margin Risk` and `Diagnostic` columns are always available before table rendering.

## Factory Analysis

| Factory | Sales | Gross Profit | Gross Margin | Products |
|---|---:|---:|---:|---:|
| Lot's O' Nuts | $76,340.15 | $52,771.05 | 69.1% | 3 |
| Wicked Choccy's | $55,352.75 | $36,053.57 | 65.1% | 2 |
| Secret Factory | $8,587.50 | $4,344.70 | 50.6% | 3 |
| The Other Factory | $1,282.25 | $152.25 | 11.9% | 2 |
| Sugar Shack | $220.98 | $121.23 | 54.9% | 5 |

Lot's O' Nuts has the highest mapped sales and gross profit. The Other Factory has a structurally weak mapped margin, driven by products including Kazookles and Hair Toffee. Factory comparisons should be interpreted together with product mix because factories have different product counts and very different sales scales.

## Key Findings

The portfolio is profitable at an aggregate level, but it is not diversified. Chocolate supplies nearly all the observed economic contribution. The five leading products are the central profit engine. Kazookles is the clearest margin-risk product in the current data, and the Other division is the weakest division by blended margin. The factory mapping reinforces that The Other Factory deserves cost and pricing attention, while Lot's O' Nuts and Wicked Choccy's should be protected from avoidable supply disruption.

## Business Recommendations

Management should first establish a recurring review for the five products that generate most profit. The review should track price, cost, volume, availability, and customer mix so that the company can protect the portfolio's profit engine without assuming that historical performance will persist.

The next action should be a targeted margin recovery plan for Kazookles and the Other division. The plan should compare current price realization with unit cost, test repricing options, and investigate supplier or manufacturing cost renegotiation. Discontinuation should remain a later-stage option after demand, strategic assortment, and substitution effects are evaluated.

The company should also create a concentration watchlist. Because five products account for approximately 95% of observed profit, inventory and sourcing controls for those products should receive priority. Finally, the apparent two-to-four-year gap between order and shipment dates should be reconciled with the source-system owner before shipment-lag or service-level decisions are made.

## Limitations

This analysis uses only the uploaded file. It does not include discounts, returns, customer acquisition costs, inventory carrying costs, supplier terms, capacity constraints, demand elasticity, or operational service outcomes. Gross profit is treated as the supplied measure of sales minus cost, with a reconciliation field included for auditability. The shipment dates appear inconsistent with the order dates and are therefore not used for the primary profitability period filter. The results are descriptive of the observed data and should not be treated as a forecast.

## Conclusion

The Nassau Candy Distributor file shows a high-margin portfolio whose economic performance is concentrated in five chocolate products and two principal chocolate factories. The most defensible near-term opportunity is to protect the core products while correcting the low-margin tail, especially Kazookles and the Other division. The accompanying dashboard makes these conclusions filterable and repeatable rather than dependent on a static one-time table.

## References

Streamlit Documentation — Streamlit, “Build and deploy data apps,” Streamlit Documentation.
Pandas Documentation — Pandas, “User Guide,” Pandas Documentation.
Python Documentation — Python Software Foundation, “Python Documentation.”
Plotly Documentation — Plotly, “Python Graphing Library Documentation.”
Nassau Candy Dataset — Dataset used for product sales, cost, profitability, and margin analysis.

[1]: https://pandas.pydata.org/docs/ "Pandas documentation"

[2]: https://plotly.com/python/ "Plotly Python documentation"

[3]: https://docs.streamlit.io/ "Streamlit documentation"
