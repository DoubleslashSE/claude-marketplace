---
description: Full diagnostic workflow for infrastructure issues. Use when something is broken and you need comprehensive troubleshooting.
---

# Infrastructure Diagnosis

Diagnose issue: **$ARGUMENTS**

## Overview

This command runs a comprehensive diagnostic workflow to identify and resolve infrastructure issues. It combines log analysis, error pattern recognition, health checks, and root cause analysis.

## Usage

```bash
/infra:diagnose [issue description]
```

### Examples

```bash
# General diagnosis
/infra:diagnose "app not responding"

# Specific error diagnosis
/infra:diagnose "500 errors on /api/users"

# Performance issue
/infra:diagnose "slow database queries"

# Deployment problem
/infra:diagnose "deployment failed"
```

## Diagnostic Workflow

### Phase 1: Issue Characterization

**Gather Information**

If not provided in arguments, ask:
1. What is the symptom? (errors, slowness, unavailability)
2. When did it start?
3. Is it affecting all users or specific ones?
4. What changed recently? (deployments, config changes)
5. Is it consistent or intermittent?

**Establish Scope**

Determine which platforms might be involved:
- API errors → Supabase API, Edge Functions
- Database errors → Postgres, Supabase
- Build failures → GitHub Actions
- Deployment issues → Railway, GitHub Actions
- Auth problems → Supabase Auth

### Phase 2: Evidence Collection

Run these checks based on issue type:

**For All Issues**
```
# Check for recent errors across platforms
- Supabase: mcp__plugin_supabase_supabase__get_logs (api, postgres, auth)
- GitHub: gh run list --status failure --limit 5
- Railway: railway logs | grep -i error

# Check advisories
- mcp__plugin_supabase_supabase__get_advisors (security)
- mcp__plugin_supabase_supabase__get_advisors (performance)
```

**For Database Issues**
```sql
-- Connection status
SELECT state, count(*) FROM pg_stat_activity GROUP BY state;

-- Long-running queries
SELECT pid, now() - query_start AS duration, query
FROM pg_stat_activity WHERE state = 'active'
ORDER BY duration DESC LIMIT 5;

-- Blocked queries
SELECT blocked.pid, blocked.query, blocking.pid AS blocker, blocking.query
FROM pg_stat_activity blocked
JOIN pg_stat_activity blocking ON blocking.pid = ANY(pg_blocking_pids(blocked.pid));

-- Recent errors
SELECT * FROM pg_stat_activity WHERE state = 'idle in transaction';
```

**For API Issues**
```
# Check API logs for error patterns
mcp__plugin_supabase_supabase__get_logs(project_id, "api")

# Check edge function logs if applicable
mcp__plugin_supabase_supabase__get_logs(project_id, "edge-function")
```

**For Deployment Issues**
```bash
# GitHub Actions
gh run list --limit 10
gh run view <latest-failed> --log-failed

# Railway
railway status
railway logs
```

### Phase 3: Timeline Construction

Build a timeline of events:

```markdown
## Event Timeline

| Time | Source | Event | Significance |
|------|--------|-------|--------------|
| T-4h | GitHub | Deployment completed | Last known good |
| T-2h | GitHub | New deployment | Potential trigger |
| T-1h | Supabase | First 500 error | Issue started |
| T-30m | Supabase | Error rate spike | Escalation |
| Now | - | Diagnosis started | - |
```

### Phase 4: Root Cause Analysis

Apply the 5 Whys technique:

```
Symptom: API returning 500 errors
├── Why? Database connection timeout
│   ├── Why? Connection pool exhausted
│   │   ├── Why? Connections not released
│   │   │   ├── Why? Error handler missing cleanup
│   │   │   │   └── Why? Recent code change
│   │   │   │       └── ROOT CAUSE: Commit abc123 removed finally block
```

Consider common root causes:
- **Recent deployments**: What code changed?
- **Configuration changes**: Environment variables, secrets?
- **External dependencies**: Third-party service issues?
- **Resource exhaustion**: Connections, memory, disk?
- **Traffic spikes**: Unusual load patterns?

### Phase 5: Health Check

Run comprehensive health check to assess current state:

```
/infra:health --deep
```

Verify:
- Which services are affected
- Current error rates
- Resource utilization
- Any cascading failures

### Phase 6: Remediation Plan

Based on findings, create actionable plan:

```markdown
## Remediation Plan

### Immediate Actions (Do Now)
1. {Specific action with commands/steps}
2. {Specific action with commands/steps}

### Short-term Fix (Today)
1. {Specific action}
2. {Specific action}

### Long-term Prevention
1. {Monitoring/alerting to add}
2. {Code/config changes to prevent recurrence}
```

## Output Format

```markdown
# Diagnostic Report

**Issue**: {DESCRIPTION}
**Reported**: {TIME}
**Status**: {Investigating / Root Cause Found / Resolved}

## Summary

{2-3 sentence summary of findings}

## Severity Assessment

**Severity**: {CRITICAL / HIGH / MEDIUM / LOW}
**Impact**: {Who/what is affected}
**Scope**: {Percentage of users/requests affected}

## Timeline

{Event timeline table}

## Evidence

### Logs
{Key log entries supporting diagnosis}

### Metrics
{Relevant metrics/stats}

### Health Check Results
{Summary of health check}

## Root Cause

**Root Cause**: {Clear statement of underlying issue}

**Contributing Factors**:
- {Factor 1}
- {Factor 2}

**Evidence Supporting This Conclusion**:
- {Evidence 1}
- {Evidence 2}

## Remediation

### Immediate (Do Now)
- [ ] {Action 1}
- [ ] {Action 2}

### Short-term (This Week)
- [ ] {Action 1}
- [ ] {Action 2}

### Prevention (Long-term)
- [ ] {Monitoring to add}
- [ ] {Code changes}
- [ ] {Process improvements}

## Verification Steps

After remediation:
1. {How to verify fix worked}
2. {What metrics to monitor}
3. {When to consider issue resolved}

---
*Diagnosis completed: {TIMESTAMP}*
```

## Escalation Criteria

Recommend escalation when:
- Unable to determine root cause after 30 minutes
- Issue affects >50% of users
- Data loss is suspected
- Security breach indicators
- Issue is getting worse despite investigation

## Related Commands

- `/infra:logs <platform>` - Get detailed logs
- `/infra:errors` - Focus on error analysis
- `/infra:health` - Run health check
- `/infra:trace <id>` - Trace specific request/error
