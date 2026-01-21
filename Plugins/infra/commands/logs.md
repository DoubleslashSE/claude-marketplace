---
description: Quick log retrieval from infrastructure platforms. Use to fetch and display logs from GitHub Actions, Railway, Supabase, or Postgres.
---

# Log Retrieval

Retrieve and display logs for: **$ARGUMENTS**

## Overview

This command provides quick access to logs from your infrastructure platforms. Specify the platform and optionally a service type to get relevant logs.

## Usage

```bash
/infra:logs <platform> [service]
```

### Examples

```bash
# Supabase logs
/infra:logs supabase postgres
/infra:logs supabase api
/infra:logs supabase auth
/infra:logs supabase storage
/infra:logs supabase realtime
/infra:logs supabase edge-function

# GitHub Actions logs
/infra:logs github
/infra:logs github <workflow-name>
/infra:logs github <run-id>

# Railway logs
/infra:logs railway
/infra:logs railway <service-name>
```

## Platform-Specific Instructions

### Supabase

Use the Supabase MCP tools to retrieve logs:

1. First, list available projects if not specified:
   ```
   mcp__plugin_supabase_supabase__list_projects
   ```

2. Get logs for the specified service:
   ```
   mcp__plugin_supabase_supabase__get_logs(project_id, service)
   ```

**Service Types**:
- `api` - API gateway logs (requests, responses, errors)
- `postgres` - Database logs (queries, errors, connections)
- `auth` - Authentication logs (logins, signups, errors)
- `storage` - Storage service logs (uploads, downloads)
- `realtime` - Realtime/WebSocket logs
- `edge-function` - Edge function execution logs

### GitHub Actions

Use the `gh` CLI to retrieve workflow logs:

```bash
# List recent runs
gh run list --limit 10

# View logs for a specific run
gh run view <run-id> --log

# View only failed step logs
gh run view <run-id> --log-failed

# List runs for a specific workflow
gh workflow view <workflow-name> --recent 10
```

### Railway

Use the `railway` CLI to retrieve logs:

```bash
# View recent logs
railway logs

# Follow logs in real-time
railway logs --follow

# View logs for specific service
railway logs --service <service-name>
```

## Output Format

Present logs in a clear, readable format:

```markdown
## Logs: {PLATFORM} / {SERVICE}

**Time Range**: {START} to {END}
**Entries**: {COUNT}

### Recent Entries

{LOG_ENTRIES}

### Error Summary (if any)

| Error Type | Count | Last Occurrence |
|------------|-------|-----------------|
| {ERROR}    | {N}   | {TIME}          |

### Quick Analysis

{Brief analysis of log patterns, any notable issues}
```

## Error Handling

If logs cannot be retrieved:

1. **Platform not specified**: Ask which platform to fetch logs from
2. **Project not found**: List available projects/services
3. **CLI not installed**: Provide installation instructions
4. **Authentication required**: Guide through authentication steps
5. **No logs available**: Report empty result with time range checked

## Quick Tips

- For Supabase, logs are available for the last 24 hours
- For GitHub Actions, use `--log-failed` to focus on failure output
- For Railway, use `--follow` to stream live logs
- Use `/infra:errors` if you want to focus specifically on error logs
