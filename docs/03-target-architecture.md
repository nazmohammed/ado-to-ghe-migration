# 03. Target Architecture

## Identity & Tenancy

```
Microsoft Entra ID (tenant)
  ├── SCIM → GitHub EMU Enterprise
  │            ├── Org: <business-unit-1>
  │            ├── Org: <business-unit-2>
  │            └── ... (consolidated from 95 ADO orgs)
  ├── SAML SSO
  └── App registrations for OIDC → Azure deployments
```

## Compute / Runners

```
GitHub Actions
  └── self-hosted runners (Azure VMSS) + GitHub-hosted runners
        └── OIDC federation → Azure subscriptions (replaces service connections)
```

## Org Consolidation Decision

Map **95 ADO orgs → ~10–20 GHE orgs** by business unit / line-of-business. The exact target is decided in Phase 1 based on:

- Business unit ownership boundaries.
- Compliance/regulatory segregation requirements.
- Repo and user volume per BU.
- Billing / chargeback structure.

A consolidation matrix is produced in Phase 1 and approved by steering before foundation build.

## Key Design Choices

| Decision | Choice | Rationale |
|----------|--------|-----------|
| GHE flavour | **GHE Cloud with EMU** | Centralized identity, lifecycle managed via Entra |
| Auth | **SAML SSO + SCIM** | Single source of truth; no personal accounts |
| Runner topology | **Per-BU VMSS pools + GitHub-hosted for low-risk** | Isolation where needed, cost efficiency elsewhere |
| Cloud deploy auth | **OIDC federation** | No long-lived secrets in Actions |
| Secret store | **Azure Key Vault + Actions secrets** | Vault for cross-pipeline, Actions for repo-local |
| Security tooling | **GitHub Advanced Security** | Code scanning, secret scanning, Dependabot baseline |
