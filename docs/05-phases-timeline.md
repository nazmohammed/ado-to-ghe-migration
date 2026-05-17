# 05. Phases & Timeline

Phases are sequential at the program level. Within Phase 4, multiple waves run concurrently.

## Phase 0 — Mobilize

- Stand up program, RACI, tooling licenses.
- Provision EMU enterprise shell.
- Set up comms channels (Teams, mailing lists, status page).
- Stand up program dashboards.

**Exit gate:** sponsor sign-off, budget approved, EMU enterprise created.

## Phase 1 — Discovery & Design

- Inventory all 95 ADO orgs (repos, pipelines, work items, users, artifacts, integrations).
- Identify TFVC repos that must be converted to Git pre-migration.
- Org consolidation mapping (95 ADO → N GHE orgs).
- Wave planning with complexity scoring.
- Define naming conventions, repo topology, branch protection baseline.
- Identity mapping: ADO user → Entra UPN → EMU handle.

**Exit gate:** consolidation map and wave plan approved by steering.

## Phase 2 — Foundation Build

- EMU + SCIM + SSO operational and tested.
- GHE orgs created with baseline policies (rulesets, CODEOWNERS template, default branch).
- Migration factory: GEI scripts parameterized, secrets vaulted, dashboards built.
- Self-hosted runner pools deployed (Azure VMSS, autoscale).
- OIDC trust to Azure subscriptions established.
- End-to-end test against a throwaway ADO org.

**Exit gate:** end-to-end factory test green; pilot wave authorized.

## Phase 3 — Pilot Wave (Wave 0)

- 3 orgs, end-to-end including pipelines and work items.
- Capture lessons, refine runsheet, update tooling.

**Exit gate:** pilot retrospective → approval to scale.

## Phase 4 — Production Waves

- ~12 waves × ~8 orgs/wave (adjustable).
- Each wave follows the standard runsheet (see `docs/runsheet/`).
- Parallel pods (3–4 migration pods running waves concurrently after Wave 1).

**Exit gate (per wave):** hypercare exit with zero P1/P2 open defects.

## Phase 5 — Stabilization & Decommission

- Mannequin reclamation complete across all waves.
- ADO orgs archived (read-only), then deleted after retention window (e.g., 90 days).
- VSE entitlements re-validated; GHE license trueup.

**Exit gate:** all ADO orgs archived; all critical defects closed.

## Phase 6 — Close-out

- Final reporting, lessons learned, runbook handover to BAU.
- License release confirmation, financial close.

**Exit gate:** program closure report accepted by sponsor.
