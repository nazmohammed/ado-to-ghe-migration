# Phase 1 — Effort Estimation & Plan
**Scope:** Migrate 100 ADO repos (Repos + PRs + commits) → GitHub Enterprise (EMU). Work items, Boards, and Release pipelines stay in Azure DevOps. Azure Boards GitHub App wires the two together. MoJ Entra ID authenticates both ends.

---

## 1. Assumptions

| # | Assumption |
|---|-----------|
| A1 | 100 ADO repos in scope; all Git (no TFVC). TFVC repos, if any, are converted to Git **before** Phase 1 starts. |
| A2 | Average repo: < 5 GB, < 500 open PRs, < 100 active contributors. Outliers handled case-by-case. |
| A3 | Total active users across 100 repos: ~500. |
| A4 | MoJ holds a GHE Enterprise (EMU) contract or will procure before Phase 1 kick-off. |
| A5 | MoJ Entra ID admin team can configure SAML SSO and SCIM provisioning to GHE. |
| A6 | ADO Pipelines & Releases remain in ADO; only the **source** is re-pointed to GitHub. |
| A7 | One GHE org per ADO org (1:1; no consolidation in Phase 1). |
| A8 | Existing ADO branch policies will be **re-implemented** as GHE rulesets (not migrated). |
| A9 | A pilot wave of ~5 low-risk repos precedes the 4 production waves. |
| A10 | Hypercare per wave = 3 business days; no new wave starts during another wave's D-0 → D+3. |
| A11 | Standard working hours; no out-of-hours surcharge built in. |
| A12 | All effort estimates exclude vendor lead-times (EMU provisioning, licence procurement). |

---

## 2. Pre-requisites

### 2.1 Commercial & Licensing
- [ ] GitHub Enterprise (EMU) contract signed and tenant provisioned.
- [ ] GHE seat count confirmed ≥ active user count (~500).
- [ ] Decision on GitHub Advanced Security (GHAS) — in or out for Phase 1.
- [ ] Optional: GitHub Copilot Business/Enterprise seats (if required).

### 2.2 Identity & Access
- [ ] MoJ Entra ID tenant admin available for SAML/SCIM setup.
- [ ] Identity mapping spreadsheet started (ADO user → Entra UPN → planned EMU handle).
- [ ] Service principal in Entra ID for SCIM provisioning to GHE.
- [ ] Break-glass admin accounts agreed for the GHE Enterprise.

### 2.3 Source-side (Azure DevOps)
- [ ] Project Collection Admin access on every ADO org in scope.
- [ ] PAT issued for migration service identity (scopes: code read, work items read, build read, identity read).
- [ ] Inventory of all 100 repos: owner, BU, size, PR counts, LFS usage, integrations.
- [ ] Inventory of all pipelines (YAML vs Classic) per repo.
- [ ] List of existing ADO branch policies per repo (for replication as rulesets).
- [ ] Approval to install **Azure Boards GitHub App** at ADO org level.

### 2.4 Target-side (GitHub Enterprise)
- [ ] GHE Enterprise (EMU) shell provisioned.
- [ ] Target GHE orgs pre-created (1:1 with ADO orgs).
- [ ] Repo naming convention agreed.
- [ ] Baseline ruleset JSON template approved (PR + N approvals + status checks + linear history + restrict push to default).
- [ ] CODEOWNERS template approved.

### 2.5 Tooling
- [ ] GitHub CLI + `gh-gei` + `gh-ado2gh` extensions installed on migration workstation(s).
- [ ] Azure Key Vault (or equivalent) for storing ADO PAT + GH PAT.
- [ ] Power BI / Grafana / spreadsheet dashboard for tracking migration progress.
- [ ] ServiceNow / Jira queue for defect tracking during hypercare.

### 2.6 Network & Connectivity
- [ ] Outbound HTTPS to `*.github.com`, `*.githubusercontent.com`, `api.github.com` permitted from migration workstation.
- [ ] If MoJ uses a proxy: proxy whitelist updated for the above endpoints.
- [ ] No IP allowlist on the GHE Enterprise that would block GEI workers.

