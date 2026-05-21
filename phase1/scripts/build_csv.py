"""Generate Phase 1 L3 task plan CSV."""
import csv

OUT = r"C:\Users\nazmohammed\.copilot\session-state\f7603c23-d320-431c-874f-087287e33674\files\ADO-to-GHE-Phase1-L3-Tasks.csv"

# Columns: Stage, ID, Task, Owner, Effort (p-days), Predecessors, Week, Workstream, Notes
ROWS = [
    # Stage 0 - Mobilise & Discovery (Weeks 1-2)
    ("S0", "0.1",  "Sponsor sign-off & charter",                                    "PM",                 1.0, "-",           "W1", "WS1", "Charter signed; budget approved."),
    ("S0", "0.2",  "RACI agreed",                                                   "PM",                 0.5, "0.1",         "W1", "WS1", ""),
    ("S0", "0.3",  "Steering committee chartered, first meeting held",              "PM",                 0.5, "0.1",         "W1", "WS1", "Weekly cadence agreed."),
    ("S0", "0.4",  "RAID log v1 published",                                         "PM",                 1.0, "0.1",         "W1", "WS1", ""),
    ("S0", "0.5",  "Comms plan signed off",                                         "Change Mgr",         2.0, "0.1",         "W1", "WS8", "T-10/T-3/T-1/D-0/D+1 templates."),
    ("S0", "0.6",  "Stakeholder & contact matrix (per repo)",                       "Change Mgr",         1.0, "0.1",         "W1", "WS8", ""),
    ("S0", "0.7",  "Pull ADO users from all 100 repos",                             "IAM",                1.0, "0.1",         "W1", "WS2", ""),
    ("S0", "0.8",  "Identity mapping CSV (ADO -> Entra UPN -> EMU)",                "IAM",                2.0, "0.7",         "W1", "WS2", "Drives EMU provisioning."),
    ("S0", "0.9",  "Inventory: gh ado2gh inventory-report per ADO org",             "Platform",           1.0, "0.1",         "W1", "WS3", ""),
    ("S0", "0.10", "Repo size + LFS audit",                                         "Platform",           1.0, "0.9",         "W1", "WS3", "Identify oversize repos early."),
    ("S0", "0.11", "Open PRs + open branches snapshot",                             "Platform",           1.0, "0.9",         "W2", "WS3", ""),
    ("S0", "0.12", "Pipeline inventory per repo (YAML vs Classic)",                 "DevEx",              2.0, "0.9",         "W2", "WS6", "Classic ratio drives Phase 2 sizing too."),
    ("S0", "0.13", "ADO branch policy inventory per repo",                          "Platform",           2.0, "0.9",         "W2", "WS7", "Input to ruleset design."),
    ("S0", "0.14", "ADO service connections & integrations inventory",              "DevEx",              1.0, "0.9",         "W2", "WS6", ""),
    ("S0", "0.15", "Complexity scoring per repo",                                   "Tech Lead",          1.0, "0.10-0.14",   "W2", "WS3", "1-5 across 6 factors."),
    ("S0", "0.16", "Wave assignment (Pilot + W1-W4)",                               "Tech Lead",          1.0, "0.15",        "W2", "WS3", "8 ADO orgs per wave target."),
    ("S0", "0.17", "Baseline ruleset JSON v1",                                      "InfoSec + Platform", 2.0, "0.13",        "W2", "WS7", "Default-branch ruleset template."),
    ("S0", "0.18", "CODEOWNERS template",                                           "Platform",           0.5, "-",           "W2", "WS7", ""),
    ("S0", "0.19", "M1 gate: steering sign-off on wave plan & risks",               "PM + Sponsor",       0.5, "0.16, 0.17",  "W2", "WS1", "GATE M1."),

    # Stage 1 - Identity & Foundation (Weeks 3-4)
    ("S1", "1.1",  "EMU enterprise shell created",                                  "IAM",                1.0, "0.19",        "W3", "WS2", ""),
    ("S1", "1.2",  "Break-glass admin accounts configured",                         "IAM",                1.0, "1.1",         "W3", "WS2", ""),
    ("S1", "1.3",  "SAML SSO configured with MoJ Entra ID",                         "IAM",                2.0, "1.1",         "W3", "WS2", "Critical path."),
    ("S1", "1.4",  "SCIM endpoint configured",                                      "IAM",                1.0, "1.3",         "W3", "WS2", ""),
    ("S1", "1.5",  "SCIM mapping (Entra attributes -> GHE)",                        "IAM",                1.0, "1.4",         "W3", "WS2", ""),
    ("S1", "1.6",  "SCIM dry-run with 10 test users",                               "IAM",                1.0, "1.5",         "W4", "WS2", ""),
    ("S1", "1.7",  "SCIM full provisioning sweep",                                  "IAM",                1.0, "1.6",         "W4", "WS2", ""),
    ("S1", "1.8",  "UAT: SSO login + access for 10 users",                          "Tech Lead",          1.0, "1.7",         "W4", "WS2", ""),
    ("S1", "1.9",  "Target GHE orgs pre-created (1:1 with ADO orgs)",               "Platform",           1.0, "1.1",         "W3", "WS3", ""),
    ("S1", "1.10", "Migration workstation provisioned (gh, gh-gei, gh-ado2gh)",     "Platform",           0.5, "-",           "W3", "WS3", ""),
    ("S1", "1.11", "Key Vault for migration secrets",                               "Platform",           1.0, "-",           "W3", "WS3", ""),
    ("S1", "1.12", "ADO PAT + GH PAT issued and vaulted",                           "Platform + IAM",     0.5, "1.11",        "W3", "WS3", ""),
    ("S1", "1.13", "Parameterised GEI migration script template",                   "Platform",           2.0, "1.10",        "W3", "WS3", ""),
    ("S1", "1.14", "Ruleset application script (apply JSON to any repo)",           "Platform",           1.0, "0.17, 1.9",   "W4", "WS7", ""),
    ("S1", "1.15", "Migration tracking dashboard (Power BI / Grafana)",             "Platform",           2.0, "-",           "W4", "WS3", ""),
    ("S1", "1.16", "Sandbox GHE org for dry-runs",                                  "Platform",           0.5, "1.9",         "W4", "WS3", ""),
    ("S1", "1.17", "End-to-end factory smoke test (1 throwaway repo)",              "Migration Pod",      1.0, "1.13, 1.14",  "W4", "WS3", ""),
    ("S1", "1.18", "M2 gate: identity + factory ready",                             "Sponsor + IAM + TL", 0.5, "1.8, 1.17",   "W4", "WS1", "GATE M2."),

    # Stage 2 - Pilot Wave (Weeks 5-6)
    ("S2", "2.1",  "Pilot scope confirmed (5 repos, owners on board)",              "PM",                 0.5, "1.18",        "W5", "WS1", ""),
    ("S2", "2.2",  "T-10 / T-3 / T-1 comms to pilot users",                         "Change Mgr",         1.0, "2.1",         "W5", "WS8", ""),
    ("S2", "2.3",  "Dry-run pilot migration into sandbox",                          "Migration Pod",      1.0, "1.17, 2.1",   "W5", "WS4", ""),
    ("S2", "2.4",  "Validate dry-run",                                              "Migration Pod",      0.5, "2.3",         "W5", "WS4", "Commits, branches, PRs, attachments."),
    ("S2", "2.5",  "Pilot Go/No-Go meeting",                                        "Steering",           0.5, "2.4",         "W5", "WS1", ""),
    ("S2", "2.6",  "Freeze pilot ADO repos (read-only)",                            "ADO Admin",          0.5, "2.5",         "W6", "WS9", ""),
    ("S2", "2.7",  "Execute pilot migration (5 repos)",                             "Migration Pod",      1.0, "2.6",         "W6", "WS4", ""),
    ("S2", "2.8",  "Apply rulesets to pilot repos",                                 "InfoSec",            0.5, "2.7",         "W6", "WS7", ""),
    ("S2", "2.9",  "Apply CODEOWNERS to pilot repos",                               "Platform",           0.5, "2.7",         "W6", "WS7", ""),
    ("S2", "2.10", "Install Azure Boards GitHub App on GHE pilot org",              "Platform + ADO Admin", 0.5, "1.9",       "W6", "WS5", ""),
    ("S2", "2.11", "Connect Boards App to ADO org + projects",                      "Platform + ADO Admin", 0.5, "2.10",      "W6", "WS5", ""),
    ("S2", "2.12", "Test AB#123 linking on commit",                                 "DevEx",              0.5, "2.11",        "W6", "WS5", ""),
    ("S2", "2.13", "Test AB# linking on PR + auto-state-transition on merge",       "DevEx + Apps SME",   1.0, "2.12",        "W6", "WS5", ""),
    ("S2", "2.14", "Install Azure Pipelines GitHub App on GHE org",                 "Platform",           0.5, "1.9",         "W6", "WS6", ""),
    ("S2", "2.15", "Re-point pilot pipelines (5-10 pipelines, YAML)",               "DevEx",              2.0, "2.7, 2.14",   "W6", "WS6", ""),
    ("S2", "2.16", "Validate build + release end-to-end",                           "DevEx + Owners",     1.0, "2.15",        "W6", "WS6", ""),
    ("S2", "2.17", "Mannequin reclamation for pilot",                               "Platform",           1.0, "2.7",         "W6", "WS4", ""),
    ("S2", "2.18", "Repo owner smoke tests & sign-off",                             "Repo Owners",        0.5, "2.7-2.9",     "W6", "WS4", ""),
    ("S2", "2.19", "Hypercare D+1 -> D+3",                                          "Wave Lead + Pods",   2.0, "2.7",         "W6", "WS10", ""),
    ("S2", "2.20", "Archive pilot ADO repos (D+7)",                                 "ADO Admin",          0.5, "2.19",        "W6", "WS9", ""),
    ("S2", "2.21", "Pilot retrospective + runsheet update",                         "PM",                 1.0, "2.19",        "W6", "WS1", ""),
    ("S2", "2.22", "M3 gate: pilot accepted, scale authorised",                     "Steering",           0.5, "2.21",        "W6", "WS1", "GATE M3."),
]

