# Platform-Specific Log Patterns

## Supabase Log Patterns

### API Gateway Logs

**Request Log Format**:
```json
{
  "timestamp": "ISO8601",
  "method": "GET|POST|PUT|DELETE|PATCH",
  "path": "/rest/v1/table",
  "status_code": 200,
  "response_time": 45,
  "request_id": "uuid",
  "user_agent": "string"
}
```

**Common Patterns**:

| Pattern | Meaning | Action |
|---------|---------|--------|
| `status_code: 401` | Unauthorized | Check auth token |
| `status_code: 403` | Forbidden | Check RLS policies |
| `status_code: 404` | Not found | Check path/resource |
| `status_code: 429` | Rate limited | Reduce request rate |
| `status_code: 500` | Server error | Check postgres logs |
| `response_time > 1000` | Slow request | Check query performance |

### Postgres Logs

**Error Log Format**:
```
2024-01-15 14:30:00.123 UTC [pid] LOG: statement: SELECT ...
2024-01-15 14:30:00.456 UTC [pid] ERROR: relation "table" does not exist
2024-01-15 14:30:00.789 UTC [pid] FATAL: too many connections
```

**Common Patterns**:

| Pattern | Meaning | Action |
|---------|---------|--------|
| `ERROR: relation ... does not exist` | Missing table | Check migrations |
| `ERROR: permission denied` | Auth issue | Check RLS/grants |
| `ERROR: duplicate key` | Constraint violation | Handle in app |
| `ERROR: deadlock detected` | Transaction conflict | Review transactions |
| `FATAL: too many connections` | Pool exhaustion | Scale connections |
| `FATAL: password authentication failed` | Wrong credentials | Check secrets |
| `LOG: duration: Xms` | Slow query logged | Optimize query |
| `ERROR: statement timeout` | Query killed | Optimize or increase timeout |

**Connection States**:
```sql
-- Healthy distribution
idle: Many (connections waiting)
active: Few (executing queries)
idle in transaction: Few (should release)
```

**Warning Signs**:
- High `idle in transaction` count → Connection leak
- High `active` with slow queries → Query optimization needed
- Approaching `max_connections` → Scale or optimize

### Auth Logs

**Login Event Format**:
```json
{
  "timestamp": "ISO8601",
  "event": "login|signup|logout|token_refresh",
  "user_id": "uuid",
  "provider": "email|google|github|...",
  "success": true|false,
  "error": "optional error message"
}
```

**Common Patterns**:

| Pattern | Meaning | Action |
|---------|---------|--------|
| Multiple failed logins | Brute force attempt | Rate limit/block |
| `invalid_grant` | Bad refresh token | User needs to re-login |
| `user_not_found` | Unknown email | Expected for typos |
| `email_not_confirmed` | Unverified email | Resend confirmation |
| `invalid_credentials` | Wrong password | Expected for typos |
| Provider errors | OAuth issue | Check provider config |

### Edge Function Logs

**Execution Log Format**:
```json
{
  "timestamp": "ISO8601",
  "function": "function-name",
  "execution_id": "uuid",
  "status": "success|error",
  "duration_ms": 150,
  "memory_used_mb": 32,
  "logs": ["console output"]
}
```

**Common Patterns**:

| Pattern | Meaning | Action |
|---------|---------|--------|
| `status: error` | Unhandled exception | Check stack trace |
| High `duration_ms` | Slow function | Optimize code |
| High `memory_used_mb` | Memory pressure | Optimize memory |
| Timeout errors | Exceeded limit | Optimize or split |

## GitHub Actions Log Patterns

### Workflow Run Logs

**Run Status**:
```
✓ completed (success)
✗ completed (failure)
○ in_progress
⊘ cancelled
```

**Common Failure Patterns**:

| Pattern | Meaning | Action |
|---------|---------|--------|
| `Process completed with exit code 1` | Command failed | Check command output |
| `Error: Resource not accessible` | Permission issue | Check token/secrets |
| `Error: HttpError: rate limit` | API rate limited | Wait and retry |
| `##[error]` | Step error marker | Read following message |
| `ENOENT: no such file` | Missing file | Check paths |
| `npm ERR!` | NPM failure | Check dependencies |
| `FATAL ERROR: ... JavaScript heap` | OOM | Increase memory |

**Timeout Patterns**:
```
The job running on runner ... has exceeded the maximum execution time
```

**Cache Patterns**:
```
Cache not found for input keys: ...   # Cache miss
Cache restored from key: ...           # Cache hit
```

### Test Failure Patterns

```
FAIL src/tests/example.test.ts
  ✕ should do something (5ms)

  Expected: "expected"
  Received: "actual"
```

**Common Test Patterns**:

| Pattern | Meaning | Action |
|---------|---------|--------|
| `FAIL` | Test failed | Check assertion |
| `Timeout` | Test too slow | Increase timeout or optimize |
| `Cannot find module` | Import error | Check dependencies |
| `ReferenceError` | Undefined variable | Check test setup |

## Railway Log Patterns

### Application Logs

**Standard Output Format**:
```
[timestamp] [level] message
```

**Health Check Patterns**:
```
Health check failed: Connection refused
Health check passed
```

**Deployment Patterns**:
```
Deploying from ...
Build started
Build completed in X seconds
Deploy started
Deploy completed
```

**Common Patterns**:

| Pattern | Meaning | Action |
|---------|---------|--------|
| `ECONNREFUSED` | Service unreachable | Check networking |
| `ETIMEDOUT` | Connection timeout | Check target service |
| `ENOMEM` | Out of memory | Increase resources |
| `SIGTERM` | Graceful shutdown | Expected on redeploy |
| `SIGKILL` | Forced termination | OOM or timeout |
| Port already in use | Binding issue | Check PORT env |

### Build Logs

**Nixpacks Patterns**:
```
==> Building with Nixpacks
==> Installing dependencies
==> Running build command
```

**Common Build Failures**:

| Pattern | Meaning | Action |
|---------|---------|--------|
| `npm install` failure | Dependency issue | Check package.json |
| `Build command failed` | Build script error | Check build output |
| `No Procfile found` | Missing start command | Add Procfile or railway.toml |

## Log Correlation Strategies

### By Request ID

Look for consistent request/correlation IDs across services:

```
[API]      request_id=abc123 - Request started
[Auth]     request_id=abc123 - Token validated
[Database] request_id=abc123 - Query executed
[API]      request_id=abc123 - Response sent
```

### By Timestamp

Match events within a tight time window:

```
14:30:01.100 [Service A] Event 1
14:30:01.105 [Service B] Event 2  ← ~5ms later
14:30:01.110 [Service A] Event 3  ← ~10ms after Event 1
```

### By User/Session

Track user journey:

```
user_id=user123 - Login
user_id=user123 - View dashboard
user_id=user123 - Submit order
user_id=user123 - Error: payment failed
```

## Pattern Matching Regex

### Error Extraction
```regex
# Generic error line
(?i)(error|fail|fatal|exception|crash)

# HTTP status codes
status[_:]?\s*(\d{3})

# Stack traces
at\s+[\w.]+\([^)]+\)

# Timestamps
\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}
```

### Postgres Specific
```regex
# Error messages
^ERROR:\s*(.+)$

# Duration logging
duration:\s*([\d.]+)\s*ms

# Connection info
connection.*from\s+([\d.]+)
```

### Performance Metrics
```regex
# Response times
response[_-]?time[=:]\s*([\d.]+)

# Memory usage
memory[=:]\s*([\d.]+)\s*(MB|GB|KB)

# CPU usage
cpu[=:]\s*([\d.]+)%
```
