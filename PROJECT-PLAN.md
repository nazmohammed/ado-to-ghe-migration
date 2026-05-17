# Project Plan: Migrate 95 Azure DevOps Subscriptions → GitHub Enterprise

## 1. Executive Summary

Migrate **95 Azure DevOps (ADO) organizations** (one per VSE/Azure subscription) into a consolidated **GitHub Enterprise Cloud (EMU)** tenant linked to Microsoft Entra ID. Scope covers Git repos, pipelines, work items, artifacts, wikis, service connections, identities, and governance.

**Strategy:** Factory-model, wave-based migration using GitHub Enterprise Importer (GEI), GitHub Actions Importer, and Entra ID-driven EMU provisioning. Migration teams run parallel waves; central platform team owns tooling, governance, and cutover.

---

## 2. Guiding Principles

1. **Identity first** — EMU + Entra SSO/SCIM before any repo moves.
2. **Factory model** — repeatable, scripted, idempotent migrations.
3. **Wave-based** — 5–8 ADO orgs per wave; parallelize within waves.
4. **Zero data loss** — full history, PRs, attachments, LFS preserved.
5. **Read-only freeze, then cutover** — no dual-write windows.
6. **Comms first** — owners and developers know exactly what changes and when.

---

## 3. Target Architecture

```
Microsoft Entra ID (tenant)
  ├── SCIM → GitHub EMU Enterprise
  │            ├── Org: <business-unit-1>
  │            ├── Org: <business-unit-2>
  │            └── ... (consolidated from 95 ADO orgs)
  ├── SAML SSO
  └── App registrations for OIDC → Azure deployments

GitHub Actions
  └── self-hosted runners (Azure VMSS) + GitHub-hosted runners
        └── OIDC federation → Azure subscriptions (replaces service connections)
```

**Org consolidation decision:** Map 95 ADO orgs to a smaller number of GHE orgs by business unit / line-of-business (target ~10–20 GHE orgs). Decision matrix completed in Phase 1.

---

## 4. Workstreams

| # | Workstream | Lead | Output |
|---|------------|------|--------|
| WS1 | Program Management | PMO | Schedule, RAID log, status |
| WS2 | Identity & Access | IAM team | EMU + SCIM + SSO live |
| WS3 | Platform / Tooling | Platform Eng | GEI factory, runbooks, runners |
| WS4 | Repo Migration | Migration Pod (×N) | Repos in GHE per wave |
| WS5 | CI/CD Migration | DevEx team | Actions workflows live |
| WS6 | Work Items & Boards | App teams + scripts | Issues/Projects migrated |
| WS7 | Artifacts & Packages | Build team | GitHub Packages cutover |
| WS8 | Security & Compliance | InfoSec | Advanced Security, scanning, policies |
| WS9 | Communications & Training | Change Mgmt | Comms plan, training, office hours |
| WS10 | Decommission | IT Ops | ADO orgs archived/closed |

---

## 5. Phases & Timeline (relative)

### Phase 0 — Mobilize
- Stand up program, RACI, tooling licenses, EMU enterprise provisioned.

### Phase 1 — Discovery & Design
- Inventory all 95 ADO orgs (repos, pipelines, work items, users, artifacts, integrations).
- Org consolidation mapping (95 ADO → N GHE orgs).
- Wave planning (complexity score → wave assignment).
- Define naming conventions, repo topology, branch protection baseline.
- Identity mapping: ADO user → Entra UPN → EMU handle.

### Phase 2 — Foundation Build
- EMU + SCIM + SSO operational.
- GHE orgs created with baseline policies (rulesets, CODEOWNERS template, default branch).
- Migration factory: GEI scripts parameterized, secrets vaulted, dashboards built.
- Self-hosted runner pools deployed (Azure VMSS, autoscale).
- OIDC trust to Azure subscriptions established.
- Pilot wave (3 low-risk ADO orgs) — end-to-end validation.

### Phase 3 — Pilot Wave (Wave 0)
- 3 orgs, end-to-end including pipelines + work items.
- Capture lessons, refine runsheet, update tooling.
- **Gate:** pilot retrospective → approval to scale.

