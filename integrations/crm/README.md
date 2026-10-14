# NEXORA CRM Integration — Technical Decision & Implementation Plan

**Status:** Evaluation / design only. No production deployment or external outreach authorized.

## Business goal
Give NEXORA Growth one operational source of truth for acquiring restaurant clients in Egypt, beginning with El Zarqa and Damietta. This is an internal sales tool and must remain separate from customer-facing products `nexora-qr` and `nexora-platform`.

## Candidate assessment (desk research)

### Candidate A — Frappe CRM
Repository: https://github.com/frappe/crm
- Public repo describes CRM for sales teams, lead/deal activity timeline, Kanban pipeline, customizable views, tasks/notes, and self-hosting.
- Likely quickest path if the desired experience is a ready-made sales CRM.
- Deployment adds Frappe framework/site maintenance and needs a host where the approved stack can run.
- Need verify current stable image/API/auth, API support for custom fields, import semantics, and license obligations before committing.

### Candidate B — Twenty
Repository: https://github.com/twentyhq/twenty
- Public repo describes a customizable open-source CRM with objects, fields, views, workflows/agents, app development and Docker Compose self-hosting. Stack described in README: TypeScript/NestJS, PostgreSQL, Redis and React.
- Stronger fit if NEXORA wants a code-defined data model and future custom application.
- More operational complexity for our small initial outbound workflow; verify API and edition limitations before final selection.

### Recommendation
**Run a gated proof of concept with Frappe CRM first**, and keep Twenty as the fallback if integration tests or UX customization fail. Do not deploy either publicly until the POC passes and the owner approves a hosting target/cost. Do not write to a production CRM yet.

## Scope for the POC
1. Inspect/import an anonymized subset (10 rows) from the existing lead workbook.
2. Dry-run importer first: report create/update/skip/duplicate/invalid counts without making changes.
3. Test CSV import/export manually before building a custom API adapter.
4. Validate API access, authentication, custom fields, activity creation and idempotent update behavior in a disposable sandbox.
5. Only after POC pass: approve target environment; then implement production-safe adapter behind a feature flag.

## Data model
### Lead / Organization
- Business name (required)
- Normalized business name (derived)
- Region: El Zarqa / Damietta City / New Damietta / other
- Category
- Public business phone (optional; preserve leading zero as a string)
- Public website/social URLs
- Source URL and source label
- Last verified at, verification status (unverified / partially verified / verified / stale)
- QR menu, website, POS status (unknown / exists / missing / needs verification)
- Decision maker / role (only when lawfully and appropriately collected)
- Observed need (evidence) vs suspected need (explicitly separate)
- Lead score and scoring rationale
- Owner/assignee
- Next action and due date
- Notes and last contact outcome
- Do-not-contact / opt-out flag and reason
- Created/updated/imported timestamps

### Activities
Record calls, visits, replies, follow-ups, demo preparation, demo delivery, proposal, win/loss. Do not store secrets or unnecessary personal data.

## Pipeline mapping (preserve current business terms)
1. Lead جديد
2. تم التواصل
3. وافق على التجربة
4. جاري تجهيز Demo
5. Demo اتبعت
6. متابعة
7. عميل متعاقد
8. لم يكتمل

Do not conflate 'contacted' with 'qualified'. Track qualification evidence separately.

## Required views
- Kanban by pipeline stage
- High-priority leads (with evidence, not assumptions)
- Follow-ups due / overdue
- Unverified and stale data
- By region and category
- Demo in preparation / sent
- Won / not completed

## Metrics
Total leads; verified leads; attempted contacts; responses; positive replies; qualified opportunities; demos agreed/prepared/sent; proposals; wins; conversion rates by stage; follow-up overdue count; average time between stages; revenue (only when recorded); source-to-win performance.

## Import and sync safeguards
- Initial import source: `NEXORA_Restaurant_Leads_ElZarqa_Damietta.xlsx`.
- Dry-run and export backup required before every write.
- Deduplication hierarchy: normalized phone when present + normalized business name + region; flag ambiguous matches for human review instead of destructive merge.
- Idempotent import; no duplicate activity creation on retry.
- Preserve phone numbers as strings; do not infer missing leading zero unless the row has trustworthy evidence.
- Every imported row retains source and verification status. Public-directory data is not marked verified by default.
- Audit log includes run ID, timestamp, row counts and redacted errors.
- Secrets stored only in environment or secret manager, never repository files.
- No automatic WhatsApp/SMS/email in POC. Draft only. Any outbound execution requires a separately approved workflow.
- No paid hosting, paid plan or domain purchase without explicit approval.

## Test plan
- Unit tests for normalization and duplicate matching.
- Mapping tests for stages, regions and status enums.
- Invalid-row handling; preserve error report, don't silently skip.
- Repeat import produces zero duplicate records/activities.
- Round-trip CSV export preserves Arabic text, leading zeros and statuses.
- API auth and authorization tests.
- Manual acceptance of board views and follow-up workflow.
- Backup/restore and rollback procedure.

## Acceptance criteria
- Side-by-side evaluation note completed.
- Disposable sandbox POC works.
- Dry-run report is accurate, repeatable and non-mutating.
- Import/export retains all required fields.
- Owner signs off on environment, security and the write operation before any live import.
- No outreach, paid spend, or public deployment triggered by this work.

## Next execution
1. Confirm available local/workspace execution route and runtime.
2. Set up only a local/disposable sandbox for candidate Frappe CRM.
3. Test import/export and API against anonymized sample data.
4. Record pass/fail evidence and decision; only then propose the production integration.