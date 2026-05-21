# ADO → GHE Migration Program

Migration program for consolidating Azure DevOps repositories into **GitHub Enterprise Cloud (EMU)** linked to **MoJ Entra ID**.

> **Customer:** Saudi Arabia Ministry of Justice  
> **Phase 1 scope (active):** 100 repos — code, PRs, commits → GHE. Boards & release pipelines stay in Azure DevOps. Linked via the Azure Boards GitHub App (`AB#123` references).  
> **Phase 2 (deferred):** Migrate CI/CD release pipelines to GitHub Actions.

---

## 📦 Phase 1 deliverables

| Artefact | Description |
|----------|-------------|
| [phase1/PHASE1-EFFORT-PLAN.md](phase1/PHASE1-EFFORT-PLAN.md) | Detailed effort estimation: 10 weeks · 150 person-days · 8-person team · L1/L2/L3 plan · pre-requisites · decisions |
| [phase1/ADO-to-GHE-Phase1-Plan.pptx](phase1/ADO-to-GHE-Phase1-Plan.pptx) | 18-slide branded steering deck with speaker notes (Gantt, RACI, risks, KPIs) |
| [phase1/ADO-to-GHE-Phase1-L3-Tasks.csv](phase1/ADO-to-GHE-Phase1-L3-Tasks.csv) | L3 task list — 133 tasks, owners, effort, predecessors, week, workstream |
| [phase1/scripts/build_deck.py](phase1/scripts/build_deck.py) | Regenerates the deck (python-pptx) |
| [phase1/scripts/build_csv.py](phase1/scripts/build_csv.py) | Regenerates the L3 task CSV |

**Phase 1 headline numbers**

| Metric | Value |
|--------|-------|
| Duration | 10 calendar weeks (2 mobilise + 8 delivery) |
| Effort | 150 person-days |
| Team | 8 people (5.3 peak FTE) |
| Repos in scope | 100 |
| Waves | 5 (Pilot + Waves 1–4) |
| Capacity utilisation | ~70% (150 effort / 217 capacity) |

---

## 📚 Program plan (full)

| Doc | Description |
|-----|-------------|
| [docs/01-executive-summary.md](docs/01-executive-summary.md) | Program scope, strategy, sponsor view |
| [docs/02-guiding-principles.md](docs/02-guiding-principles.md) | Non-negotiables that govern execution |
| [docs/03-target-architecture.md](docs/03-target-architecture.md) | Target identity, org topology, runners |
| [docs/04-workstreams.md](docs/04-workstreams.md) | Ten workstreams, leads, outputs |
| [docs/05-phases-timeline.md](docs/05-phases-timeline.md) | Phases 0–6 |
| [docs/06-wave-planning.md](docs/06-wave-planning.md) | Complexity scoring & wave model |
| [docs/runsheet/01-pre-wave.md](docs/runsheet/01-pre-wave.md) | D-10 → D-1 activities |
| [docs/runsheet/02-cutover-day.md](docs/runsheet/02-cutover-day.md) | D-0 cutover blocks A–G |
| [docs/runsheet/03-hypercare-close.md](docs/runsheet/03-hypercare-close.md) | D+1 → D+90 |
| [docs/07-cross-cutting.md](docs/07-cross-cutting.md) | Program-level recurring activities |
| [docs/08-tooling.md](docs/08-tooling.md) | Tools inventory |
| [docs/09-risks.md](docs/09-risks.md) | Risk register & mitigations |
| [docs/10-kpis.md](docs/10-kpis.md) | Success metrics |
| [docs/11-open-decisions.md](docs/11-open-decisions.md) | Decisions awaiting steering |
| [PROJECT-PLAN.md](PROJECT-PLAN.md) | Consolidated single-file plan |

---

## 🎯 Quick strategy

- **Identity first** — EMU + Entra SSO/SCIM before any repo moves.
- **Factory model** — repeatable, scripted, idempotent migrations.
- **Wave-based** — 5–8 ADO orgs per wave; parallelize within waves.
- **Zero data loss** — full history, PRs, attachments, LFS preserved.
- **Read-only freeze, then cutover** — no dual-write windows.
- **Azure Boards GitHub App** keeps work-item linkage (`AB#123`) intact during Phase 1.