### 2.7 Governance & Comms
- [ ] Sponsor identified and steering committee chartered.
- [ ] RAID log created.
- [ ] Comms plan signed off (T-10 / T-3 / T-1 / D-0 / D+1 templates).
- [ ] Pilot wave volunteers confirmed (3–5 repos, low-risk).
- [ ] Decision on whether to disable GitHub Issues per repo (since Boards stays in ADO).

### 2.8 Pipelines (Phase 1 in-scope: re-pointing only)
- [ ] **Azure Pipelines GitHub App** install approved on the GHE org(s).
- [ ] Service connection / GitHub App auth strategy agreed.
- [ ] List of pipelines that will switch source from Azure Repos → GitHub.
- [ ] Branch trigger inventory (which branches trigger which pipelines).

---

## 3. Duration Summary

**Phase 1 total calendar duration: 10 weeks** (with a realistic range of 8–12 weeks depending on environment readiness).

| Stage | Calendar Weeks |
|-------|---------------|
| Stage 0 — Mobilise & Discovery | 2 |
| Stage 1 — Identity & Foundation | 2 |
| Stage 2 — Migration Factory Build & Pilot Wave | 2 |
| Stage 3 — Production Waves (×4, partially overlapped) | 3 |
| Stage 4 — Stabilisation, Boards Integration Sign-off, Close-out | 1 |
| **Total** | **10** |

---

## 4. Effort Estimation Summary

**Total Phase 1 effort: ~150 person-days** (range 130–170 depending on environment friction).

### 4.1 By Workstream

| # | Workstream | Effort (p-days) |
|---|-----------|-----------------|
| WS1 | Program Management & PMO | 25 |
| WS2 | Identity & Access (EMU + SAML + SCIM) | 14 |
| WS3 | Platform / Migration Factory | 10 |
| WS4 | Repo Migration (Pilot + 4 waves) | 25 |
| WS5 | Azure Boards GitHub App Integration | 4 |
| WS6 | Pipeline Source Re-pointing | 20 |
| WS7 | Security, Policy & Rulesets | 7 |
| WS8 | Comms & Training | 15 |
| WS9 | Decommission Prep (read-only freeze) | 5 |
| WS10 | Hypercare (×5 waves) | 15 |
| WS11 | Contingency (10%) | 10 |
| | **Total** | **150** |

### 4.2 Team Composition (Phase 1)

| Role | FTE | Duration | Person-days |
|------|-----|----------|-------------|
| Program Manager | 0.5 | 10 weeks | 25 |
| Technical Lead / Architect | 1.0 | 10 weeks | 50 |
| IAM Engineer | 0.5 | 4 weeks (heavy) + 0.2 ongoing | 14 |
| Platform / Migration Engineer ×2 | 1.0 each | 8 weeks | 80 (combined) |
| DevEx Engineer (pipelines) | 0.7 | 6 weeks | 21 |
| InfoSec Engineer | 0.3 | 8 weeks | 12 |
| Change Manager / Comms | 0.3 | 10 weeks | 15 |

(Sum exceeds 150 because each role has some idle/overlap — practical capacity tends to be ~70% utilisation of nominal FTE.)

---

## 5. L1 Plan — Milestones

Five sequential stages with explicit exit gates.

| # | Milestone | Exit Gate | Calendar Week |
|---|----------|-----------|---------------|
| M1 | **Mobilise & Discovery complete** | Steering sign-off on scope, wave plan, risk register | End of Week 2 |
| M2 | **Identity Foundation live** | EMU + SAML + SCIM in production, ≥ 95% users provisionable | End of Week 4 |
| M3 | **Pilot Wave complete** | 5 repos migrated, Boards link verified, pipelines re-pointed, retrospective signed off | End of Week 6 |
| M4 | **Production Waves complete** | All 100 repos in GHE, all in-scope pipelines re-pointed and green | End of Week 9 |
| M5 | **Phase 1 closed** | Hypercare exited, ADO repos archived, lessons logged, Phase 2 mandate decision taken | End of Week 10 |

