# ADO → GHE Migration Program

Project plan and runsheet for migrating **95 Azure DevOps organizations** into a consolidated **GitHub Enterprise Cloud (EMU)** tenant.

## Contents

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

## Quick Strategy

- **Identity first** — EMU + Entra SSO/SCIM before any repo moves.
- **Factory model** — repeatable, scripted, idempotent migrations.
- **Wave-based** — 5–8 ADO orgs per wave; parallelize within waves.
- **Zero data loss** — full history, PRs, attachments, LFS preserved.
- **Read-only freeze, then cutover** — no dual-write windows.
