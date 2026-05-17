# Runsheet — Part 2: Cutover Day (D-0)

## Block A — Freeze (T+00:00)

| # | Activity | Owner | Output / Gate |
|---|----------|-------|---------------|
| 26 | Set ADO repos to **read-only** (deny contribute on default branch + all branches) | ADO Admin | Repos frozen |
| 27 | Stop/disable all ADO pipelines | DevEx | Pipelines off |
| 28 | Announce freeze in progress | Comms | Notice posted |

## Block B — Migrate Repos (T+00:30)

| # | Activity | Owner | Output / Gate |
|---|----------|-------|---------------|
| 29 | Execute `migrate-<org>.ps1` for each org in wave (parallel) | Migration Pod | GEI migration IDs |
| 30 | Monitor GEI migration status (`gh ado2gh wait-for-migration`) | Migration Pod | All `SUCCEEDED` |
| 31 | Spot-check repos: commit count, latest SHA, PR count, LFS | Migration Pod | Checklist signed |
| 32 | Apply branch protection rulesets via API | Platform | Rulesets active |
| 33 | Apply repo topics, default branch, CODEOWNERS template | Platform | Repo settings applied |

## Block C — Migrate Pipelines (T+02:00)

| # | Activity | Owner | Output / Gate |
|---|----------|-------|---------------|
| 34 | `gh actions-importer migrate` for each pipeline | DevEx | Workflow PRs opened |
| 35 | Recreate secrets as Actions secrets / OIDC bindings | DevEx | Secrets set |
| 36 | Merge workflow PRs, trigger validation run | DevEx | Green run per repo |
| 37 | Re-enable schedules (if any) | DevEx | Scheduled runs visible |

## Block D — Work Items & Wiki (T+04:00)

| # | Activity | Owner | Output / Gate |
|---|----------|-------|---------------|
| 38 | Run WI migration script (ADO → Issues/Projects) | Apps Pod | Issues created |
| 39 | Map area paths → labels, iterations → milestones, states | Apps Pod | Mapping applied |
| 40 | Migrate wiki to repo Markdown or GHE wiki | Apps Pod | Wiki live |

## Block E — Artifacts & Integrations (T+05:00)

| # | Activity | Owner | Output / Gate |
|---|----------|-------|---------------|
| 41 | Republish NuGet/npm feeds to GitHub Packages | Build team | Feeds published |
| 42 | Update internal package consumers to new feed URLs | Build team | Consumers updated |
| 43 | Recreate webhooks (Jira, Teams, ServiceNow, etc.) | Integrations | Webhooks active |

## Block F — Validation (T+06:00)

| # | Activity | Owner | Output / Gate |
|---|----------|-------|---------------|
| 44 | Repo owner smoke test (clone, branch, PR, merge) per repo | Repo Owners | Sign-off form |
| 45 | Pipeline smoke test (trigger build + deploy to non-prod) | DevEx | Green deploy |
| 46 | Reclaim mannequins (`gh ado2gh reclaim-mannequin`) | Platform | Mannequins reclaimed |
| 47 | Security scan baseline (CodeQL, secret scanning, Dependabot) | InfoSec | Scans enabled |

## Block G — Open for Business (T+08:00)

| # | Activity | Owner | Output / Gate |
|---|----------|-------|---------------|
| 48 | Announce cutover complete; users may push to GHE | Comms | Go-live notice |
| 49 | Update IDE/CLI guidance, redirect docs | DevEx | Docs updated |
| 50 | On-call support pod active for 48h hypercare | Wave Lead | Hypercare rota |