```
W1   W2   W3   W4   W5   W6   W7   W8   W9   W10
|----|----|----|----|----|----|----|----|----|----|
[ M1 Mobilise ]
          [ M2 Identity ]
                    [ M3 Pilot ]
                              [---- M4 Waves 1-4 ----]
                                                  [M5 Close]
```

---

## 6. L2 Plan — Workstream Activities by Stage

### Stage 0 — Mobilise & Discovery (Weeks 1–2)

| WS | Activity | Owner | Effort (p-days) |
|----|---------|-------|-----------------|
| WS1 | Charter, RACI, steering setup | PM | 2 |
| WS1 | RAID log creation & first review | PM | 1 |
| WS1 | Comms plan, templates, distribution lists | Change Mgr | 3 |
| WS2 | Identity mapping CSV (ADO users → Entra UPN) | IAM | 3 |
| WS3 | Inventory all 100 repos (size, PRs, LFS, integrations) | Platform | 3 |
| WS3 | Inventory all pipelines per repo (YAML vs Classic, triggers) | DevEx | 2 |
| WS3 | Inventory ADO branch policies per repo | Platform | 2 |
| WS7 | Baseline ruleset JSON definition | InfoSec + Platform | 2 |
| WS3 | Wave assignment (complexity scoring → 4 waves + pilot) | Tech Lead | 2 |

### Stage 1 — Identity & Foundation (Weeks 3–4)

| WS | Activity | Owner | Effort (p-days) |
|----|---------|-------|-----------------|
| WS2 | EMU enterprise shell configuration | IAM | 2 |
| WS2 | SAML SSO with MoJ Entra ID | IAM | 3 |
| WS2 | SCIM provisioning from Entra → GHE | IAM | 3 |
| WS2 | Identity UAT with 10 test users | IAM + Tech Lead | 2 |
| WS3 | Migration factory: parameterised GEI scripts | Platform | 3 |
| WS3 | Secret vaulting (ADO PAT, GH PAT in Key Vault) | Platform | 1 |
| WS3 | Migration tracking dashboard | Platform | 2 |
| WS3 | Sandbox GHE org for dry-runs | Platform | 1 |
| WS7 | Ruleset application script (apply baseline to any repo) | InfoSec + Platform | 1 |
| WS8 | T-10 / T-3 / T-1 / D-0 comms templates finalised | Change Mgr | 2 |

### Stage 2 — Pilot Wave (Weeks 5–6)

| WS | Activity | Owner | Effort (p-days) |
|----|---------|-------|-----------------|
| WS1 | Pilot wave kickoff & comms | PM + Change Mgr | 1 |
| WS4 | Dry-run pilot migration in sandbox | Migration Pod | 1 |
| WS4 | Execute pilot migration (5 repos) | Migration Pod | 2 |
| WS7 | Apply rulesets to pilot repos | InfoSec | 1 |
| WS5 | Install Azure Boards GitHub App on pilot org | Platform + ADO Admin | 1 |
| WS5 | Connect Boards App to ADO org/projects | Platform + ADO Admin | 1 |
| WS5 | Test AB#123 linking (commits, PRs, branches, merge) | DevEx + Repo Owners | 1 |
| WS6 | Install Azure Pipelines GitHub App on GHE org | Platform | 0.5 |
| WS6 | Re-point pilot pipelines (5–10 pipelines) | DevEx | 2 |
| WS6 | Validate end-to-end build + release | DevEx + Repo Owners | 1 |
| WS4 | Mannequin reclamation for pilot | Platform | 1 |
| WS10 | Hypercare (3 days) | Wave Lead | 2 |
| WS1 | Pilot retrospective + lessons captured | PM | 1 |

### Stage 3 — Production Waves 1–4 (Weeks 7–9)

Each wave = ~25 repos, ~5 days execution.

**Repeating pattern per wave:**

