# Research quality, provenance and release controls

## Evidence classification
- **Official actual:** dated figures directly attributable to public Henkel investor disclosures, with explicit period, unit and source.
- **Public market observation:** sourced third-party or company facts, not evidence of customer relationships or addressable Henkel revenue.
- **Derived:** transparent calculations from identified source figures; never described as independently reported.
- **Assumed:** user-defined economic or market scenarios, never forecasts.
- **Synthetic:** simulated customer, distributor, price, order, account and experimental observations; never actual Henkel operating performance.

## Reproducibility
Run the project from the repository root:

```bash
python scripts/validate_repository.py
python scripts/reproduce_all.py
python -m unittest discover -s tests -v
```

Generated outputs are written under `outputs/` and are excluded from version control. Keep code, documentation and source CSVs in sync.

## Commercial decision integrity
- Do not use the Adhesive Technologies price/volume split as a Packaging & Consumer Goods-specific split.
- Keep quarter, half-year and full-year margin metrics distinct.
- Do not designate publicly identified manufacturers as Henkel customers, competitor customers or qualified opportunities.
- Do not represent a modeled causal effect, bootstrap interval, or scenario contribution as a realized commercial impact.
- Keep the analytical limitations adjacent to every visual or recommendation.
- Require documented supplier authority, customer consent where appropriate, technical qualification, privacy, safety and competition review before any live commercial test.

## Public repository release checks
- Validate source links, publication dates, period labels, calculation methods and screenshots.
- Exclude personal correspondence, interview material, employee identities, confidential CRM exports and any non-public financial data.
- Keep copyrighted source reports as external links, not bundled copies.
- Ensure the Power BI implementation status is stated correctly: DAX and design resources are provided; no validated `.pbix` is claimed.
- Publish only analysis and assets that can be independently explained and reproduced.
