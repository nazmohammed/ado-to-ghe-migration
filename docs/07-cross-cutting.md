# 07. Cross-Cutting Activities

Recurring program-level activities that run continuously, independent of any single wave.

| Activity | Owner | Cadence |
|----------|-------|---------|
| Steering committee | Sponsor + PMO | Weekly |
| RAID log review | PMO | Weekly |
| Migration metrics dashboard (repos done, defects, velocity) | Platform | Daily |
| Security & compliance review | InfoSec | Per wave gate |
| License & cost tracking | Procurement | Monthly |
| Training cohorts (Actions, GHAS, Copilot, Projects) | Change Mgmt | Bi-weekly |
| Office hours | DevEx | Twice weekly |
| Champions network sync | Change Mgmt | Bi-weekly |
| Tooling backlog grooming | Platform | Weekly |
| Defect triage (cross-wave) | Hypercare lead | Daily during active waves |

## Steering Committee Agenda (standing)

1. Program health dashboard (red/amber/green).
2. Wave status: in flight, upcoming, recently closed.
3. Open risks and decisions requested.
4. Budget and license burn vs. plan.
5. Escalations and blockers.

## Defect Severity Definitions

| Severity | Definition | Response SLA |
|----------|------------|--------------|
| P1 | Data loss or full org outage in GHE | Immediate, all-hands |
| P2 | Critical workflow broken for many users (e.g., pipelines failing) | Same business day |
| P3 | Workflow degraded for some users; workaround exists | Within 3 business days |
| P4 | Minor issue, cosmetic, or documentation | Backlog, next release |
