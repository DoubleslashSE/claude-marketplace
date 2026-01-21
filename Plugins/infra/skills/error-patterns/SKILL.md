---
name: error-patterns
description: Error recognition and diagnosis patterns for infrastructure troubleshooting. Use when identifying, categorizing, or resolving errors across platforms.
allowed-tools: Bash, Grep, Read, mcp__plugin_supabase_supabase__get_logs, mcp__plugin_supabase_supabase__execute_sql
---

# Error Patterns Skill

## Overview

This skill provides knowledge for recognizing, categorizing, and resolving common infrastructure errors. It covers error classification, diagnostic techniques, and resolution strategies.

## Error Classification Framework

### By Severity

| Severity | Definition | Response Time | Example |
|----------|------------|---------------|---------|
| **Critical** | Service completely down | Immediate | Database unreachable |
| **High** | Major functionality broken | < 1 hour | Auth failures |
| **Medium** | Partial functionality affected | < 4 hours | Slow queries |
| **Low** | Minor issues, workarounds exist | < 24 hours | Deprecation warnings |

### By Category

| Category | Subcategories | Typical Causes |
|----------|---------------|----------------|
| **Database** | Connection, Query, Transaction, Replication | Pool exhaustion, locks, slow queries |
| **Network** | DNS, Timeout, Connection | Misconfiguration, service down |
| **Authentication** | Token, Permission, Provider | Expired tokens, wrong credentials |
| **Application** | Logic, Memory, Timeout | Bugs, resource leaks |
| **Infrastructure** | Disk, CPU, Memory | Resource exhaustion |
| **External** | API, Service, Rate limit | Third-party issues |

### By Pattern Type

| Pattern | Description | Example |
|---------|-------------|---------|
| **Transient** | Self-resolving, retry works | Network blip |
| **Persistent** | Consistent, needs fix | Misconfiguration |
| **Cascading** | One failure causes others | DB down → API errors |
| **Intermittent** | Random occurrence | Race condition |
| **Load-dependent** | Appears under load | Connection exhaustion |

## Diagnostic Methodology

### The 5 Whys

Dig deeper for root cause:

```
Symptom: API returning 500 errors
  Why? → Database query failing
    Why? → Connection timeout
      Why? → Connection pool exhausted
        Why? → Connections not released
          Why? → Missing finally block in error handler

ROOT CAUSE: Code bug in error handling
```

### Timeline Analysis

Map events chronologically:

```
T-60m: Deployment completed
T-45m: Memory usage started climbing
T-30m: First slow query warning
T-15m: Connection pool warnings
T-0:   Service unavailable
```

### Fault Tree

Break down possible causes:

```
                [Service Down]
                      |
        +-------------+-------------+
        |             |             |
    [Database]    [Network]    [Application]
        |             |             |
    +---+---+     +---+---+     +---+---+
    |       |     |       |     |       |
 [Conn]  [Query] [DNS]  [FW]  [OOM]  [Bug]
```

## Error Resolution Process

### Step 1: Identify
- What is the exact error message?
- When did it start?
- What's the impact?

### Step 2: Categorize
- Which category does this fall into?
- Is it transient or persistent?
- What's the severity?

### Step 3: Investigate
- Gather relevant logs
- Check recent changes
- Look for patterns

### Step 4: Diagnose
- Apply 5 Whys
- Build timeline
- Identify root cause

### Step 5: Remediate
- Apply immediate fix
- Verify resolution
- Document for prevention

## Error Correlation Techniques

### Cross-Platform Correlation

Match errors across systems:

```
14:30:01 [Railway]  Connection refused to db:5432
14:30:01 [Supabase] Too many connections
14:30:00 [GitHub]   Deployment completed
↑ Deployment triggered connection spike
```

### Error Chains

Follow the cascade:

```
[1] Initial: Database connection timeout
[2] Result:  API endpoint returns 500
[3] Result:  Frontend shows error page
[4] Result:  User reports "site is down"
```

### Impact Mapping

```
Error: Auth service down
├── Direct Impact
│   └── No new logins
├── Cascade Impact
│   ├── API requests fail (no token validation)
│   └── Realtime connections drop
└── User Impact
    └── All users affected
```

## Resolution Strategies

### Immediate Mitigation

| Strategy | Use When | Example |
|----------|----------|---------|
| **Rollback** | Recent deployment caused issue | `git revert` |
| **Restart** | Service stuck/crashed | Container restart |
| **Scale up** | Resource exhaustion | Add replicas |
| **Failover** | Primary system down | Switch to backup |
| **Rate limit** | Overload | Block/throttle traffic |
| **Circuit break** | Cascading failures | Disable failing component |

### Root Cause Fix

| Cause | Fix Approach |
|-------|--------------|
| Code bug | Deploy fix, add tests |
| Configuration | Update config, validate |
| Resource limit | Increase limits or optimize |
| External dependency | Add retry/fallback |
| Infrastructure | Scale or redesign |

### Prevention

| Issue | Prevention |
|-------|------------|
| Connection leaks | Connection pooling, timeouts |
| Memory leaks | Profiling, limits |
| Slow queries | Indexes, query optimization |
| Deployment failures | Canary deployments, rollback automation |
| External failures | Circuit breakers, fallbacks |

## Common Resolution Templates

### Database Connection Issues

```markdown
## Issue: Database Connection Error

### Immediate Actions
1. Check connection count:
   SELECT count(*) FROM pg_stat_activity;
2. Identify idle connections:
   SELECT * FROM pg_stat_activity WHERE state = 'idle in transaction';
3. Kill stuck connections if safe:
   SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE ...;

### Root Cause Fix
- Add connection pooling (PgBouncer)
- Implement connection timeouts
- Fix connection leak in application code

### Prevention
- Monitor connection metrics
- Alert on pool usage > 80%
- Regular connection audits
```

### API Error Spike

```markdown
## Issue: API 500 Errors

### Immediate Actions
1. Check API logs for error pattern
2. Identify failing endpoint(s)
3. Check downstream dependencies

### Root Cause Fix
- Fix code bug causing exception
- Handle edge cases
- Add proper error handling

### Prevention
- Add error monitoring
- Implement circuit breakers
- Add integration tests
```

See [common-errors.md](common-errors.md) for a catalog of specific errors and solutions.
