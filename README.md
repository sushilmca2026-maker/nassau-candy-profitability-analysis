# Product Line Profitability & Margin Performance Analysis for Nassau Candy Distributor

## Project overview

This repository turns the uploaded Nassau Candy Distributor transaction file into a reproducible profitability analysis and an interactive Streamlit dashboard. The project focuses on the distinction between sales scale and economic contribution. It identifies products and divisions that drive gross profit, products that carry margin risk, concentration dependencies, and factory-level performance.

All calculations use only `data/NassauCandyDistributor.csv`. No synthetic, demo, or hard-coded analytical records are used.

## Business problem

Sales volume alone can be misleading. A product may generate substantial revenue while absorbing disproportionate cost or contributing weak margin. Nassau Candy Distributor needs a consistent view of gross profit, margin, unit economics, concentration, and cost risk to support pricing, sourcing, and product portfolio decisions.

## Objectives

The project validates and cleans the transaction data, calculates product and division profitability metrics, classifies product risk transparently, measures revenue and profit concentration, connects products to the supplied factory mapping, and exposes the analysis through a premium dark-theme Streamlit dashboard.

## Dataset

The dataset contains 10,194 transaction rows and 18 source fields, including dates, geography, division, product, sales, units, gross profit, and cost. The uploaded file contains 15 products across Chocolate, Sugar, and Other divisions. The cleaning workflow parses dates with day-first semantics, validates positive sales and units, standardizes text labels, checks duplicates and missing values, and preserves an auditable profit reconciliation field.

## KPIs and methodology

| KPI | Definition |
|---|---|
| Gross Margin % | Gross Profit ÷ Sales × 100 |
| Profit per Unit | Gross Profit ÷ Units |
| Revenue Contribution % | Product Sales ÷ Total Sales × 100 |
| Profit Contribution % | Product Gross Profit ÷ Total Gross Profit × 100 |
| Margin Volatility | Standard deviation of transaction-level margin by product |

Products are classified with transparent rules based on portfolio medians. The dashboard preserves calculated `Margin Risk` and `Diagnostic` columns even when the current filter returns no rows, and it displays a clear empty-state message instead of failing.

## Dashboard features

The Streamlit application includes an executive overview, product profitability leaderboard, division performance, interactive cost-versus-margin diagnostics, revenue and profit Pareto views, factory analysis, product-to-factory mapping, date/division/region/factory/product filters, and validation evidence.

## Project structure

```text
app/streamlit_app.py              Streamlit dashboard
src/analysis.py                   Cleaning, metrics, classifications, aggregations
src/generate_outputs.py           Reproducible output generation
data/NassauCandyDistributor.csv  Uploaded source dataset
outputs/                          Cleaned data and analytical tables
docs/research_paper.md            Full analytical report
outputs/executive_summary.md      Stakeholder-facing summary
requirements.txt                  Runtime dependencies
```

## Installation

```bash
git clone <your-repository-url>
cd NassauCandyProfitability
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

## How to run

Regenerate the analytical outputs:

```bash
PYTHONPATH=src python src/generate_outputs.py
```

Launch the dashboard:

```bash
streamlit run app/streamlit_app.py
```

## Technologies

Python, Pandas, NumPy, Plotly, Streamlit, and Markdown are used. The analytical tables are generated with SQL-style group-and-aggregate logic in Pandas.

## Key insights from the uploaded data

The portfolio totals **$141,783.63 in sales**, **$93,442.80 in gross profit**, and **38,654 units**, producing a **65.9% blended gross margin**. Chocolate represents **92.9% of sales and 95.1% of gross profit**, making it both the primary engine and the principal portfolio dependency. Five of 15 products (33.3%) generate approximately 92.9% of revenue and 95.1% of gross profit, highlighting significant product concentration. The Other division has a lower blended margin of **44.8%**, led down by Kazookles at approximately **7.7%** product margin. Lot's O' Nuts is the strongest mapped factory by gross profit, while The Other Factory has the weakest mapped margin at approximately **11.9%**.

These findings are descriptive of this uploaded file and should not be generalized beyond the observed period without additional data.

## Future improvements

Future versions could add customer-level retention, price-volume-mix decomposition, shipment-lag diagnostics, supplier or purchase-order costs, scenario modeling for repricing, and automated refresh through a controlled data pipeline.
