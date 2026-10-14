# CRM Integration Decision Log

Date: 2026-10-14

## Current decision
Frappe CRM is the preferred proof-of-concept candidate, with Twenty retained as a fallback. This is not a production selection yet.

## Evidence checked
- NEXORA Growth repository README scopes this repository to sales/client acquisition and states no outreach, publishing, or paid spend without owner approval.
- phase-1/PHASE_1_STATUS.md says lead data must be re-verified before contact and no external action is authorized by the document alone.
- Official Frappe CRM README documents pipeline/Kanban, lead/deal activity timeline, notes/tasks/custom views and self-hosting.
- Official Twenty README documents customizable CRM objects/fields/views/workflows and Docker Compose self-hosting.

## Why start with Frappe
NEXORA currently needs repeatable lead qualification and follow-up, rather than a custom CRM product. A configured CRM is likely a shorter path, pending POC confirmation. Twenty remains viable if Frappe proves too restrictive.

## Gate before any production integration
1. Disposable sandbox and anonymized sample only.
2. Validate import/export, API/auth, custom fields, deduplication and repeat-run idempotence.
3. Inspect environment/hosting constraints and licensing.
4. Review evidence, rollback plan and cost.
5. Obtain explicit owner approval before production write, deployment, spend or outreach.

## Workspace limitation
The GitHub integration is available and the technical plan has been committed to this repository. The local Chat On Steroids execution bridge was unavailable during this turn, so CRM containers could not be launched or integration tests run here. No code has been deployed and no lead import was written to a CRM.
