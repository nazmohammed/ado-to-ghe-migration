# 02. Guiding Principles

Non-negotiable principles that govern every wave and decision.

1. **Identity first** — EMU + Entra SSO/SCIM are live before any repo moves.
2. **Factory model** — repeatable, scripted, idempotent migrations; no bespoke per-team work.
3. **Wave-based** — 5–8 ADO orgs per wave; parallelize within waves, not across them at first.
4. **Zero data loss** — full history, PRs, attachments, and LFS preserved; verified before sign-off.
5. **Read-only freeze, then cutover** — no dual-write windows; ADO becomes read-only before GHE opens.
6. **Comms first** — owners and developers know exactly what changes and when, with named contacts.
7. **Validation by owners** — repo owners and pipeline owners sign off; central team facilitates, doesn't certify on their behalf.
8. **Security parity, not regression** — baseline scanning, secret detection, and protected branches active from day one in GHE.
9. **Reversible until cutover** — until the freeze, any migration can be retried into a sandbox without user impact.
10. **Decommission is part of done** — a wave is not closed until ADO is archived and inventory is updated.