### Phase 4 — Production Waves
- ~12 waves × ~8 orgs/wave (adjustable). Each wave follows the standard runsheet (Section 7).
- Parallel pods (3–4 migration pods running waves concurrently after Wave 1).

### Phase 5 — Stabilization & Decommission
- Mannequin reclamation complete.
- ADO orgs archived (read-only), then deleted after retention window (e.g., 90 days).
- VSE entitlements re-validated; GHE license trueup.

### Phase 6 — Close-out
- Final reporting, lessons learned, runbook handover to BAU.

---

## 6. Wave Planning Model

**Complexity score per ADO org** (1–5 each):
- Repo count & size (incl. LFS)
- Pipeline count & complexity (classic vs YAML)
- Work item volume
- Number of integrations / service connections
- Active user count
- Regulatory sensitivity

Score → wave bucket:
- **Wave 0 (Pilot):** lowest complexity, willing teams.
- **Waves 1–4:** low-medium.
- **Waves 5–9:** medium-high.
- **Waves 10–12:** highest (regulated, largest, most integrations).

Each wave = ~8 ADO orgs, ~5 business days end-to-end.

---

## 7. Standard Wave Runsheet (per wave, repeatable)

> Times are **relative offsets** within the wave (Day D-X / D / D+X). No calendar dates.

### D-10 — Wave Kickoff
| # | Activity | Owner | Output / Gate |
|---|----------|-------|---------------|
| 1 | Confirm wave scope (orgs, repos, pipelines, work items) | Wave Lead | Wave manifest signed off |
| 2 | Identify org admins, repo owners, on-call SMEs per org | Wave Lead | Contact matrix |
| 3 | Send T-10 comms (announce migration, dates, impact) | Comms | Email + Teams post |
| 4 | Verify identity mapping CSV for wave users | IAM | Mapping file in repo |

### D-7 — Pre-Flight
| # | Activity | Owner | Output / Gate |
|---|----------|-------|---------------|
| 5 | Run GEI `inventory-report` for each ADO org in wave | Platform | Inventory CSVs |
| 6 | Run `gh actions-importer audit azure-devops` per org | DevEx | Audit reports |
| 7 | Identify TFVC repos → schedule Git conversion | Migration Pod | TFVC list |
| 8 | Identify oversize repos / LFS → plan large object handling | Migration Pod | LFS plan |
| 9 | Generate per-org migration script (`gh ado2gh generate-script`) | Platform | `migrate-<org>.ps1` |
| 10 | Stage secrets (ADO PAT, GH PAT) in Key Vault, fetched at run | Platform | Vault refs |
| 11 | Pre-create target GHE orgs/repos shells (if not exist) | Platform | Org URLs |
| 12 | Define branch protection ruleset to apply post-migration | Platform | Ruleset JSON |

### D-5 — Dry Run
| # | Activity | Owner | Output / Gate |
|---|----------|-------|---------------|
| 13 | Execute **dry-run** migration into sandbox GHE org | Migration Pod | Dry-run logs |
| 14 | Validate repo content, history, PR count, attachments | Migration Pod | Validation report |
| 15 | `gh actions-importer dry-run` per pipeline | DevEx | Workflow YAML drafts |
| 16 | Work items export dry-run (ADO REST → JSON) | Apps Pod | WI JSON dumps |
| 17 | Resolve dry-run defects, update scripts | Platform | Re-tested scripts |

### D-3 — T-3 Comms & Final Checks
| # | Activity | Owner | Output / Gate |
|---|----------|-------|---------------|
| 18 | T-3 reminder comms to all wave users | Comms | Sent |
| 19 | Confirm EMU accounts provisioned for all wave users | IAM | Account list verified |
| 20 | Confirm self-hosted runner capacity for wave | Platform | Runner pool status |
| 21 | Confirm rollback plan & owner per org | Wave Lead | Rollback doc |
| 22 | Go/No-Go meeting | Steering | **GATE: Go/No-Go** |

### D-1 — Freeze Eve
| # | Activity | Owner | Output / Gate |
|---|----------|-------|---------------|
| 23 | Send T-1 final notice ("freeze tomorrow at HH:MM") | Comms | Sent |
| 24 | Verify backups of ADO orgs (project export) | Platform | Backup IDs |
| 25 | Disable scheduled pipelines in ADO | DevEx | Disabled list |

