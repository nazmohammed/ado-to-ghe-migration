# Runsheet — Part 3: Hypercare & Close (D+1 → D+90)

## D+1 — Hypercare Day 1

| # | Activity | Owner | Output / Gate |
|---|----------|-------|---------------|
| 51 | Triage user issues (Teams channel + ticket queue) | Hypercare | Issue log |
| 52 | Daily standup, defect burn-down | Wave Lead | Standup notes |
| 53 | Verify nightly pipelines ran successfully | DevEx | Run report |

## D+3 — Hypercare End

| # | Activity | Owner | Output / Gate |
|---|----------|-------|---------------|
| 54 | Confirm zero P1/P2 open defects | Wave Lead | **GATE: Hypercare exit** |
| 55 | Wave retrospective | Wave Lead | Lessons log updated |

## D+7 — Wave Close

| # | Activity | Owner | Output / Gate |
|---|----------|-------|---------------|
| 56 | Archive ADO repos (set archived flag) | ADO Admin | Archived |
| 57 | Revoke ADO write permissions org-wide | ADO Admin | Permissions revoked |
| 58 | Update CMDB / inventory with new GHE URLs | IT Ops | CMDB updated |
| 59 | Wave closure report to steering | PMO | Report filed |

## D+90 — Decommission

| # | Activity | Owner | Output / Gate |
|---|----------|-------|---------------|
| 60 | Delete ADO orgs (after retention window) | ADO Admin | Orgs deleted |
| 61 | Release ADO licenses | Procurement | Licenses released |

## Rollback Triggers (during D-0 only)

If any of the following occur **before T+06:00 (Validation block)**, the wave lead may invoke rollback:

- GEI migration failures on > 25% of repos that cannot be resolved within 1 hour.
- Identity provisioning failure that blocks > 50% of users from accessing GHE.
- Data integrity discrepancy on a critical repo (missing branches, missing PRs, or wrong default branch).

**Rollback action:**

1. Halt remaining migrations.
2. Re-enable ADO write permissions (lift read-only).
3. Re-enable disabled ADO pipelines.
4. Communicate rollback to all wave users within 30 minutes.
5. Schedule incident review within 2 business days.

After T+06:00, defects are managed under hypercare rather than rollback.