| WS | Activity | Effort per wave (p-days) |
|----|---------|--------------------------|
| WS1 | Wave kickoff + comms | 1 |
| WS4 | Dry-run in sandbox | 1 |
| WS4 | D-0 execute migration (25 repos in parallel) | 1 |
| WS7 | Apply rulesets | 0.5 |
| WS6 | Re-point pipelines for wave repos | 3 |
| WS5 | Verify Boards linking on new repos | 0.5 |
| WS4 | Mannequin reclamation | 1 |
| WS10 | Hypercare (D+1 → D+3) | 2.5 |
| WS9 | Archive ADO repos for wave (D+7) | 0.5 |

**Per-wave total: ~11 p-days × 4 waves = 44 p-days**  
(With 2 waves in flight concurrently in weeks 7–9, calendar duration is 3 weeks.)

### Stage 4 — Stabilisation & Close (Week 10)

| WS | Activity | Owner | Effort (p-days) |
|----|---------|-------|-----------------|
| WS4 | Final mannequin reclamation sweep | Platform | 1 |
| WS5 | Boards linking audit across all 100 repos | DevEx | 1 |
| WS6 | Pipeline pass-rate audit | DevEx | 1 |
| WS7 | Security baseline audit (rulesets, scans) | InfoSec | 1 |
| WS9 | All ADO repos archived & permissions revoked | ADO Admin | 1 |
| WS1 | Phase 1 closure report | PM | 2 |
| WS1 | Phase 2 mandate decision pack | PM + Tech Lead | 2 |
| WS8 | Lessons learned session + publish | Change Mgr | 1 |

---

## 7. L3 Plan — Detailed Task List

Each task: ID · Title · Owner · Effort (p-days) · Predecessors.

### Stage 0 — Mobilise & Discovery

| ID | Task | Owner | Effort | Pred |
|----|------|-------|--------|------|
| 0.1 | Sponsor sign-off & charter | PM | 1 | — |
| 0.2 | RACI agreed | PM | 0.5 | 0.1 |
| 0.3 | Steering committee chartered, first meeting held | PM | 0.5 | 0.1 |
| 0.4 | RAID log v1 published | PM | 1 | 0.1 |
| 0.5 | Comms plan signed off | Change Mgr | 2 | 0.1 |
| 0.6 | Stakeholder & contact matrix (per repo) | Change Mgr | 1 | 0.1 |
| 0.7 | Identity inventory: pull ADO users from all 100 repos | IAM | 1 | 0.1 |
| 0.8 | Identity mapping CSV (ADO ↔ Entra ↔ planned EMU) | IAM | 2 | 0.7 |
| 0.9 | Repo inventory: `gh ado2gh inventory-report` for each ADO org | Platform | 1 | 0.1 |
| 0.10 | Repo size + LFS audit | Platform | 1 | 0.9 |
| 0.11 | Open PRs + open branches snapshot | Platform | 1 | 0.9 |
| 0.12 | Pipeline inventory per repo (YAML vs Classic) | DevEx | 2 | 0.9 |
| 0.13 | ADO branch policy inventory per repo | Platform | 2 | 0.9 |
| 0.14 | ADO service connections & integrations inventory | DevEx | 1 | 0.9 |
| 0.15 | Complexity scoring per repo | Tech Lead | 1 | 0.10–0.14 |
| 0.16 | Wave assignment (Pilot + W1–W4) | Tech Lead | 1 | 0.15 |
| 0.17 | Baseline ruleset JSON v1 | InfoSec + Platform | 2 | 0.13 |
| 0.18 | CODEOWNERS template | Platform | 0.5 | — |
| 0.19 | M1 gate: steering sign-off on wave plan & risks | PM + Sponsor | 0.5 | 0.16, 0.17 |

### Stage 1 — Identity & Foundation

