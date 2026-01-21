# Health Check Checklists

## Quick Health Check Checklist

**Time**: ~5 minutes
**When**: After deployments, start of day, incident investigation

### GitHub Actions
- [ ] Check recent run status: `gh run list --limit 5`
- [ ] Any stuck runs? `gh run list --status in_progress`
- [ ] Recent failures? `gh run list --status failure --limit 3`

### Railway
- [ ] Services running: `railway status`
- [ ] Recent errors in logs: `railway logs 2>&1 | grep -i error | tail -10`

### Supabase
- [ ] Check for advisories: `get_advisors(type: "security")`
- [ ] Check API logs for errors: `get_logs(service: "api")`

### Postgres
- [ ] Connection count OK:
  ```sql
  SELECT count(*) FROM pg_stat_activity;
  ```
- [ ] No blocked queries:
  ```sql
  SELECT count(*) FROM pg_stat_activity
  WHERE cardinality(pg_blocking_pids(pid)) > 0;
  ```

---

## Daily Health Check Checklist

**Time**: ~15 minutes
**When**: Start of business day

### All Quick Checks Plus:

### GitHub Actions
- [ ] 24-hour success rate:
  ```bash
  gh run list --limit 50 --json conclusion
  ```
- [ ] No workflows stuck > 1 hour

### Railway
- [ ] All deployments successful
- [ ] Resource utilization within limits
- [ ] No repeated restarts in logs

### Supabase
- [ ] Review all advisories:
  - [ ] Security advisories: `get_advisors(type: "security")`
  - [ ] Performance advisories: `get_advisors(type: "performance")`
- [ ] Auth service healthy: `get_logs(service: "auth")`
- [ ] Realtime service healthy: `get_logs(service: "realtime")`
- [ ] Edge functions healthy: `get_logs(service: "edge-function")`

### Postgres
- [ ] Connection utilization < 70%:
  ```sql
  SELECT round(count(*)::numeric /
    (SELECT setting::int FROM pg_settings WHERE name = 'max_connections') * 100, 2)
  FROM pg_stat_activity;
  ```
- [ ] No long-running queries > 5 min:
  ```sql
  SELECT count(*) FROM pg_stat_activity
  WHERE state = 'active' AND query_start < now() - interval '5 minutes';
  ```
- [ ] No idle-in-transaction > 10 min:
  ```sql
  SELECT count(*) FROM pg_stat_activity
  WHERE state = 'idle in transaction'
  AND query_start < now() - interval '10 minutes';
  ```

---

## Weekly Health Check Checklist

**Time**: ~30 minutes
**When**: Beginning of week

### All Daily Checks Plus:

### GitHub Actions
- [ ] Review workflow efficiency
- [ ] Check cache hit rates
- [ ] Identify flaky tests
- [ ] Review build times trend

### Railway
- [ ] Review deployment history
- [ ] Check for memory/CPU trends
- [ ] Verify environment variables current
- [ ] Check domain/SSL status

### Supabase
- [ ] Review storage usage
- [ ] Check auth provider status
- [ ] Review RLS policies are adequate
- [ ] Verify realtime publication config

### Postgres
- [ ] Index usage analysis:
  ```sql
  SELECT indexrelname, idx_scan
  FROM pg_stat_user_indexes
  WHERE idx_scan = 0
  AND indexrelname NOT LIKE '%pkey%';
  ```
- [ ] Table bloat check:
  ```sql
  SELECT schemaname || '.' || relname, n_dead_tup, n_live_tup
  FROM pg_stat_user_tables
  WHERE n_dead_tup > 1000
  ORDER BY n_dead_tup DESC LIMIT 10;
  ```
- [ ] Table sizes review:
  ```sql
  SELECT schemaname || '.' || tablename,
    pg_size_pretty(pg_total_relation_size(schemaname || '.' || tablename))
  FROM pg_tables
  WHERE schemaname = 'public'
  ORDER BY pg_total_relation_size(schemaname || '.' || tablename) DESC
  LIMIT 10;
  ```
- [ ] Query performance review (top 5 slow):
  ```sql
  SELECT query, calls, round(mean_exec_time::numeric, 2) as avg_ms
  FROM pg_stat_statements
  ORDER BY mean_exec_time DESC LIMIT 5;
  ```

