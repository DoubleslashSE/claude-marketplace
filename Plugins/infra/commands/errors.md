---
description: Find and analyze errors across infrastructure platforms. Use to identify, categorize, and understand recent errors.
---

# Error Analysis

Find and analyze errors for: **$ARGUMENTS**

## Overview

This command searches for and analyzes errors across your infrastructure platforms, providing categorized error summaries and insights.

## Usage

```bash
/infra:errors [platform] [--since <time>]
```

### Examples

```bash
# Find errors across all platforms
/infra:errors

# Find errors on a specific platform
/infra:errors supabase
/infra:errors github
/infra:errors railway

# Find errors with time filter
/infra:errors --since 1h
/infra:errors supabase --since 24h
```

## Error Collection Process

### Phase 1: Gather Errors

Collect error logs from each platform:

**Supabase**
```
# API errors (5xx responses)
mcp__plugin_supabase_supabase__get_logs(project_id, "api")
# Filter for error status codes

# Postgres errors
mcp__plugin_supabase_supabase__get_logs(project_id, "postgres")
# Filter for ERROR, FATAL, PANIC levels

# Auth errors
mcp__plugin_supabase_supabase__get_logs(project_id, "auth")
# Filter for failed auth attempts, errors

# Edge function errors
mcp__plugin_supabase_supabase__get_logs(project_id, "edge-function")
# Filter for uncaught exceptions, errors
```

**GitHub Actions**
```bash
# Failed workflow runs
gh run list --status failure --limit 20

# Get failure details
gh run view <run-id> --log-failed
```

**Railway**
```bash
# Search logs for errors
railway logs 2>&1 | grep -i "error\|fatal\|exception\|crash\|panic"
```

### Phase 2: Categorize Errors

Group errors by:
1. **Platform**: Where the error occurred
2. **Type**: Error category (database, auth, API, build, etc.)
3. **Frequency**: How often it occurs
4. **Severity**: Critical, High, Medium, Low

### Phase 3: Analyze Patterns

For each error category:
- First occurrence
- Most recent occurrence
- Frequency trend (increasing/stable/decreasing)
- Potential root cause
- Recommended action

## Output Format

```markdown
## Error Analysis Report

**Time Range**: {START} to {END}
**Total Errors Found**: {COUNT}

## Summary by Platform

| Platform | Critical | High | Medium | Low | Total |
|----------|----------|------|--------|-----|-------|
| Supabase | {N}      | {N}  | {N}    | {N} | {N}   |
| GitHub   | {N}      | {N}  | {N}    | {N} | {N}   |
| Railway  | {N}      | {N}  | {N}    | {N} | {N}   |

## Critical Errors (Immediate Attention)

### {ERROR_TYPE_1}
- **Platform**: {PLATFORM}
- **Count**: {N} occurrences
- **First Seen**: {TIME}
- **Last Seen**: {TIME}
- **Example**:
  ```
  {ERROR_MESSAGE}
  ```
- **Likely Cause**: {ANALYSIS}
- **Recommended Action**: {ACTION}

## High Priority Errors

{Similar format to Critical}

## Medium/Low Priority Errors

| Error Type | Platform | Count | Last Seen | Action |
|------------|----------|-------|-----------|--------|
| {ERROR}    | {PLAT}   | {N}   | {TIME}    | {ACT}  |

## Error Trends

{Analysis of error patterns over time}

## Recommended Next Steps

1. {Most urgent action}
2. {Second priority}
3. {Third priority}

---
*Use `/infra:diagnose` for deeper analysis of specific errors*
```

## Error Severity Classification

### Critical
- Service completely unavailable
- Data loss or corruption
- Security breach indicators
- All requests failing

### High
- Significant functionality broken
- >10% error rate
- Authentication failures
- Database connection issues

### Medium
- Intermittent failures
- Performance degradation
- Non-critical feature broken
- Warning patterns increasing

### Low
- Isolated incidents
- Expected errors (404s, validation)
- Deprecation warnings
- Minor configuration issues

## Common Error Patterns

### Database Errors
- `connection refused` - DB unreachable
- `too many connections` - Pool exhaustion
- `deadlock detected` - Transaction conflicts
- `statement timeout` - Slow query killed

### API Errors
- `401 Unauthorized` - Auth token issues
- `403 Forbidden` - Permission denied
- `429 Too Many Requests` - Rate limited
- `500 Internal Server Error` - Unhandled exception
- `502 Bad Gateway` - Upstream failure
- `503 Service Unavailable` - Overloaded

### Build/Deploy Errors
- `npm ERR!` - Dependency issues
- `ENOMEM` - Out of memory
- `ETIMEDOUT` - Network timeout
- `exit code 1` - Build script failure

## Quick Actions

Based on findings, may recommend:
- `/infra:diagnose <error>` - Deep dive on specific error
- `/infra:health` - Check overall system health
- `/infra:trace <id>` - Trace error through system