| ID | Task | Owner | Effort | Pred |
|----|------|-------|--------|------|
| 1.1 | EMU enterprise shell created | IAM | 1 | 0.19 |
| 1.2 | Break-glass admin accounts configured | IAM | 1 | 1.1 |
| 1.3 | SAML SSO configured with MoJ Entra ID | IAM | 2 | 1.1 |
| 1.4 | SCIM endpoint configured | IAM | 1 | 1.3 |
| 1.5 | SCIM mapping (Entra attributes → GHE) | IAM | 1 | 1.4 |
| 1.6 | SCIM dry-run with 10 test users | IAM | 1 | 1.5 |
| 1.7 | SCIM full provisioning sweep | IAM | 1 | 1.6 |
| 1.8 | UAT: SSO login + access for 10 users | Tech Lead | 1 | 1.7 |
| 1.9 | Target GHE orgs pre-created (1:1 with ADO orgs) | Platform | 1 | 1.1 |
| 1.10 | Migration workstation provisioned (gh, gh-gei, gh-ado2gh) | Platform | 0.5 | — |
| 1.11 | Key Vault for migration secrets | Platform | 1 | — |
| 1.12 | ADO PAT + GH PAT issued and vaulted | Platform + IAM | 0.5 | 1.11 |
| 1.13 | Parameterised GEI migration script template | Platform | 2 | 1.10 |
| 1.14 | Ruleset application script (apply JSON to any repo) | Platform | 1 | 0.17, 1.9 |
| 1.15 | Migration tracking dashboard (Power BI / Grafana) | Platform | 2 | — |
| 1.16 | Sandbox GHE org for dry-runs | Platform | 0.5 | 1.9 |
| 1.17 | End-to-end factory smoke test (1 throwaway repo) | Migration Pod | 1 | 1.13, 1.14 |
| 1.18 | M2 gate: identity + factory ready | Sponsor + IAM + Tech Lead | 0.5 | 1.8, 1.17 |

### Stage 2 — Pilot Wave (5 repos)

| ID | Task | Owner | Effort | Pred |
|----|------|-------|--------|------|
| 2.1 | Pilot scope confirmed (5 repos, owners on board) | PM | 0.5 | 1.18 |
| 2.2 | T-10 / T-3 / T-1 comms to pilot users | Change Mgr | 1 | 2.1 |
| 2.3 | Dry-run pilot migration into sandbox | Migration Pod | 1 | 1.17, 2.1 |
| 2.4 | Validate dry-run (commits, branches, PRs, attachments) | Migration Pod | 0.5 | 2.3 |
| 2.5 | Pilot Go/No-Go meeting | Steering | 0.5 | 2.4 |
| 2.6 | Freeze pilot ADO repos (read-only) | ADO Admin | 0.5 | 2.5 |
| 2.7 | Execute pilot migration (5 repos) | Migration Pod | 1 | 2.6 |
| 2.8 | Apply rulesets to pilot repos | InfoSec | 0.5 | 2.7 |
| 2.9 | Apply CODEOWNERS to pilot repos | Platform | 0.5 | 2.7 |
| 2.10 | Install Azure Boards GitHub App on GHE pilot org | Platform + ADO Admin | 0.5 | 1.9 |
| 2.11 | Connect Boards App to ADO org + projects | Platform + ADO Admin | 0.5 | 2.10 |
| 2.12 | Test AB#123 linking on commit | DevEx | 0.5 | 2.11 |
| 2.13 | Test AB#123 linking on PR + auto-state-transition on merge | DevEx + Apps SME | 1 | 2.12 |
| 2.14 | Install Azure Pipelines GitHub App on GHE org | Platform | 0.5 | 1.9 |
| 2.15 | Re-point pilot pipelines (5–10 pipelines, YAML repos) | DevEx | 2 | 2.7, 2.14 |
| 2.16 | Validate build + release end-to-end | DevEx + Repo Owners | 1 | 2.15 |
| 2.17 | Mannequin reclamation for pilot | Platform | 1 | 2.7 |
| 2.18 | Repo owner smoke tests & sign-off | Repo Owners | 0.5 | 2.7, 2.8, 2.9 |
| 2.19 | Hypercare D+1 → D+3 (triage, fixes) | Wave Lead + Pods | 2 | 2.7 |
| 2.20 | Archive pilot ADO repos (D+7) | ADO Admin | 0.5 | 2.19 |
| 2.21 | Pilot retrospective + runsheet update | PM | 1 | 2.19 |
| 2.22 | M3 gate: pilot accepted, scale authorised | Steering | 0.5 | 2.21 |

