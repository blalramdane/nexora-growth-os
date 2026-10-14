# CRM POC Runbook — safe dry run

## Current state
The importer is **dry-run only**. It does not call Frappe CRM or write to any CRM. This lets us validate the workbook mapping and duplicate detection before the live API integration exists.

## Requirements
- Python 3.10+
- `openpyxl` for XLSX input (`python -m pip install openpyxl`)
- No CRM credentials needed.

## Run tests
From this folder:
```powershell
python -m unittest -v
```

## Run dry-run against the current lead workbook
```powershell
python -m pip install openpyxl
python poc_importer.py "C:\path\to\NEXORA_Restaurant_Leads_ElZarqa_Damietta.xlsx" --report crm-import-dry-run.json
```
The report is written locally. It contains lead data, so do not commit it to GitHub or share it publicly.

## Expected report
- `create_candidates`: valid unique rows for later review only
- `update_candidates`: always 0 until CRM matching/API is implemented
- `skipped_duplicates`: duplicates detected inside the input file
- `invalid`: rows missing required business name or region
- `mutations_performed`: always 0

## Important constraints
- Phone numbers are strings; leading zeros must survive.
- Similar records are flagged, not merged automatically.
- Public-listing records remain unverified.
- This POC intentionally has no API token handling and no outbound messaging.
- Do not commit the JSON report because it contains business contact data.
- Before API integration, validate Frappe CRM stable branch (README states `main - v1.x` is stable; `develop` is unstable), custom-field mapping, authentication and retry/idempotency in a disposable sandbox.
- Production import, hosting, external contact and spend require separate owner approval.
