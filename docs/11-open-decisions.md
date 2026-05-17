# 11. Open Decisions

Decisions awaiting steering committee approval before relevant phases begin.

| # | Decision | Recommendation | Required By |
|---|----------|----------------|-------------|
| D1 | GHE org consolidation target count and naming convention | ~10–20 GHE orgs aligned to BUs; naming `<bu>-<domain>` | End of Phase 1 |
| D2 | GHE flavour: EMU vs standard GHE Cloud | **EMU** — centralized identity for 95-org consolidation | Start of Phase 0 |
| D3 | Self-hosted runner topology | Per-BU VMSS pools + GitHub-hosted for low-risk repos | Start of Phase 2 |
| D4 | Work-item migration fidelity bar | Metadata + state + comments; attachments best-effort; ADO archive retained | End of Phase 1 |
| D5 | Retention window for archived ADO orgs | 90 days post-wave-close | End of Phase 1 |
| D6 | Wave size and concurrency | 8 orgs/wave, up to 3 waves concurrent after pilot | End of Phase 1 |
| D7 | Pipeline conversion approach for classic pipelines | Re-author as YAML where complex; importer for simple cases | End of Phase 1 |
| D8 | GitHub Advanced Security scope | All migrated repos; remediation owned by repo owner | Start of Phase 2 |
| D9 | Branch protection ruleset baseline | Require PR + 1 approval + status checks + linear history on default branch | End of Phase 1 |
| D10 | Cost model / chargeback for GHE seats | Aligned to BU consolidation; monthly trueup | Start of Phase 2 |

## Decision Log Format

When a decision is made, record:

- Decision number, title, date.
- Options considered.
- Selected option and rationale.
- Decision maker(s).
- Impact on plan or runsheet.
