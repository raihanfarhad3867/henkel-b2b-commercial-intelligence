# Power BI dashboard build guide | Phase 5

**Data classification:** independent portfolio exercise. P5 customer and distributor records are completely synthetic. Henkel published results are kept on a separate context page.

## Import and model

1. Import `P5_Synthetic_Experiment_Panel.csv` as `FactP5Months`.
2. Import `P5_Experiment_Design.csv` as `DimP5Experiment`.
3. Import `P5_Effect_Estimates.csv` as `FactP5EffectEstimates` (precomputed validation table). If using DAX to recompute DiD, display one or the other; don't sum duplicate estimates.
4. Import `P5_Management_Decision_Gates.csv` as `FactP5Gates`.
5. Create 1:* single-direction relationship from `DimP5Experiment[Experiment_ID]` to `FactP5Months[Experiment_ID]`. The experiment summary and gate tables can also relate as 1:1 to `DimP5Experiment`, if validated for uniqueness.
6. Keep `Henkel_Public_Data` and `P4_Sales_Ledger` separate. Do **not** connect account IDs across phases; the synthetic populations differ.
7. Set data types: financials as decimal; treatment price/volume effects as decimal percentages; period as categorical; simulation month as text.
8. Paste measures from `PowerBI_Phase5_Measures.dax`. Do not mix quarterly organic growth percentages with synthetic volume growth rates.

## Suggested six pages

1. **Executive decision:** five interventions, conditional screening results, approval gates, prominent synthetic watermark.
2. **Experiment portfolio:** intervention mechanism, eligible population, study type, assignment unit, owner and risks.
3. **Treatment vs comparison:** monthly contributions for each arm (small multiples), pre/post means, DiD and design limitations.
4. **Economic sensitivity:** low / base / high hypothetical scenarios; break-even efficacy factor and cost-of-trial details.
5. **Safety and rollout gates:** technical qualification, supply-service constraints, privacy/legal, sampling and sponsorship.
6. **Official Henkel context:** Q3 2026 business-unit results from verified Henkel source and separate explanation of price + volume. Never place official and synthetic euros on the same total.

## Visual decisions

- Show `Experiment_ID` slicer; default one experiment to avoid improperly aggregating overlapping models.
- Use positive/negative color plus explicit labels and a no-approval indicator.
- Label every P5 chart: `SIMULATED — NOT HENKEL OPERATIONAL DATA`.
- Label uncertainty: `Synthetic 90% account-resample interval; not real-world predictive interval`.
- Use P5 Source Ethics as a visible provenance page and not merely a hidden data sheet.

## Method and limitations

The model uses 12 treated and 12 comparison accounts per intervention, three synthetic pre months, three synthetic post months, and simple descriptive difference-in-differences. The 12-month extrapolation assumes persistence and contains no true-world validation. Effects are not causal estimates about Henkel, and the cohort sizes are not justified by a real statistical power analysis. Real design must account for eligibility, cluster assignment, spillovers, shared customers, trend comparability, quality, privacy, technical acceptance and marginal contribution.