### Stage 3 — Production Waves 1–4 (~25 repos each)

Template repeated 4× (W1, W2, W3, W4). Effort below is **per wave**.

| ID (per wave) | Task | Owner | Effort | Pred |
|---------------|------|-------|--------|------|
| Wn.1 | Wave manifest confirmed (repos, owners, pipelines) | Wave Lead | 0.5 | M3 / prev wave hypercare exit |
| Wn.2 | T-10 / T-3 / T-1 comms | Change Mgr | 1 | Wn.1 |
| Wn.3 | Dry-run wave migration into sandbox | Migration Pod | 1 | Wn.1 |
| Wn.4 | Dry-run validation | Migration Pod | 0.5 | Wn.3 |
| Wn.5 | Go/No-Go meeting | Steering | 0.5 | Wn.4 |
| Wn.6 | Freeze wave ADO repos | ADO Admin | 0.5 | Wn.5 |
| Wn.7 | Execute migration (25 repos parallel) | Migration Pod | 1 | Wn.6 |
| Wn.8 | Apply rulesets + CODEOWNERS | InfoSec + Platform | 0.5 | Wn.7 |
| Wn.9 | Verify Boards integration on new repos | DevEx | 0.5 | Wn.7 |
| Wn.10 | Re-point pipelines for wave (~25–50 pipelines) | DevEx | 3 | Wn.7 |
| Wn.11 | Validate builds for wave | DevEx + Repo Owners | 1 | Wn.10 |
| Wn.12 | Mannequin reclamation | Platform | 1 | Wn.7 |
| Wn.13 | Repo owner smoke tests & sign-off | Repo Owners | 1 | Wn.7, Wn.8 |
| Wn.14 | Hypercare D+1 → D+3 | Wave Lead + Pods | 2 | Wn.7 |
| Wn.15 | Archive wave ADO repos (D+7) | ADO Admin | 0.5 | Wn.14 |
| Wn.16 | Wave closure report | Wave Lead | 0.5 | Wn.14 |

**Per-wave effort:** ~14 p-days. 4 waves = **56 p-days**, executed in ~3 calendar weeks with 2 waves overlapping at any time.

### Stage 4 — Stabilisation & Close

| ID | Task | Owner | Effort | Pred |
|----|------|-------|--------|------|
| 4.1 | Final mannequin reclamation sweep across all waves | Platform | 1 | All Wn.12 |
| 4.2 | Boards linking audit (sample of ≥ 20 repos) | DevEx | 1 | All Wn.9 |
| 4.3 | Pipeline pass-rate audit | DevEx | 1 | All Wn.11 |
| 4.4 | Security baseline audit | InfoSec | 1 | All Wn.8 |
| 4.5 | All ADO repos confirmed archived; write perms revoked | ADO Admin | 1 | All Wn.15 |
| 4.6 | CMDB / asset inventory updated to new GHE URLs | IT Ops | 1 | 4.5 |
| 4.7 | Phase 1 closure report | PM | 2 | 4.1–4.6 |
| 4.8 | Lessons learned session & publish | Change Mgr | 1 | 4.7 |
| 4.9 | Phase 2 mandate pack (Actions migration) | PM + Tech Lead | 2 | 4.7 |
| 4.10 | M5 gate: Phase 1 closed | Sponsor + Steering | 0.5 | 4.7, 4.9 |

---

## 8. Critical Path

```
Sponsor sign-off
    └── Discovery & inventory
          └── Identity foundation (EMU + SAML + SCIM)
                └── Migration factory smoke test
                      └── Pilot wave (5 repos)
                            └── Pilot retrospective (M3 gate)
                                  └── Waves 1–4 (overlap, 2 in flight)
                                        └── Phase 1 close (M5)
```

