# Reproducibility guide

## Standard-library pipeline
Requires Python 3.10+; no `pip install` needed to reproduce the Python analytics outputs.

From the repository root:

```bash
python scripts/validate_repository.py
python scripts/reproduce_all.py
python -m unittest discover -s tests -v
```

Generated results are written to **untracked** `outputs/channel`, `outputs/phase4`, `outputs/phase5`.

The channel engine consumes the exported, unchanged values of the original `Simulated_Channel_Data` worksheet. Phase 4 and Phase 5 regenerate fictional scenarios from code; Phase 5 uses a fixed seed. The DAX measures and Excel reports are supplied for review, but are not executed by Python.

## Notebook usage
Open `notebooks/01_...` to `05_...` from the repository root in Jupyter; alternatively open them in VS Code. They use Python standard library. Notebook outputs are empty in source control to prevent accidental publication of local paths or misleading stale results.

## Excel
Open `dashboards/excel/Henkel_APC_Complete_Portfolio_Phase5.xlsx`. All prior research and synthetic sheets are included. Do not overwrite the file when regenerating CSVs; the pipelines are deliberately independent.

## Power BI
Follow `dashboards/powerbi/README.md`, then use Power BI Desktop to import CSVs and create a report. No finished `.pbix` is included.

## Verification scope
Automated checks validate schemas, labels, selected reported numerical transcriptions, arithmetic reconciliation, and synthetic row counts. They do not independently authenticate source PDFs or prove real-life market opportunity estimates. Read the linked primary sources for those claims.
