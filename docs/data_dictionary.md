# Data dictionary and unit conventions

| Domain | Representative files | Unit and important definitions | Data-status labels |
|---|---|---|---|
| Henkel finance | `data/official_financials/AT_Quarterly_Official_2024_2026.csv` | `AT_Sales_EUR_m` = EUR millions; `AT_Organic_Growth_pct` = year-over-year percent; `AT_Price_Contribution_pp` and `AT_Volume_Contribution_pp` = percentage points | `Official actual`, or explicit missing/derived disclosures |
| APC finance | `data/official_financials/APC_Quarterly_Official_2024_2026.csv` | Business-area sales EUR million; organic growth %; **APC price/volume is not disclosed** | Blank numerical cells plus `Not disclosed (APC)` |
| Margins | `data/official_financials/AT_Margins_Official_Availability.csv` | Adjusted EBIT in EUR million and adjusted EBIT margin % for **H1 or FY**, not an invented Q3 margin | Period-specific official/undisclosed |
| Market evidence | `data/desk_research/P2_Market_Evidence.csv` | Different metrics with explicit `Unit`, `Data_Period`, `Source_URL` | External market evidence; not Henkel sales |
| Account research | `data/desk_research/P3_Account_Research.csv` | Public manufacturer/site observations; application relevance hypotheses | No assumed real customer relationship |
| Channel ledger | `data/synthetic/channel/Simulated_Channel_Data_Original_1440_Rows.csv` | Revenue `Net_Sales_EUR` = EUR, quantity `Units_Sold` = arbitrary simulated units; `Month_Start` originally Excel date serial, use Year/Month_Number | `SIMULATED – NOT HENKEL DATA` |
| Phase 4 | `data/synthetic/phase4/*.csv` | `Volume_kg_SIM`, `Net_Sales_EUR_SIM_CALC`, bridge EUR; accounts and reason flags fictional | `SIMULATED — NOT HENKEL CUSTOMER OR DISTRIBUTOR DATA` |
| Phase 5 | `data/synthetic/phase5/*.csv` | Synthetic contributions and annualized net EUR scenario; program costs assumed | `SIMULATED — NOT HENKEL CUSTOMER OR DISTRIBUTOR DATA` |

**Missing versus zero:** A blank or `Not disclosed` value is not 0. Never impute undisclosed APC price, volume, distributor revenue or margin. Phase 1 contains direct official URLs for source verification.
