---
description: Health check across all infrastructure platforms. Use to verify system health, check for advisories, and get an overall status report.
---

# Infrastructure Health Check

Run health check for: **$ARGUMENTS**

## Overview

This command performs comprehensive health checks across all your infrastructure platforms and generates a unified health report.

## Usage

```bash
/infra:health [platform] [--deep]
```

### Examples

```bash
# Quick health check all platforms
/infra:health

# Check specific platform
/infra:health supabase
/infra:health github
/infra:health railway
/infra:health postgres

# Deep/comprehensive check
/infra:health --deep
```

## Health Check Procedure

### Quick Check (Default)

Run these checks in parallel for speed:

**1. Supabase Health**
```
# Get security advisories
mcp__plugin_supabase_supabase__get_advisors(project_id, "security")

# Get performance advisories
mcp__plugin_supabase_supabase__get_advisors(project_id, "performance")

# Check for recent errors in API logs
mcp__plugin_supabase_supabase__get_logs(project_id, "api")
```

**2. GitHub Actions Health**
```bash
# Check recent run success rate
gh run list --limit 20 --json conclusion

# Check for any stuck runs
gh run list --status in_progress --limit 5
```

**3. Railway Health**
```bash
# Check service status
railway status

# Quick log check for errors
railway logs 2>&1 | tail -50 | grep -i "error\|fatal"
```

**4. Postgres Health**
```sql
-- Connection utilization
SELECT count(*)::float / (SELECT setting::int FROM pg_settings WHERE name = 'max_connections') * 100 AS pct
FROM pg_stat_activity;

-- Any blocked queries?
SELECT count(*) FROM pg_stat_activity WHERE cardinality(pg_blocking_pids(pid)) > 0;

-- Long-running queries?
SELECT count(*) FROM pg_stat_activity
WHERE state = 'active' AND query_start < now() - interval '5 minutes';
```

### Deep Check (--deep flag)

All quick checks plus:

**Postgres Extended**
```sql
-- Table sizes
SELECT schemaname || '.' || tablename AS table,
       pg_size_pretty(pg_total_relation_size(schemaname || '.' || tablename)) AS size
FROM pg_tables WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname || '.' || tablename) DESC
LIMIT 10;

-- Index usage
SELECT schemaname, tablename, indexrelname, idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0 AND indexrelname NOT LIKE '%pkey%'
LIMIT 10;

-- Tables needing maintenance
SELECT schemaname, tablename, n_dead_tup, last_vacuum, last_analyze
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY n_dead_tup DESC;

-- Replication status (if applicable)
SELECT * FROM pg_stat_replication;
```

**GitHub Actions Extended**
```bash
# Success rate over more runs
gh run list --limit 100 --json conclusion

# Check all workflows
gh workflow list --all
```

## Health Status Definitions

### GREEN - Healthy
- All services responding
- No critical advisories
- Error rate < 1%
- Resource utilization < 70%
- No blocked queries
- CI success rate > 90%

### YELLOW - Warning
- Minor advisories present
- Error rate 1-5%
- Resource utilization 70-85%
- Some long-running queries
- CI success rate 75-90%

### RED - Critical
- Security advisories present
- Error rate > 5%
- Resource utilization > 85%
- Blocked queries present
- Service unavailable
- CI success rate < 75%

## Output Format

```markdown
# Infrastructure Health Report

**Generated**: {TIMESTAMP}
**Check Type**: {Quick / Deep}

## Overall Status: {GREEN / YELLOW / RED}

```
┌─────────────────────────────────────────────────────────┐
│  GitHub Actions: {STATUS}  │  Railway: {STATUS}        │
├─────────────────────────────────────────────────────────┤
│  Supabase: {STATUS}        │  Postgres: {STATUS}       │
└─────────────────────────────────────────────────────────┘
```

## Platform Details

### GitHub Actions {STATUS_EMOJI}
- **Success Rate**: {N}% (last {N} runs)
- **In Progress**: {N} runs
- **Failed Recently**: {N} runs
- **Status**: {GREEN/YELLOW/RED}

### Railway {STATUS_EMOJI}
- **Services**: {N} running
- **Deployments**: Last deploy {TIME} ago
- **Recent Errors**: {N} in last hour
- **Status**: {GREEN/YELLOW/RED}

### Supabase {STATUS_EMOJI}
- **Security Advisories**: {N}
- **Performance Advisories**: {N}
- **API Error Rate**: {N}%
- **Status**: {GREEN/YELLOW/RED}

### Postgres {STATUS_EMOJI}
- **Connections**: {N}/{MAX} ({PCT}%)
- **Blocked Queries**: {N}
- **Long-running Queries**: {N}
- **Status**: {GREEN/YELLOW/RED}

## Advisories

### Security (Action Required)
{List security advisories with remediation links}

### Performance (Recommended)
{List performance advisories with remediation links}

## Action Items

### Immediate
{Critical issues requiring immediate attention}

### This Week
{Important issues to address soon}

### Monitor
{Items to keep an eye on}

---
*Next recommended check: {TIME}*
*For deeper analysis: `/infra:diagnose`*
```

## Advisory Handling

When advisories are found:

1. **Always include the remediation URL** as a clickable link
2. **Categorize by urgency**:
   - Security advisories = Immediate
   - Performance advisories = This Week
3. **Provide context** on impact if not addressed

## Follow-up Commands

Based on health check results, may recommend:
- `/infra:errors` - If error rate is elevated
- `/infra:diagnose` - If specific issues found
- `/infra:logs <platform>` - For more details on specific service
