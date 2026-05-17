# 10. Success Metrics & KPIs

## Program-Level KPIs

| KPI | Target |
|-----|--------|
| Repos migrated with history integrity verified | 100% of in-scope |
| Pipelines converted to Actions and green within hypercare | ≥ 95% |
| Mannequins unreclaimed at wave close | < 2% |
| P1 data-loss incidents | 0 |
| Developer NPS post-migration vs baseline | No regression |
| ADO licenses released within 30 days of program close | 100% |
| On-time wave completion (closure within +1 business day of plan) | ≥ 90% |
| Security baseline (CodeQL + secret scanning + Dependabot) enabled on migrated repos | 100% |

## Per-Wave KPIs

| KPI | Target |
|-----|--------|
| Repos migrated successfully on first run | ≥ 95% |
| Repo owner smoke-test sign-off | 100% before hypercare exit |
| Pipeline first-run pass rate | ≥ 90% |
| P1/P2 defects open at hypercare exit | 0 |
| Average time from D-0 freeze to "open for business" | ≤ 8 hours |
| Mannequins reclaimed within wave | ≥ 98% |

## Reporting

A migration metrics dashboard is published daily during active waves, showing:

- Repos migrated (cumulative and per-wave).
- Pipelines migrated and pass rate.
- Mannequins reclaimed vs total.
- Defects open by severity.
- Wave status (planned, in flight, hypercare, closed).
- License consumption (ADO trending down, GHE trending up).
