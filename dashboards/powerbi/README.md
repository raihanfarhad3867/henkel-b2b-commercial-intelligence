# Power BI implementation — source assets, not a completed .pbix

This repository contains **CSV datasets, DAX measures and dashboard blueprints**, not a finished interactive `.pbix` report. Power BI Desktop is required for assembly. Examples are based on independent portfolio simulations.

## Recommended six-page structure
1. **Financial context (actual)** — 2024–2026 Adhesive Technologies and APC official figures; report period, units and source URL visible. Never show inferred APC price/volume.
2. **Growth-quality & scenario overview** — price/volume bridges and hypothetical scenario sensitivity in separate visual groups.
3. **Channel performance (synthetic)** — channel KPI drilldown, distributor segments and trends.
4. **Loss diagnostics (synthetic)** — client case 2025 vs 2026 bridges, win/loss reasons as hypothetical evidence.
5. **Customer/white-space research** — named companies are research units only; hypothetical sizing separated by tabs/labels.
6. **Experiment decision queue (synthetic)** — DiD calculations, assumed fixed costs, screen decisions and approval gates.

## Model safeguards
- Use explicit tables: `AT_Quarterly_Official`, `APC_Quarterly_Official`, `Channel_Synthetic`, `P4_Diagnostics_SIM`, `P5_Effect_Estimates_SIM`.
- **Do not create relationships** between official financial observations and invented account/distributor IDs.
- Show a visible page banner on synthetic pages: `SYNTHETIC PORTFOLIO DEMONSTRATION — NOT HENKEL DATA`.
- The original Phase 0 channel `Net_Sales_EUR` is EUR, whereas `AT_Sales_EUR_m` is EUR millions; don't combine without deliberate conversion, and never sum across evidence tiers.
- Organize the measures in `dax/` by phase; inspect each measure's table names against the imported CSVs before pasting it.
- See `phase4_diagnostics_blueprint.md` and `phase5_experiments_blueprint.md` for more detailed setup.
