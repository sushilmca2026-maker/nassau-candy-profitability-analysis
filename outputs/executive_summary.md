# Executive Summary

## Purpose

This analysis evaluates product-line profitability for Nassau Candy Distributor using the uploaded transaction dataset. It separates sales scale from gross-profit contribution and identifies concentration and margin risks that can inform pricing, sourcing, and product portfolio review.

## Portfolio position

The validated file contains **10,194 transactions**, **15 products**, and **3 divisions**. The portfolio generated **$141,783.63 in sales**, **$93,442.80 in gross profit**, and **38,654 units**, producing a **65.9% blended gross margin**. No rows were removed during validation, and no missing values or duplicate rows were found.

## Principal findings

Chocolate is the portfolio's dominant economic engine. It represents **92.9% of sales** and **95.1% of gross profit**, while its blended margin is **67.4%**. The Other division has the weakest blended margin at **44.8%**. Sugar has a healthy observed margin of **66.6%**, but its contribution is only **0.3% of sales**, so its strategic impact is limited in this file.

Five products account for approximately **95.1% of gross profit** and reach more than 80% of revenue. This concentration creates a dependency risk: supply interruptions, cost inflation, or pricing mistakes affecting the leading chocolate products could materially reduce total profit.

Kazookles is the clearest margin-risk product. It generates **$1,205.75 in sales** but only **$92.75 in gross profit**, equivalent to a **7.7% gross margin**. The product should receive a pricing and cost review before any portfolio decision is made. The mapped **Other Factory** also has the weakest factory-level margin at approximately **11.9%**, although factory comparisons are influenced by product mix and scale.

## Recommended actions

Management should protect availability and cost discipline for the five leading profit products. It should then launch a focused margin-recovery review for Kazookles and the broader Other division, testing price realization, manufacturing cost, and sourcing alternatives. Portfolio removal should be considered only after demand, substitution, and strategic assortment effects are assessed.

The organization should maintain a concentration watchlist and review the leading products on a recurring basis. It should also reconcile the source-system shipment dates, which appear to fall two to four years after the order dates in this file, before using the data for logistics or service-level decisions.

## Decision-use note

These findings are descriptive of the uploaded dataset. The analysis does not include discounts, returns, inventory carrying costs, supplier terms, demand elasticity, or customer-level strategic value. The accompanying Streamlit dashboard allows stakeholders to test date, division, region, factory, product, and margin filters interactively.
