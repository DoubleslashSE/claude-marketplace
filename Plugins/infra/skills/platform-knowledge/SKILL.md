---
name: platform-knowledge
description: Deep knowledge of GitHub Actions, Railway, Supabase, and Postgres platforms. Use when troubleshooting, configuring, or optimizing any of these platforms.
allowed-tools: Bash, Grep, Read, Glob, mcp__plugin_supabase_supabase__list_projects, mcp__plugin_supabase_supabase__get_project, mcp__plugin_supabase_supabase__list_tables
---

# Platform Knowledge Skill

## Overview

This skill provides comprehensive knowledge of the infrastructure platforms: GitHub Actions, Railway, Supabase, and Postgres. It covers architecture, configuration, troubleshooting, and best practices for each platform.

## Platform Overview

### GitHub Actions
- **Purpose**: CI/CD automation
- **Key Features**: Workflow automation, testing, deployment
- **Config Files**: `.github/workflows/*.yml`
- **CLI**: `gh`

### Railway
- **Purpose**: Application hosting and deployment
- **Key Features**: Auto-deployments, instant rollbacks, environment management
- **Config Files**: `railway.toml`, `nixpacks.toml`, `Procfile`
- **CLI**: `railway`

### Supabase
- **Purpose**: Backend-as-a-Service (Postgres, Auth, Storage, Realtime)
- **Key Features**: Managed Postgres, authentication, file storage, realtime subscriptions
- **Config Files**: `supabase/config.toml`, migrations
- **Access**: MCP tools, Dashboard, CLI

### Postgres
- **Purpose**: Relational database
- **Key Features**: ACID compliance, extensions, full-text search, JSON support
- **Config**: Connection strings, postgresql.conf
- **Access**: SQL queries via MCP or psql

## Platform Interaction Map

```
┌──────────────┐     ┌──────────────┐
│   GitHub     │     │   Railway    │
│   Actions    │────▶│   (App)      │
│   (CI/CD)    │     │              │
└──────────────┘     └──────┬───────┘
                            │
                            ▼
                     ┌──────────────┐
                     │   Supabase   │
                     │   (Backend)  │
                     │              │
                     │ ┌──────────┐ │
                     │ │ Postgres │ │
                     │ └──────────┘ │
                     └──────────────┘
```

## Quick Reference

### Tool Access by Platform

| Platform | MCP Tools | CLI | Logs |
|----------|-----------|-----|------|
| GitHub Actions | No | `gh` | `gh run view --log` |
| Railway | No | `railway` | `railway logs` |
| Supabase | Yes | `supabase` | MCP `get_logs` |
| Postgres | Yes (via Supabase) | `psql` | MCP `get_logs` |

### Common Operations

| Task | GitHub | Railway | Supabase |
|------|--------|---------|----------|
| Deploy | Push/workflow | Git push / `railway up` | Dashboard / CLI |
| Logs | `gh run view --log` | `railway logs` | MCP `get_logs` |
| Status | `gh run list` | `railway status` | MCP `get_project` |
| Rollback | Re-run workflow | Dashboard | Run migration down |
| Secrets | Repository settings | Environment variables | Project settings |

## Troubleshooting Decision Tree

```
Issue Reported
     │
     ▼
┌─────────────────────────────────────┐
│ Where does the issue manifest?      │
└─────────────────────────────────────┘
     │
     ├─► Build/Deploy fails ──► GitHub Actions / Railway
     │
     ├─► API errors ──► Supabase API / Edge Functions
     │
     ├─► Auth issues ──► Supabase Auth
     │
     ├─► Database errors ──► Postgres
     │
     ├─► App crashes ──► Railway / Edge Functions
     │
     └─► Performance ──► All platforms (profile each)
```

## Platform-Specific Guides

Detailed guides for each platform:

- [GitHub Actions](github-actions.md) - CI/CD workflows, secrets, debugging
- [Railway](railway.md) - Deployment, configuration, troubleshooting
- [Supabase](supabase.md) - Auth, API, Realtime, Storage
- [Postgres](postgres.md) - Queries, performance, administration

## Cross-Platform Issues

### Deployment Chain Failure

**Symptom**: Deploy succeeds but app broken

**Check all stages**:
1. GitHub Actions - Build/test passed?
2. Railway - Deploy successful?
3. Supabase - Migrations applied?
4. Environment - Variables set?

### Environment Variable Issues

**Common causes**:
- Set in wrong environment
- Typo in variable name
- Not propagated after change

**Verify across platforms**:
```bash
# GitHub Actions - Check secrets
# (Can't view, only verify existence)

# Railway
railway variables

# Supabase - Check project settings
# Dashboard or MCP
```

### Connection Issues Between Services

**Railway → Supabase**:
- Check Supabase URL format
- Verify API key (anon vs service_role)
- Check connection pooling settings
- Verify IP restrictions

**GitHub Actions → Services**:
- Check secrets are accessible
- Verify network egress allowed
- Check for rate limiting

## Performance Troubleshooting Matrix

| Symptom | GitHub Actions | Railway | Supabase | Postgres |
|---------|---------------|---------|----------|----------|
| Slow | Cache missing, big deps | Cold start, resources | Edge function | Query optimization |
| Timeout | Step timeout | Health check | API timeout | Statement timeout |
| Memory | OOM on build | Container limit | Function limit | work_mem |
| CPU | Concurrent jobs | Container limit | N/A | Query complexity |

## Configuration Files Reference

### GitHub Actions
```yaml
# .github/workflows/deploy.yml
name: Deploy
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      # ... more steps
```

### Railway
```toml
# railway.toml
[build]
builder = "nixpacks"
buildCommand = "npm run build"

[deploy]
startCommand = "npm start"
healthcheckPath = "/health"
```

### Supabase
```toml
# supabase/config.toml
[api]
port = 54321
schemas = ["public", "graphql_public"]

[db]
port = 54322
```

### Postgres
```sql
-- Key settings
SHOW max_connections;
SHOW statement_timeout;
SHOW work_mem;
```
