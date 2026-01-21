---
description: Trace issues across the infrastructure stack. Use to follow a request, error, or transaction through multiple systems.
---

# Issue Tracing

Trace: **$ARGUMENTS**

## Overview

This command traces an issue, request, or transaction across multiple infrastructure platforms to understand the complete flow and identify where problems occur.

## Usage

```bash
/infra:trace <identifier>
```

### Examples

```bash
# Trace by correlation/request ID
/infra:trace "req-abc123"

# Trace by user ID
/infra:trace "user:user-456"

# Trace by error message
/infra:trace "connection timeout"

# Trace by timestamp
/infra:trace "2024-01-15 14:30"

# Trace a specific transaction
/infra:trace "order:ord-789"
```

## Tracing Process

### Phase 1: Identify Trace Target

Parse the provided identifier to determine trace type:

| Pattern | Type | Search Strategy |
|---------|------|-----------------|
| `req-*`, `x-request-id:*` | Request ID | Search all logs for ID |
| `user:*`, `uid:*` | User ID | Search auth + API logs |
| `order:*`, `txn:*` | Transaction | Search API + DB logs |
| Timestamp | Time-based | Search all platforms around time |
| Error message | Error pattern | Search for matching errors |

### Phase 2: Collect Traces

Search each platform for related entries:

**Supabase API Logs**
```
mcp__plugin_supabase_supabase__get_logs(project_id, "api")
# Filter for trace identifier
```

**Supabase Auth Logs**
```
mcp__plugin_supabase_supabase__get_logs(project_id, "auth")
# Filter for user-related traces
```

**Supabase Postgres Logs**
```
mcp__plugin_supabase_supabase__get_logs(project_id, "postgres")
# Filter for query patterns
```

**Supabase Edge Functions**
```
mcp__plugin_supabase_supabase__get_logs(project_id, "edge-function")
# Filter for trace identifier
```

**GitHub Actions (if relevant)**
```bash
# Search for correlation in build logs
gh run list --limit 20
gh run view <id> --log 2>&1 | grep "<identifier>"
```

**Railway**
```bash
# Search service logs
railway logs 2>&1 | grep "<identifier>"
```

### Phase 3: Build Trace Timeline

Construct chronological flow:

```markdown
## Trace Timeline: {IDENTIFIER}

| Sequence | Time | Platform | Component | Event | Status |
|----------|------|----------|-----------|-------|--------|
| 1 | 14:30:01.123 | Supabase | API Gateway | Request received | OK |
| 2 | 14:30:01.125 | Supabase | Auth | JWT validated | OK |
| 3 | 14:30:01.130 | Supabase | Edge Func | Function invoked | OK |
| 4 | 14:30:01.145 | Supabase | Postgres | Query started | OK |
| 5 | 14:30:06.145 | Supabase | Postgres | Query timeout | ERROR |
| 6 | 14:30:06.150 | Supabase | Edge Func | Exception thrown | ERROR |
| 7 | 14:30:06.155 | Supabase | API Gateway | 500 returned | ERROR |
```

### Phase 4: Identify Failure Point

Analyze the trace to find:
1. **Last successful step**: Where things were still working
2. **First failure**: Where the problem started
3. **Cascade effects**: What failed as a result
4. **Root cause location**: The actual source of the problem

### Phase 5: Contextual Analysis

For the failure point, gather additional context:

**If Database-related**
```sql
-- Check for similar queries at that time
SELECT query, calls, mean_time, max_time
FROM pg_stat_statements
WHERE query LIKE '%pattern%'
ORDER BY max_time DESC;

-- Check for locks at that time (if within window)
SELECT * FROM pg_locks WHERE NOT granted;
```

**If API-related**
- Check rate limits
- Check payload sizes
- Check auth token validity

**If Edge Function-related**
- Check function logs for stack traces
- Check for timeout patterns
- Check memory/CPU usage if available

## Output Format

```markdown
# Trace Report

**Trace ID**: {IDENTIFIER}
**Type**: {Request / User / Transaction / Error}
**Time Range**: {START} to {END}

## Summary

{2-3 sentence summary of what was traced and findings}

## Request Flow

```
┌─────────────────────────────────────────────────────────────┐
│ Client                                                       │
│   │                                                          │
│   ▼                                                          │
│ ┌─────────────┐    ┌─────────────┐    ┌─────────────┐       │
│ │ API Gateway │───▶│ Edge Func   │───▶│ Postgres    │       │
│ │    (OK)     │    │    (OK)     │    │   (ERROR)   │       │
│ └─────────────┘    └─────────────┘    └─────────────┘       │
│                                             │                │
│                                        TIMEOUT               │
└─────────────────────────────────────────────────────────────┘
```

## Detailed Timeline

{Timeline table}

## Failure Analysis

### Failure Point
- **Location**: {Platform / Component}
- **Time**: {Timestamp}
- **Event**: {What happened}

### Error Details
```
{Error message / stack trace}
```

### Root Cause
{Analysis of why the failure occurred}

### Contributing Factors
- {Factor 1}
- {Factor 2}

## Related Entries

### Before Failure
{Log entries leading up to failure}

### At Failure
{Log entries at failure time}

### After Failure
{Cascade effects / cleanup}

## Recommendations

1. {Recommendation based on findings}
2. {Recommendation based on findings}

---
*Trace completed: {TIMESTAMP}*
*Related: `/infra:diagnose` for full diagnosis*
```

## Trace Correlation Strategies

### By Request ID
Most reliable when available. Look for:
- `x-request-id` header
- `trace-id` in logs
- `correlation-id` field

### By User ID
Useful for user-specific issues:
- Auth logs show login/token activity
- API logs show requests by user
- Database logs may show user context

### By Time Window
When no ID available:
- Narrow to specific minute
- Correlate events across platforms
- Look for matching patterns

### By Error Pattern
For recurring issues:
- Search for error message across all logs
- Group by timestamp
- Find common patterns

## Tips for Effective Tracing

1. **Start narrow, expand if needed**: Begin with tight time window
2. **Follow the data flow**: Client → API → Auth → Database
3. **Look for handoffs**: Where does data pass between services?
4. **Check both success and failure**: Compare working vs broken requests
5. **Note timing differences**: Unusual delays indicate problems