### D-0 — Cutover Day

**Block A — Freeze (T+00:00)**
| # | Activity | Owner | Output / Gate |
|---|----------|-------|---------------|
| 26 | Set ADO repos to **read-only** (deny contribute on default branch + all branches) | ADO Admin | Repos frozen |
| 27 | Stop/disable all ADO pipelines | DevEx | Pipelines off |
| 28 | Announce freeze in progress | Comms | Notice posted |

**Block B — Migrate Repos (T+00:30)**
| # | Activity | Owner | Output / Gate |
|---|----------|-------|---------------|
| 29 | Execute `migrate-<org>.ps1` for each org in wave (parallel) | Migration Pod | GEI migration IDs |
| 30 | Monitor GEI migration status (`gh ado2gh wait-for-migration`) | Migration Pod | All `SUCCEEDED` |
| 31 | Spot-check repos: commit count, latest SHA, PR count, LFS | Migration Pod | Checklist signed |
| 32 | Apply branch protection rulesets via API | Platform | Rulesets active |
| 33 | Apply repo topics, default branch, CODEOWNERS template | Platform | Repo settings applied |

**Block C — Migrate Pipelines (T+02:00)**
| # | Activity | Owner | Output / Gate |
|---|----------|-------|---------------|
| 34 | `gh actions-importer migrate` for each pipeline | DevEx | Workflow PRs opened |
| 35 | Recreate secrets as Actions secrets / OIDC bindings | DevEx | Secrets set |
| 36 | Merge workflow PRs, trigger validation run | DevEx | Green run per repo |
| 37 | Re-enable schedules (if any) | DevEx | Scheduled runs visible |

**Block D — Work Items & Wiki (T+04:00)**
| # | Activity | Owner | Output / Gate |
|---|----------|-------|---------------|
| 38 | Run WI migration script (ADO → Issues/Projects) | Apps Pod | Issues created |
| 39 | Map area paths → labels, iterations → milestones, states | Apps Pod | Mapping applied |
| 40 | Migrate wiki to repo Markdown or GHE wiki | Apps Pod | Wiki live |

**Block E — Artifacts & Integrations (T+05:00)**
| # | Activity | Owner | Output / Gate |
|---|----------|-------|---------------|
| 41 | Republish NuGet/npm feeds to GitHub Packages | Build team | Feeds published |
| 42 | Update internal package consumers to new feed URLs | Build team | Consumers updated |
| 43 | Recreate webhooks (Jira, Teams, ServiceNow, etc.) | Integrations | Webhooks active |

**Block F — Validation (T+06:00)**
| # | Activity | Owner | Output / Gate |
|---|----------|-------|---------------|
| 44 | Repo owner smoke test (clone, branch, PR, merge) per repo | Repo Owners | Sign-off form |
| 45 | Pipeline smoke test (trigger build + deploy to non-prod) | DevEx | Green deploy |
| 46 | Reclaim mannequins (`gh ado2gh reclaim-mannequin`) | Platform | Mannequins reclaimed |
| 47 | Security scan baseline (CodeQL, secret scanning, Dependabot) | InfoSec | Scans enabled |

**Block G — Open for Business (T+08:00)**
| # | Activity | Owner | Output / Gate |
|---|----------|-------|---------------|
| 48 | Announce cutover complete; users may push to GHE | Comms | Go-live notice |
| 49 | Update IDE/CLI guidance, redirect docs | DevEx | Docs updated |
| 50 | On-call support pod active for 48h hypercare | Wave Lead | Hypercare rota |

### D+1 — Hypercare Day 1
| # | Activity | Owner | Output / Gate |
|---|----------|-------|---------------|
| 51 | Triage user issues (Teams channel + ticket queue) | Hypercare | Issue log |
| 52 | Daily standup, defect burn-down | Wave Lead | Standup notes |
| 53 | Verify nightly pipelines ran successfully | DevEx | Run report |

