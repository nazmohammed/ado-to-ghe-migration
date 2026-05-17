# 06. Wave Planning Model

## Complexity Score (per ADO org)

Score each ADO org **1–5** on six factors:

| Factor | 1 (Low) | 5 (High) |
|--------|---------|----------|
| Repo count & size (incl. LFS) | < 10 repos, < 1 GB total | > 100 repos or > 50 GB |
| Pipeline count & complexity | < 5 YAML pipelines | > 30 pipelines or classic-heavy |
| Work item volume | < 500 active | > 10,000 with custom processes |
| Integrations / service connections | 0–2 | > 10, with custom extensions |
| Active user count | < 20 | > 200 |
| Regulatory sensitivity | None | Regulated (PCI, HIPAA, SOX) |

**Total score (sum of six factors, 6–30)** → wave bucket:

| Score | Wave Bucket |
|-------|-------------|
| 6–10 | Wave 0 (Pilot) or Waves 1–2 |
| 11–15 | Waves 3–5 |
| 16–20 | Waves 6–8 |
| 21–25 | Waves 9–11 |
| 26–30 | Wave 12 (highest-risk, last) |

## Wave Sizing

- **8 ADO orgs per wave** (target).
- **~5 business days end-to-end** per wave (D-10 prep → D+7 close).
- **Up to 3 waves concurrent** after Pilot, staggered by 2 days.

## Wave Assignment Heuristics

1. **Low-risk first, willing teams first.** Pilot recruits volunteers.
2. **Regulated orgs last.** Maximum runbook maturity before touching them.
3. **Group by BU within a wave** where possible to amplify comms.
4. **Avoid mixing TFVC and Git-native** orgs in the same wave.
5. **Reserve hypercare capacity** — no new wave starts during another wave's D-0 → D+3.

## Wave Manifest (template)

Each wave produces a manifest containing:

- Wave number and target dates (relative).
- List of ADO orgs in scope.
- Target GHE org(s) per ADO org.
- Repo count, pipeline count, user count totals.
- Named org admin, repo owners, SMEs per ADO org.
- Assigned migration pod and wave lead.
- Known risks and special handling notes.
