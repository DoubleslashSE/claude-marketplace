# Infrastructure Troubleshooting Plugin

A Claude Code plugin for diagnosing and resolving issues across GitHub Actions, Railway, Supabase, and Postgres. Focuses on log analysis, error pattern recognition, and proactive health monitoring.

## Commands

| Command | Description | Use Case |
|---------|-------------|----------|
| `/infra:diagnose` | Full diagnostic workflow | "My app is broken, help!" |
| `/infra:logs <platform>` | Quick log retrieval | "Show me Supabase postgres logs" |
| `/infra:health` | Health check all platforms | "Is everything okay?" |
| `/infra:errors` | Find and analyze errors | "What errors happened today?" |
| `/infra:trace` | Trace issue across stack | "Follow this error through the system" |

## Agents

| Agent | Purpose |
|-------|---------|
| `log-analyzer` | Parse and analyze logs from all platforms |
| `error-diagnostician` | Root cause analysis and remediation |
| `platform-specialist` | Platform-specific expertise and configuration |
| `health-monitor` | Proactive health assessment and monitoring |

## Supported Platforms

### Supabase
- API logs, Postgres logs, Auth logs, Storage logs, Realtime logs, Edge Function logs
- Security and performance advisories
- Direct Postgres health queries

### GitHub Actions
- Workflow run history
- Build logs and failed step analysis
- CI/CD success rate monitoring

### Railway
- Service logs
- Deployment status
- Application health

### Postgres
- Connection monitoring
- Long-running query detection
- Table size analysis
- Lock detection

## Quick Start

```bash
# Check overall infrastructure health
/infra:health

# Get logs from a specific platform
/infra:logs supabase postgres
/infra:logs github
/infra:logs railway

# Diagnose an issue
/infra:diagnose "API returning 500 errors"

# Find and analyze recent errors
/infra:errors

# Trace an issue through the stack
/infra:trace "correlation-id-123"
```

## Prerequisites

### Required CLI Tools
- `gh` - GitHub CLI (for GitHub Actions)
- `railway` - Railway CLI (for Railway)

### Supabase Access
- Supabase MCP server must be configured with project access

## Key Workflows

### Diagnose Workflow
```
Issue reported -> Collect logs (all platforms) -> Error analysis ->
Root cause analysis -> Health check -> Remediation plan
```

### Health Check Workflow
```
Check GitHub Actions (success rate) -> Check Railway (status) ->
Check Supabase (advisories) -> Check Postgres (connections, queries) ->
Generate health report
```

## Skills Reference

- **log-analysis**: Log parsing techniques and platform-specific patterns
- **error-patterns**: Error recognition and common solution catalog
- **platform-knowledge**: Deep knowledge of each platform's troubleshooting
- **health-checks**: Health monitoring procedures and checklists

## Installation

Add to your Claude Code plugins directory or install via the marketplace.

## License

MIT
