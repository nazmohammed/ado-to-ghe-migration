# Runsheet — Part 1: Pre-Wave (D-10 → D-1)

Times are **relative offsets** within the wave. No calendar dates.

## D-10 — Wave Kickoff

| # | Activity | Owner | Output / Gate |
|---|----------|-------|---------------|
| 1 | Confirm wave scope (orgs, repos, pipelines, work items) | Wave Lead | Wave manifest signed off |
| 2 | Identify org admins, repo owners, on-call SMEs per org | Wave Lead | Contact matrix |
| 3 | Send T-10 comms (announce migration, dates, impact) | Comms | Email + Teams post |
| 4 | Verify identity mapping CSV for wave users | IAM | Mapping file in repo |

## D-7 — Pre-Flight

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

## D-5 — Dry Run

| # | Activity | Owner | Output / Gate |
|---|----------|-------|---------------|
| 13 | Execute **dry-run** migration into sandbox GHE org | Migration Pod | Dry-run logs |
| 14 | Validate repo content, history, PR count, attachments | Migration Pod | Validation report |
| 15 | `gh actions-importer dry-run` per pipeline | DevEx | Workflow YAML drafts |
| 16 | Work items export dry-run (ADO REST → JSON) | Apps Pod | WI JSON dumps |
| 17 | Resolve dry-run defects, update scripts | Platform | Re-tested scripts |

## D-3 — T-3 Comms & Final Checks

| # | Activity | Owner | Output / Gate |
|---|----------|-------|---------------|
| 18 | T-3 reminder comms to all wave users | Comms | Sent |
| 19 | Confirm EMU accounts provisioned for all wave users | IAM | Account list verified |
| 20 | Confirm self-hosted runner capacity for wave | Platform | Runner pool status |
| 21 | Confirm rollback plan & owner per org | Wave Lead | Rollback doc |
| 22 | **Go/No-Go meeting** | Steering | **GATE: Go/No-Go** |

## D-1 — Freeze Eve

| # | Activity | Owner | Output / Gate |
|---|----------|-------|---------------|
| 23 | Send T-1 final notice ("freeze tomorrow at HH:MM") | Comms | Sent |
| 24 | Verify backups of ADO orgs (project export) | Platform | Backup IDs |
| 25 | Disable scheduled pipelines in ADO | DevEx | Disabled list |