# Add Stage 3 - Production Waves 1-4 (each ~14 p-days, repeated 4x)
for wave_num in range(1, 5):
    wk = "W7" if wave_num <= 2 else "W8" if wave_num == 3 else "W9"
    ROWS.extend([
        ("S3", f"W{wave_num}.1",  f"Wave {wave_num} manifest confirmed (repos, owners, pipelines)", "Wave Lead",          0.5, "M3 / prev wave hypercare exit", wk, "WS1",  ""),
        ("S3", f"W{wave_num}.2",  f"Wave {wave_num} T-10 / T-3 / T-1 comms",                        "Change Mgr",         1.0, f"W{wave_num}.1",                  wk, "WS8",  ""),
        ("S3", f"W{wave_num}.3",  f"Wave {wave_num} dry-run migration into sandbox",                "Migration Pod",      1.0, f"W{wave_num}.1",                  wk, "WS4",  ""),
        ("S3", f"W{wave_num}.4",  f"Wave {wave_num} dry-run validation",                            "Migration Pod",      0.5, f"W{wave_num}.3",                  wk, "WS4",  ""),
        ("S3", f"W{wave_num}.5",  f"Wave {wave_num} Go/No-Go meeting",                              "Steering",           0.5, f"W{wave_num}.4",                  wk, "WS1",  ""),
        ("S3", f"W{wave_num}.6",  f"Freeze wave {wave_num} ADO repos",                              "ADO Admin",          0.5, f"W{wave_num}.5",                  wk, "WS9",  ""),
        ("S3", f"W{wave_num}.7",  f"Execute wave {wave_num} migration (25 repos parallel)",         "Migration Pod",      1.0, f"W{wave_num}.6",                  wk, "WS4",  ""),
        ("S3", f"W{wave_num}.8",  f"Apply rulesets + CODEOWNERS for wave {wave_num}",               "InfoSec + Platform", 0.5, f"W{wave_num}.7",                  wk, "WS7",  ""),
        ("S3", f"W{wave_num}.9",  f"Verify Boards integration on wave {wave_num} repos",            "DevEx",              0.5, f"W{wave_num}.7",                  wk, "WS5",  ""),
        ("S3", f"W{wave_num}.10", f"Re-point pipelines for wave {wave_num} (~25-50 pipelines)",     "DevEx",              3.0, f"W{wave_num}.7",                  wk, "WS6",  ""),
        ("S3", f"W{wave_num}.11", f"Validate builds for wave {wave_num}",                           "DevEx + Owners",     1.0, f"W{wave_num}.10",                 wk, "WS6",  ""),
        ("S3", f"W{wave_num}.12", f"Mannequin reclamation wave {wave_num}",                         "Platform",           1.0, f"W{wave_num}.7",                  wk, "WS4",  ""),
        ("S3", f"W{wave_num}.13", f"Repo owner smoke tests & sign-off wave {wave_num}",             "Repo Owners",        1.0, f"W{wave_num}.7, .8",              wk, "WS4",  ""),
        ("S3", f"W{wave_num}.14", f"Hypercare wave {wave_num} D+1 -> D+3",                          "Wave Lead + Pods",   2.0, f"W{wave_num}.7",                  wk, "WS10", ""),
        ("S3", f"W{wave_num}.15", f"Archive wave {wave_num} ADO repos (D+7)",                       "ADO Admin",          0.5, f"W{wave_num}.14",                 wk, "WS9",  ""),
        ("S3", f"W{wave_num}.16", f"Wave {wave_num} closure report",                                "Wave Lead",          0.5, f"W{wave_num}.14",                 wk, "WS1",  ""),
    ])