The **identity foundation** is the longest-pole dependency. Any delay in MoJ Entra ID admin availability for SAML/SCIM will slip the whole program 1:1. Mitigate by booking IAM resource time in Week 1 and front-loading the SCIM dry-run.

---

## 9. Key Risks (Phase 1)

| # | Risk | Likelihood | Impact | Mitigation |
|---|------|-----------|--------|-----------|
| R1 | Entra SAML/SCIM configuration delayed (MoJ admin availability) | Med | High | Book MoJ IAM resource in Week 1; have backup admin |
| R2 | Pipeline re-pointing harder than expected (Classic pipelines, custom tasks) | Med | High | Inventory Classic % early; budget +20% effort for re-author |
| R3 | Branch policies don't perfectly map to rulesets | Low | Med | Baseline ruleset + per-repo exceptions list; document gaps |
| R4 | Mannequin reclamation gaps (ex-staff, contractors) | High | Low | Define unreclaimed-mannequin policy; document and move on |
| R5 | LFS / oversize repos exceed GHE limits | Low | High | Audit in Stage 0; remediate before wave assignment |
| R6 | Hardcoded ADO URLs in IaC / pipelines / docs | Med | Med | Inventory in Stage 0; provide redirect map; comms |
| R7 | Boards App rate limits across 100 repos | Low | Med | Stagger app install across waves; monitor |
| R8 | Concurrent waves overload hypercare team | Med | Med | Hard cap 2 waves concurrent; no new wave during D-0→D+3 |
| R9 | Repo owners not available for smoke tests | Med | Med | Confirm owner availability at T-10; escalation path |
| R10 | Pipeline secrets recreation gaps | Med | High | Secret inventory per pipeline; checklist for re-create |

---

## 10. Cost Indicator (Effort-Only)

At a blended £700/p-day:

| Component | p-days | Indicative Cost (£) |
|-----------|--------|---------------------|
| Phase 1 delivery | 150 | 105,000 |
| Contingency (already in 150) | included | — |

Plus licence / platform costs (GHE Enterprise seats, GHAS if in scope, Azure runner VMSS if used for Phase 2) — to be priced separately by procurement.

---

## 11. Decisions Required at Mobilise

| # | Decision | Recommendation | Owner |
|---|----------|----------------|-------|
| D1 | Pilot wave repos (5) — which? | Low-risk, willing teams, mix of YAML & Classic | Steering |
| D2 | GHAS in scope for Phase 1? | **Yes** for code/secret scanning + Dependabot baseline | InfoSec + Sponsor |
| D3 | Disable GitHub Issues per repo? | **Yes** (Boards stays in ADO; avoid drift) | Steering |
| D4 | Mannequin policy for ex-staff | Leave unreclaimed after 30 days, attribute to bot account | InfoSec + IAM |
| D5 | Auto-state-transition rules per work item type | Use ADO defaults; document per project | Apps SMEs |
| D6 | ADO retention window post-archive | 90 days read-only, then delete | Sponsor + InfoSec |
| D7 | Concurrent wave cap | 2 waves max in flight | Steering |

---

## 12. Phase 2 Preview (Out of Scope for this estimate)

Phase 2 = migrate CI/CD from Azure Pipelines & Releases to **GitHub Actions**.

| Theme | Indicative Effort | Notes |
|-------|-------------------|-------|
| Actions Importer setup & audit | 5 p-days | `gh actions-importer` |
| Self-hosted runners (VMSS) | 8 p-days | Per BU or shared |
| OIDC federation to Azure | 3 p-days | Replace service connections |
| Pipeline conversion (per pipeline avg) | 0.5–2 p-days | Depends on Classic vs YAML |
| Release pipeline conversion (per release) | 1–3 p-days | Environments, approvals, gates |
| Hypercare + cutover per wave | 3 p-days | Mirror Phase 1 model |

**Indicative Phase 2 duration: 12–16 weeks; effort: ~200–250 p-days** depending on pipeline counts and complexity.

A separate detailed estimate for Phase 2 should be produced **at Phase 1 close (M5)** when actual pipeline counts and complexity are known.
