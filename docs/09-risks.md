# 09. Risks & Mitigations

| # | Risk | Impact | Likelihood | Mitigation |
|---|------|--------|------------|-----------|
| R1 | TFVC repos in scope | High | Medium | Convert to Git in ADO pre-migration; allocate extra wave time; do not mix with Git waves |
| R2 | Large LFS / binary repos exceed GHE limits | High | Medium | Audit early; split, prune, or migrate to Packages; pre-size LFS bandwidth |
| R3 | Pipeline secrets not portable | Medium | High | OIDC federation to Azure; secret remediation list per pipeline; document each replacement |
| R4 | Service connections / shared agents | Medium | High | Inventory upfront; replace with self-hosted runners + OIDC |
| R5 | Identity mapping gaps (orphan authors) | Medium | High | Mannequin reclamation cycle each wave; chase unmapped users with comms |
| R6 | Work item fidelity loss | Medium | High | Set expectations early; preserve original ADO export as archive; map states + custom fields |
| R7 | Custom ADO extensions / process templates | Medium | Medium | Catalogue upfront; find GH equivalent or accept gap with sign-off |
| R8 | User resistance / change fatigue | Medium | Medium | Strong comms, champions network, training, office hours |
| R9 | GEI rate limits at scale | Low | Medium | Stagger waves; multiple PATs; coordinate with GitHub support for quota uplift |
| R10 | Audit/regulatory continuity | High | Low | Retain ADO read-only 90d; export ADO and GHE audit logs to SIEM; map controls before regulated waves |
| R11 | Self-hosted runner capacity at peak | Medium | Medium | Autoscale VMSS; capacity rehearsal in Phase 2; reserve burst capacity in cutover blocks |
| R12 | Hypercare overload across concurrent waves | Medium | High | Hard cap on concurrent waves; no new wave starts during another's D-0 → D+3 |
| R13 | Cross-team dependency in shared repos | High | Medium | Identify shared repos in discovery; migrate together or coordinate explicit handoffs |
| R14 | License trueup gap (over- or under-provisioning) | Low | Medium | Monthly license review; deactivate EMU users on Entra leaver event |
| R15 | Tooling change mid-program (GEI / Actions Importer breaking changes) | Medium | Low | Pin versions; test version bumps in sandbox before adopting in production waves |

## Risk Review Cadence

- **Weekly:** RAID log walked at steering.
- **Per wave gate:** active risks for the wave reviewed at Go/No-Go.
- **On materialization:** any risk that materializes is converted to an issue with owner and ETA.