# Stage 4 - Stabilisation & Close (Week 10)
ROWS.extend([
    ("S4", "4.1",  "Final mannequin reclamation sweep across all waves", "Platform",     1.0, "All Wn.12",     "W10", "WS4",  ""),
    ("S4", "4.2",  "Boards linking audit (sample of >=20 repos)",        "DevEx",        1.0, "All Wn.9",      "W10", "WS5",  ""),
    ("S4", "4.3",  "Pipeline pass-rate audit",                           "DevEx",        1.0, "All Wn.11",     "W10", "WS6",  ""),
    ("S4", "4.4",  "Security baseline audit",                            "InfoSec",      1.0, "All Wn.8",      "W10", "WS7",  ""),
    ("S4", "4.5",  "All ADO repos confirmed archived; write perms revoked", "ADO Admin", 1.0, "All Wn.15",     "W10", "WS9",  ""),
    ("S4", "4.6",  "CMDB / asset inventory updated to GHE URLs",         "IT Ops",       1.0, "4.5",           "W10", "WS9",  ""),
    ("S4", "4.7",  "Phase 1 closure report",                             "PM",           2.0, "4.1-4.6",       "W10", "WS1",  ""),
    ("S4", "4.8",  "Lessons learned session & publish",                  "Change Mgr",   1.0, "4.7",           "W10", "WS8",  ""),
    ("S4", "4.9",  "Phase 2 mandate pack (Actions migration)",           "PM + TL",      2.0, "4.7",           "W10", "WS1",  ""),
    ("S4", "4.10", "M5 gate: Phase 1 closed",                            "Sponsor + Steering", 0.5, "4.7, 4.9", "W10", "WS1", "GATE M5."),
])

# Write CSV
with open(OUT, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["Stage", "ID", "Task", "Owner", "Effort (p-days)", "Predecessors", "Week", "Workstream", "Notes"])
    for r in ROWS:
        w.writerow(r)

total = sum(r[4] for r in ROWS)
print(f"Saved: {OUT}")
print(f"Rows: {len(ROWS)}")
print(f"Total effort: {total} p-days")
