# Henkel Adhesive APC — Phase 5 Commercial Experimentation & Executive Strategy
**Independent portfolio project • 11 November 2026**

## Executive question
If Adhesive Technologies' growth is largely price-led in the latest reported quarter, which customer- and channel-level initiatives could contribute to durable, profitable growth, and how would a management team know whether the initiatives work?

## Official context, separate from experiments
Henkel's *Q3 2026 Quarterly Statement*, published 10 November 2026, reports Adhesive Technologies Q3 sales of **€3,027 million** and **7.9% organic sales growth**. Packaging & Consumer Goods (APC) achieved **9.8% organic sales growth**. Henkel's preliminary release dated 29 October 2026 described the Adhesive Technologies business-unit organic growth contribution as **+7.2 percentage points from pricing and +0.7 percentage points from volume**. The price/volume split is **not** APC-specific. Neither release provides fictional-account or distributor information.

Official Investor Relations source: https://www.henkel.com/investors-and-analysts/events/2026-q3

Preliminary price-volume release: https://www.henkel.com/press-and-media/press-releases-and-kits/2026-10-29-henkel-achieves-very-strong-organic-sales-growth-in-the-third-quarter-and-updates-outlook-for-2026-2272318

## Commercial hypothesis
Pricing is not inherently bad or unsustainable. In industrial B2B markets it may reflect technical differentiation, value realization, contracting or input cost recovery. But sustainable profitable growth requires assessing customer demand, retention, technical qualification, channel reach, and contribution margins. The project deliberately avoids claiming that Henkel's distributors are underperforming.

## What Phase 5 adds to Phases 1–4

- **Experiment portfolio:** five possible commercial interventions tied to the diagnostic hypotheses developed in Phase 4.
- **Synthetic pre/post panel:** 120 fictional accounts (12 treatment + 12 comparison per experiment) across six fictitious months, 720 observations.
- **Evaluation framework:** account-level mean monthly contribution, descriptive difference-in-differences (DiD), annualized contribution scenario, implementation cost, bootstrap range and decision gates.
- **Risk review:** selection bias, cluster spillovers, nonparallel demand trends, legal/quality risks, and forecasting uncertainty.
- **Executive recommendation:** approve data validation and experimental-design review before any pilot or rollout; do not treat simulation as actual results.

## Simulated economic screening

| Experiment | Mechanism | Annualized hypothetical net contribution | Synthetic decision screen |
|---|---|---:|---|
| EX-01 | Technical qualification recovery | +€4,077 | Conditional pilot design review |
| EX-02 | Distributor joint-selling enablement | +€1,542 | Conditional pilot design review |
| EX-03 | OTIF / delivery reliability recovery | +€2,515 | Conditional pilot design review |
| EX-04 | Value-selling coaching | +€1,707 | Conditional pilot design review |
| EX-05 | Paper-seal application expansion | −€1,808 | Hold under modeled assumptions |

The figures are fictional and depend on constructed treatment effects, assumed cost levels, 12-month persistence, and a simplified difference-in-differences design. **They are not forecasts, revenue opportunities, actual realized ROI, or estimates of Henkel's real business.** The five simulated programs should not be summed as an approved portfolio value; their populations and economic mechanisms could overlap in real deployment.

## Analytical method
For each experiment, calculate the mean contribution per account-month in treatment and comparison groups before and after the intervention. The descriptive DiD is:

`[(Treatment_post – Treatment_pre) – (Comparison_post – Comparison_pre)]`

A hypothetical annualized pre-cost contribution is `DiD × treated accounts × 12`, with the scenario net equal to that result less the assumed fixed program cost. A 90% resampled interval is computed across synthetic account-level changes. Neither a bootstrap interval nor DiD can establish real-world causal effectiveness without a credible identification design, sufficiently powered data and verified assumptions.

## Critical decision gates

1. **Commercial:** verify the customer need and baseline using permissioned CRM data and customer/partner evidence.
2. **Technical:** qualify products, manufacturing conditions, trial procedures and safety requirements.
3. **Measurement:** specify eligible unit, primary metric, comparator, duration, seasonality, account contamination and power analysis.
4. **Economic:** verify marginal contribution, discounts, working capital, technical support, customer cannibalization and costs.
5. **Governance:** obtain legal/privacy review, program sponsorship and approved customer interactions.
6. **Scale:** require repeatability and post-pilot monitoring before expanding.

## Suggested management discussion

- *Does the action solve a proven cause or simply correlate with lost sales?*
- *Is the unit of assignment a factory, customer, distributor, or product application?*
- *Which comparator is fair and analytically useful?*
- *Which leading indicators matter ahead of revenue—technical trial completion, OTIF, distributor activity or repeat orders?*
- *What risk, cost or adverse customer impact should stop the pilot?*
- *What minimum contribution margin and confidence would justify scaling?*

## Next steps with actual internal data (only if authorized)

**Days 1–30:** agree hypothesis and owner; audit CRM and fulfillment definitions; map baseline; confirm privacy and technical rules. **Days 31–60:** pre-register design, select feasible comparator and run limited diagnostic/pilot. **Days 61–90:** evaluate outcomes and uncertainty; review costs/guardrails; recommend scale, iterate or stop. These are a proposed plan, not an activity undertaken for Henkel.

## Reproducibility and source separation

Run `python run_phase5_engine.py` to regenerate P5 synthetic CSVs with seed `20261111`. The Phase 5 Excel workbook retains original Phase 1–4 tabs and adds derived analysis. It preserves the 1,440 original simulated channel rows, the 144-row Phase 4 sales ledger, and all values in the official public-data tab. The model does not include a genuine Henkel distributor/customer dataset, and no actual pilot has been executed.
