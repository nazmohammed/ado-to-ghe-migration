# 01. Executive Summary

Migrate **95 Azure DevOps (ADO) organizations** (one per VSE/Azure subscription) into a consolidated **GitHub Enterprise Cloud (EMU)** tenant linked to Microsoft Entra ID.

## Scope

Repositories, pipelines, work items, artifacts, wikis, service connections, identities, branch policies, and governance across all 95 ADO orgs.

## Strategy

A factory-model, wave-based migration using:

- **GitHub Enterprise Importer (GEI)** for repositories.
- **GitHub Actions Importer** for pipelines.
- **Entra ID-driven EMU provisioning** for identity.

Migration pods run parallel waves; a central platform team owns tooling, governance, and cutover orchestration.

## Outcomes

- One consolidated GHE Cloud (EMU) enterprise.
- All in-scope repos, history, PRs, and attachments preserved.
- Pipelines re-platformed to GitHub Actions with OIDC to Azure.
- ADO orgs archived (read-only) then decommissioned post-retention.
- Unified developer experience aligned to a single Entra-backed identity.
