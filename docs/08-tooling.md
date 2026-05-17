# 08. Tooling Inventory

| Tool | Purpose |
|------|---------|
| `gh-gei` | Repo migration (issues, PRs, attachments, history) |
| `gh-ado2gh` | ADO-specific helpers: inventory, script gen, mannequin reclamation, team migration, pipeline rewires |
| `gh-actions-importer` | Pipeline → Actions workflow conversion (audit, dry-run, migrate, forecast) |
| Azure Key Vault | PAT and secret storage; fetched at runtime by migration scripts |
| Entra ID + SCIM | EMU identity provisioning and lifecycle |
| GitHub Advanced Security | Code scanning, secret scanning, Dependabot |
| Azure Monitor / Log Analytics | Migration runner logs, audit log retention |
| Custom WI migration script | ADO REST → GitHub Issues/Projects REST (mapping table driven) |
| Power BI / Grafana dashboard | Program metrics (repos done, velocity, defects, mannequins) |
| ServiceNow / Jira | Defect & change tracking |
| Azure VMSS | Self-hosted Actions runners with autoscale |
| GitHub CLI (`gh`) | Day-to-day operations & scripting |

## Install Commands (operator quick-ref)

```bash
gh extension install github/gh-gei
gh extension install github/gh-ado2gh
gh extension install github/gh-actions-importer
```

## Required Permissions

| Identity | Scope | Used For |
|----------|-------|----------|
| ADO PAT | Read code, work items, build, packages | Source-side reads |
| GH PAT (admin:org, repo, workflow) | Target GHE enterprise | Target writes & ruleset application |
| Azure Service Principal | Subscription Contributor (on runner sub) | VMSS lifecycle |
| Entra App Registration | SCIM provisioning | EMU user lifecycle |

All PATs and credentials are stored in Azure Key Vault and rotated on a defined cadence.