### D+3 — Hypercare End
| # | Activity | Owner | Output / Gate |
|---|----------|-------|---------------|
| 54 | Confirm zero P1/P2 open defects | Wave Lead | **GATE: Hypercare exit** |
| 55 | Wave retrospective | Wave Lead | Lessons log updated |

### D+7 — Wave Close
| # | Activity | Owner | Output / Gate |
|---|----------|-------|---------------|
| 56 | Archive ADO repos (set archived flag) | ADO Admin | Archived |
| 57 | Revoke ADO write permissions org-wide | ADO Admin | Permissions revoked |
| 58 | Update CMDB / inventory with new GHE URLs | IT Ops | CMDB updated |
| 59 | Wave closure report to steering | PMO | Report filed |

### D+90 — Decommission
| # | Activity | Owner | Output / Gate |
|---|----------|-------|---------------|
| 60 | Delete ADO orgs (after retention window) | ADO Admin | Orgs deleted |
| 61 | Release ADO licenses | Procurement | Licenses released |

---

## 8. Cross-Cutting Activities (program-level, not per wave)

| Activity | Owner | Cadence |
|----------|-------|---------|
| Steering committee | Sponsor + PMO | Weekly |
| RAID log review | PMO | Weekly |
| Migration metrics dashboard (repos done, defects, velocity) | Platform | Daily |
| Security & compliance review | InfoSec | Per wave gate |
| License & cost tracking | Procurement | Monthly |
| Training cohorts (Actions, GHAS, Copilot, Projects) | Change Mgmt | Bi-weekly |
| Office hours | DevEx | Twice weekly |

---

## 9. Tooling Inventory

| Tool | Purpose |
|------|---------|
| `gh-gei` | Repo migration (issues, PRs, attachments, history) |
| `gh-ado2gh` | ADO-specific helpers: inventory, script gen, mannequin reclamation, team migration, pipeline rewires |
| `gh-actions-importer` | Pipeline → Actions workflow conversion |
| Azure Key Vault | PAT and secret storage |
| Entra ID + SCIM | EMU identity provisioning |
| Azure Monitor / Log Analytics | Migration runner logs, audit |
| Custom WI migration script | ADO REST → GitHub Issues/Projects REST |
| Power BI / Grafana dashboard | Program metrics |
| ServiceNow / Jira | Defect & change tracking |

---

## 10. Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|-----------|
| TFVC repos in scope | High | Convert to Git in ADO pre-migration; allocate extra wave time |
| Large LFS / binary repos exceed GHE limits | High | Audit early; split, prune, or use Packages |
| Pipeline secrets not portable | Med | OIDC federation to Azure; secret remediation list per pipeline |
| Service connections / shared agents | Med | Inventory upfront; replace with self-hosted runners + OIDC |
| Identity mapping gaps (orphan authors) | Med | Mannequin reclamation cycle each wave; chase unmapped users |
| Work item fidelity loss | Med | Set expectations; preserve original ADO export as archive |
| Custom ADO extensions / processes | Med | Catalogue + find GH equivalent or accept gap |
| User resistance / change fatigue | Med | Strong comms, champions network, training, office hours |
| GEI rate limits at scale | Low | Stagger waves; multiple PATs; coordinate with GitHub support |
| Audit/regulatory continuity | High | Retain ADO read-only 90d; export audit logs to SIEM |

---

## 11. Success Metrics / KPIs

- 100% of in-scope repos migrated with history integrity verified.
- ≥ 95% of pipelines converted to Actions and green within hypercare.
- < 2% mannequins unreclaimed at wave close.
- Zero P1 data-loss incidents.
- Developer NPS ≥ baseline + 0 (no regression) post-migration.
- ADO licenses fully released within 30 days of program close.

---

## 12. Decisions Needed (open)

1. GHE org consolidation target count and naming convention.
2. EMU vs standard GHE Cloud (recommend **EMU** for 95-org consolidation).
3. Self-hosted runner topology (per-org, per-BU, or shared pools).
4. Work-item migration fidelity bar (full vs metadata-only vs archive-only).
5. Retention window for archived ADO orgs (recommend 90 days).
6. Wave size and concurrency (recommend 8 orgs/wave, up to 3 waves in flight).
