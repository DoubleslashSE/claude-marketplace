---
name: log-analysis
description: Log parsing techniques and analysis methodologies for infrastructure troubleshooting. Use when retrieving, parsing, or analyzing logs from any platform.
allowed-tools: Bash, Grep, Read, mcp__plugin_supabase_supabase__get_logs
---

# Log Analysis Skill

## Overview

This skill provides techniques for effective log parsing, analysis, and insight extraction across infrastructure platforms. It covers log formats, parsing strategies, pattern recognition, and analysis methodologies.

## Log Analysis Fundamentals

### Log Anatomy

Every log entry typically contains:

```
[TIMESTAMP] [LEVEL] [SOURCE] [MESSAGE] [CONTEXT]
```

**Key Fields**:
- **Timestamp**: When the event occurred (critical for correlation)
- **Level**: Severity (DEBUG, INFO, WARN, ERROR, FATAL)
- **Source**: Component that generated the log
- **Message**: Human-readable description
- **Context**: Additional metadata (request ID, user ID, etc.)

### Log Levels

| Level | Use | Action Required |
|-------|-----|-----------------|
| FATAL | System cannot continue | Immediate |
| ERROR | Operation failed | Investigate |
| WARN | Potential problem | Monitor |
| INFO | Normal operation | None (audit) |
| DEBUG | Diagnostic detail | None (troubleshoot) |

## Parsing Strategies

### Structured Logs (JSON)

Most modern systems emit JSON logs:

```json
{
  "timestamp": "2024-01-15T14:30:00.123Z",
  "level": "error",
  "message": "Database connection failed",
  "service": "api",
  "request_id": "req-abc123",
  "error": {
    "code": "CONN_TIMEOUT",
    "detail": "Connection timed out after 30000ms"
  }
}
```

**Parsing approach**:
1. Parse JSON structure
2. Extract standard fields
3. Flatten nested objects for analysis
4. Group by common attributes

### Unstructured Logs (Plain Text)

Legacy systems often use plain text:

```
2024-01-15 14:30:00 ERROR [api.handler] Database connection failed: timeout after 30s
```

**Parsing approach**:
1. Identify timestamp format with regex
2. Extract level using keyword matching
3. Parse source from brackets/prefixes
4. Remainder is message

### Mixed Format Logs

Some systems mix formats:

```
[14:30:00] INFO: Starting request processing {"request_id": "abc123"}
```

**Parsing approach**:
1. Split structured from unstructured portions
2. Parse each portion with appropriate strategy
3. Merge results

## Analysis Techniques

### Time-Based Analysis

**Windowing**: Group events by time period

```
Window: 1 minute
14:30 - 14:31: 5 errors
14:31 - 14:32: 12 errors  ← Spike detected
14:32 - 14:33: 3 errors
```

**Correlation**: Match events across systems by timestamp

```
14:30:01.123 [API]      Request received
14:30:01.125 [Auth]     Token validated
14:30:01.130 [Database] Query started
14:30:01.145 [Database] Query completed
14:30:01.147 [API]      Response sent
```

### Pattern Recognition

**Error Clustering**: Group similar errors

```
Pattern: "Connection refused to {host}:{port}"
Instances:
  - Connection refused to db-1:5432 (15 times)
  - Connection refused to db-2:5432 (3 times)
```

**Anomaly Detection**: Identify unusual patterns

```
Normal: 10-20 requests/second
Current: 500 requests/second ← Anomaly
```

### Frequency Analysis

**Count by category**:

| Error Type | Count | % of Total |
|------------|-------|------------|
| Connection timeout | 45 | 60% |
| Auth failure | 20 | 27% |
| Validation error | 10 | 13% |

**Trend analysis**:

```
Hour 1: 10 errors
Hour 2: 15 errors
Hour 3: 25 errors ← Trending up
Hour 4: 50 errors ← Accelerating
```

### Root Cause Indicators

**First occurrence**: Often indicates trigger

```
First error: 14:30:01 - "Failed to connect to new endpoint"
Subsequent: 14:30:02+ - "Connection pool exhausted"
```

**Cascade patterns**: Later errors caused by earlier ones

```
14:30:01 [DB] Connection failed
14:30:02 [API] Database unavailable
14:30:02 [API] Database unavailable
14:30:03 [API] Database unavailable
        ↑ Cascade from initial DB failure
```

## Log Retrieval Commands

### Supabase

```
# Available services
api, postgres, auth, storage, realtime, edge-function

# MCP command
mcp__plugin_supabase_supabase__get_logs(project_id, service)
```

### GitHub Actions

```bash
# List runs
gh run list --limit 20

# Get logs
gh run view <run-id> --log
gh run view <run-id> --log-failed
```

### Railway

```bash
# Recent logs
railway logs

# Follow live
railway logs --follow
```

## Output Formatting

### Summary Format

```markdown
## Log Analysis Summary

**Time Range**: {START} to {END}
**Total Entries**: {COUNT}
**Error Rate**: {PCT}%

### By Level
| Level | Count | % |
|-------|-------|---|
| ERROR | 50 | 5% |
| WARN | 100 | 10% |
| INFO | 850 | 85% |

### Top Errors
1. {Error 1} - {count} occurrences
2. {Error 2} - {count} occurrences

### Timeline
{Key events in chronological order}

### Recommendations
{Based on patterns found}
```

### Detailed Format

For specific error investigation:

```markdown
## Error Details: {ERROR_TYPE}

**First Seen**: {TIMESTAMP}
**Last Seen**: {TIMESTAMP}
**Occurrences**: {COUNT}

### Sample Entry
```
{Full log entry}
```

### Context
{Surrounding log entries}

### Pattern
{What triggers this error}

### Impact
{What this error affects}
```

See [patterns.md](patterns.md) for platform-specific log patterns.
