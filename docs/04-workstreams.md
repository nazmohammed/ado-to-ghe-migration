# 04. Workstreams

Ten workstreams run in parallel under one program.

| # | Workstream | Lead | Primary Output |
|---|------------|------|----------------|
| WS1 | Program Management | PMO | Schedule, RAID log, status, steering pack |
| WS2 | Identity & Access | IAM team | EMU + SCIM + SSO live; identity mapping CSV |
| WS3 | Platform / Tooling | Platform Eng | GEI factory, runbooks, dashboards, runner pools |
| WS4 | Repo Migration | Migration Pod (×N) | Repos in GHE per wave with history & PRs intact |
| WS5 | CI/CD Migration | DevEx team | Actions workflows live; OIDC to Azure |
| WS6 | Work Items & Boards | App teams + scripts | Issues/Projects migrated, mappings applied |
| WS7 | Artifacts & Packages | Build team | GitHub Packages cutover for NuGet/npm/etc. |
| WS8 | Security & Compliance | InfoSec | GHAS enabled, scanning baseline, audit export |
| WS9 | Communications & Training | Change Mgmt | Comms plan, training cohorts, office hours |
| WS10 | Decommission | IT Ops | ADO orgs archived, licenses released, CMDB updated |

## RACI Summary

| Activity | Sponsor | PMO | Platform | Migration Pod | Repo Owner | InfoSec |
|----------|---------|-----|----------|---------------|------------|---------|
| Wave Go/No-Go | A | R | C | C | C | C |
| Repo migration | I | I | C | R | C | I |
| Pipeline migration | I | I | C | R | C | I |
| Smoke test sign-off | I | I | I | C | R | I |
| Security baseline | I | I | C | I | C | R |
| ADO decommission | A | R | C | I | C | C |

R = Responsible, A = Accountable, C = Consulted, I = Informed.
