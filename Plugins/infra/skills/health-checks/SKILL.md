---
name: health-checks
description: Health monitoring knowledge and procedures for infrastructure platforms. Use when assessing system health, running health audits, or setting up monitoring.
allowed-tools: Bash, Grep, Read, mcp__plugin_supabase_supabase__get_advisors, mcp__plugin_supabase_supabase__execute_sql, mcp__plugin_supabase_supabase__get_logs
---

# Health Checks Skill

## Overview

This skill provides knowledge and procedures for monitoring infrastructure health across GitHub Actions, Railway, Supabase, and Postgres.

## Health Check Philosophy

### Why Regular Health Checks?

1. **Proactive Detection**: Find issues before users do
2. **Trend Identification**: Spot degradation early
3. **Capacity Planning**: Know when to scale
4. **Compliance**: Maintain system hygiene
5. **Documentation**: Track system state over time

### Health Check Frequency

| Check Type | Frequency | When |
|------------|-----------|------|
| Quick | Every deploy | After any deployment |
| Daily | Daily | Morning/start of business |
| Weekly | Weekly | Beginning of week |
| Deep | Monthly | Beginning of month |
| Full Audit | Quarterly | Scheduled maintenance window |

## Health Status Framework

### Traffic Light System

```
GREEN  - All systems healthy
         - No critical issues
         - Metrics within normal ranges
         - Advisory count: 0

YELLOW - Warning state
         - Non-critical issues present
         - Metrics approaching limits
         - Performance advisories present

RED    - Critical state
         - Service impaired or unavailable
         - Critical metrics exceeded
         - Security advisories present
         - Immediate action required
```

### Status Determination Rules

| Condition | Status |
|-----------|--------|
| Security advisory exists | RED |
| Service unavailable | RED |
| Error rate > 5% | RED |
| Connection utilization > 85% | RED |
| CI success rate < 75% | RED |
| Performance advisory exists | YELLOW |
| Error rate 1-5% | YELLOW |
| Connection utilization 70-85% | YELLOW |
| CI success rate 75-90% | YELLOW |
| Long-running queries present | YELLOW |
| All metrics normal | GREEN |

## Health Metrics

### Key Performance Indicators

| Platform | Metric | Good | Warning | Critical |
|----------|--------|------|---------|----------|
| **Database** | Connection % | <70% | 70-85% | >85% |
| **Database** | Query Duration | <100ms | 100-500ms | >500ms |
| **Database** | Dead Rows % | <10% | 10-20% | >20% |
| **API** | Error Rate | <1% | 1-5% | >5% |
| **API** | Response Time P95 | <500ms | 500-2000ms | >2000ms |
| **CI/CD** | Success Rate | >90% | 75-90% | <75% |
| **CI/CD** | Build Time | <5min | 5-15min | >15min |

### Platform-Specific Metrics

#### Supabase
- API error rate
- Auth failure rate
- Storage utilization
- Edge function cold starts
- Realtime connection count
- Advisory count (security/performance)

#### GitHub Actions
- Workflow success rate
- Average build time
- Queue wait time
- Cache hit rate
- Failed workflow count

#### Railway
- Service uptime
- Deploy success rate
- Memory utilization
- CPU utilization
- Health check pass rate

#### Postgres
- Connection utilization
- Query duration distribution
- Lock contention
- Dead tuple ratio
- Index usage efficiency
- Table bloat

## Health Check Procedures

### Quick Health Check (5 min)

Purpose: Verify basic system functionality

```
1. [ ] Check for active incidents (any platform)
2. [ ] Verify all services responding
3. [ ] Check for critical advisories
4. [ ] Review last hour error rate
5. [ ] Check connection pool status
```

### Daily Health Check (15 min)

Purpose: Assess overall system health

```
1. [ ] Run quick health check
2. [ ] Review 24-hour error trends
3. [ ] Check CI/CD success rate
4. [ ] Review all advisories
5. [ ] Check slow query log
6. [ ] Verify backups completed
7. [ ] Review resource utilization
```

### Weekly Health Check (30 min)

Purpose: Comprehensive review and trending

```
1. [ ] Run daily health check
2. [ ] Analyze weekly error patterns
3. [ ] Review index usage stats
4. [ ] Check for table bloat
5. [ ] Review connection patterns
6. [ ] Assess capacity trends
7. [ ] Review deployment frequency
8. [ ] Check certificate expirations
```

### Monthly Deep Check (1+ hours)

Purpose: Full system audit

```
1. [ ] Run weekly health check
2. [ ] Full index analysis
3. [ ] Query performance review
4. [ ] Security configuration audit
5. [ ] Capacity planning review
6. [ ] Cost analysis
7. [ ] Documentation review
8. [ ] Disaster recovery test
```

## Alert Thresholds

### Immediate Alerts (Page)

- Service unavailable > 1 minute
- Error rate > 10%
- Database connections > 90%
- Security advisory created
- Deployment failure (production)
- Health check failure > 5 minutes

### Warning Alerts (Slack/Email)

- Error rate > 2%
- Database connections > 75%
- Performance advisory created
- Build time increase > 50%
- Response time P95 > 1s
- Disk usage > 80%

### Info Alerts (Daily Digest)

- New advisory (any type)
- Build time change
- Resource trend change
- Configuration change

## Health Report Template

```markdown
# Infrastructure Health Report

**Generated**: {TIMESTAMP}
**Report Type**: {Quick | Daily | Weekly | Monthly}
**Overall Status**: {GREEN | YELLOW | RED}

## Executive Summary
{2-3 sentence overview}

## Platform Status

| Platform | Status | Issues | Warnings |
|----------|--------|--------|----------|
| GitHub Actions | {STATUS} | {N} | {N} |
| Railway | {STATUS} | {N} | {N} |
| Supabase | {STATUS} | {N} | {N} |
| Postgres | {STATUS} | {N} | {N} |

## Key Metrics

### Database
- Connections: {N}/{MAX} ({PCT}%)
- Query P95: {MS}ms
- Dead Rows: {PCT}%

### API
- Error Rate: {PCT}%
- Response Time P95: {MS}ms

### CI/CD
- Success Rate: {PCT}%
- Avg Build Time: {MIN}m

## Advisories

### Security
{List or "None"}

### Performance
{List or "None"}

## Issues Requiring Attention

### Immediate
{List or "None"}

### This Week
{List or "None"}

## Trends

{Notable changes from previous period}

## Recommendations

{Specific actions to improve health}

---
*Next health check: {TIMESTAMP}*
```

## Remediation Playbooks

### High Connection Utilization

```
1. Check for connection leaks
2. Identify idle connections
3. Review connection pool settings
4. Consider connection pooler (PgBouncer/Supavisor)
5. Optimize application connection handling
```

### High Error Rate

```
1. Identify error types
2. Check recent deployments
3. Review affected endpoints
4. Check downstream dependencies
5. Roll back if deployment-related
```

### Slow Queries

```
1. Identify slow queries (pg_stat_statements)
2. Run EXPLAIN ANALYZE
3. Check for missing indexes
4. Review query patterns
5. Consider query optimization or caching
```

### Build Failures

```
1. Review failure logs
2. Check for flaky tests
3. Verify dependencies available
4. Check for environment issues
5. Review recent changes
```

See [checklists.md](checklists.md) for detailed health check checklists.