---

## Monthly Deep Check Checklist

**Time**: 1+ hours
**When**: Beginning of month

### All Weekly Checks Plus:

### GitHub Actions
- [ ] Audit workflow permissions
- [ ] Review secret rotation needs
- [ ] Optimize workflow caching
- [ ] Review action version pins
- [ ] Check for deprecated actions

### Railway
- [ ] Review resource allocation
- [ ] Audit environment variables
- [ ] Check for orphaned services
- [ ] Review scaling configuration
- [ ] Cost analysis

### Supabase
- [ ] Full security audit:
  - [ ] RLS policies complete
  - [ ] No public access without intent
  - [ ] Auth settings secure
  - [ ] Storage policies adequate
- [ ] Performance optimization:
  - [ ] Edge function performance
  - [ ] API response times
  - [ ] Realtime efficiency
- [ ] Review database extensions
- [ ] Check backup status

### Postgres
- [ ] Full index analysis:
  ```sql
  -- Unused indexes
  SELECT schemaname, tablename, indexrelname, idx_scan,
    pg_size_pretty(pg_relation_size(indexrelid))
  FROM pg_stat_user_indexes WHERE idx_scan = 0;

  -- Missing indexes (high seq scan tables)
  SELECT schemaname, relname, seq_scan, seq_tup_read, n_live_tup
  FROM pg_stat_user_tables
  WHERE seq_scan > idx_scan AND n_live_tup > 10000;
  ```
- [ ] Query optimization review:
  ```sql
  -- Most resource-intensive queries
  SELECT query, calls, total_exec_time, mean_exec_time, rows
  FROM pg_stat_statements
  ORDER BY total_exec_time DESC LIMIT 10;
  ```
- [ ] Table maintenance:
  ```sql
  -- Tables needing vacuum
  SELECT schemaname, relname, n_dead_tup, last_vacuum, last_autovacuum
  FROM pg_stat_user_tables
  WHERE n_dead_tup > 10000;

  -- Run vacuum on needed tables
  VACUUM ANALYZE table_name;
  ```
- [ ] Connection pool optimization
- [ ] Capacity planning (growth projections)

---

## Incident Response Checklist

**When**: During active incident

### Immediate Assessment
- [ ] What is the impact? (Users affected, data at risk)
- [ ] When did it start?
- [ ] What changed recently?
- [ ] Is it getting worse?

### Evidence Collection
- [ ] Gather logs from all platforms
- [ ] Check for correlated errors
- [ ] Build timeline of events
- [ ] Document current state

### Mitigation
- [ ] Can we rollback?
- [ ] Can we scale?
- [ ] Can we route around?
- [ ] Who needs to be notified?

### Resolution
- [ ] Root cause identified?
- [ ] Fix deployed?
- [ ] Service restored?
- [ ] Verification complete?

### Post-Incident
- [ ] Timeline documented
- [ ] Root cause documented
- [ ] Prevention measures identified
- [ ] Postmortem scheduled

---

## Pre-Deployment Checklist

**When**: Before production deployment

### Code
- [ ] All tests passing
- [ ] No security vulnerabilities
- [ ] Database migrations reviewed
- [ ] Feature flags in place (if needed)

### Infrastructure
- [ ] Environment variables updated
- [ ] Database capacity adequate
- [ ] Monitoring in place
- [ ] Rollback plan ready

### Process
- [ ] Deployment window confirmed
- [ ] Team notified
- [ ] Runbook available
- [ ] On-call aware

### Post-Deploy
- [ ] Quick health check passed
- [ ] No error spike
- [ ] Key features verified
- [ ] Monitoring normal

---

## Post-Incident Checklist

**When**: After incident resolution

### Documentation
- [ ] Timeline complete
- [ ] Root cause documented
- [ ] Impact quantified
- [ ] Resolution documented

### Follow-up
- [ ] Prevention tasks created
- [ ] Monitoring improved
- [ ] Runbook updated
- [ ] Team retrospective scheduled

### Communication
- [ ] Status page updated
- [ ] Affected users notified
- [ ] Internal report shared
- [ ] External postmortem (if needed)
