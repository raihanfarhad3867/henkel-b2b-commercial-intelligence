# Power BI dashboard — Phase 4 build specification

All commercial customer/account/price/opportunity data is **SIMULATED**. A banner reading `SIMULATED TRAINING DATA — NOT HENKEL COMMERCIAL DATA` must be shown on every synthetic report page.

## Page 1 — Executive diagnostic
Cards: simulated 9M 2026 sales, YoY percentage, closed win rate, number of cases with negative volume change, screened expected contribution (assumption-based). Clustered bars: volume and realized-price bridge. Filters: end market, region, case ID.

## Page 2 — Where is growth dropping?
Monthly sales & kg by synthetic case. Matrix: account, revenue YoY, volume YoY, price effect, volume effect, contribution. Sort by volume effect. Tooltips disclose time windows and source status. Show data-quality warning if groups include mismatched periods.

## Page 3 — Win/loss & pipeline
Won/Lost/Open opportunity funnel (not every Open opportunity is expected to close). Win rate based on closed only; count of synthetic reasons by market; use treemap or bar. Include a `Reason is CRM hypothesis until validated` note.

## Page 4 — Root-cause evidence
Evidence table with case, observation, source type, counter-hypothesis, confidence and next verification. Visual cross-filter from case slicer. Do not convert synthetic signal statements into verified real-world findings.

## Page 5 — Intervention economics
Scenario alternatives table: incremental kg, success probability, price, variable cost, channel cost, trial, enablement, discount leakage, expected net contribution, break-even probability and approval gate. What-if controls are optional; assumptions must remain visible. Profitability is contribution, not official EBIT.

## Page 6 — Commercial decision queue
Filtered highest positive option (or HOLD) by case; evidence required, owner role to assign after review, next meeting checkpoint, pilot metrics. Include scenario-overlap and decision-gate warnings. Sum of screened values is NOT a forecast.

## Page 7 — Verified Henkel context (separate, disconnected)
Official Q3 2026 Adhesive Technologies sales and growth; Packaging & Consumer Goods growth; links to Henkel Investor Relations. This is an external reference page and must not relate to synthetic account facts. Keep periods, metrics and currency distinct.

## Model/relationship tips
- Use `DimCase` case filter to avoid cross-joining multiple fact tables.
- Avoid active relationships between separate fact tables; use one-way star schema.
- Connect a date dimension to monthly sales. Opportunity dates need separate inactive links or role-playing dates if analyzed by time.
- Validate totals in Power BI against `P4_Run_Results.json`, specifically €322,790, €291,163, −€41,490, +€9,863 and 50% closed win rate.
