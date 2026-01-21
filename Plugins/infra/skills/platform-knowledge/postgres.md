# Postgres Platform Guide

## Overview

PostgreSQL is a powerful, open-source relational database system with strong reliability, feature robustness, and performance.

## Key Concepts

### Connections

```
Max Connections = base + superuser_reserved
- base: Regular connection limit
- superuser_reserved: Reserved for admin (default: 3)

Connection States:
- idle: Waiting for query
- active: Executing query
- idle in transaction: In transaction, waiting
- idle in transaction (aborted): Failed transaction
```

### Schemas

```
Database
├── public (default user schema)
├── auth (Supabase auth)
├── storage (Supabase storage)
├── extensions (Extension objects)
└── pg_catalog (System catalog)
```

### Roles and Permissions

```sql
-- Supabase roles
anon        -- Unauthenticated API access
authenticated  -- Authenticated API access
service_role   -- Bypasses RLS
postgres    -- Superuser
```

## Health Queries

### Connection Monitoring

```sql
-- Current connections by state
SELECT state, count(*)
FROM pg_stat_activity
GROUP BY state
ORDER BY count DESC;

-- Connections by user
SELECT usename, count(*)
FROM pg_stat_activity
GROUP BY usename
ORDER BY count DESC;

-- Connections by application
SELECT application_name, count(*)
FROM pg_stat_activity
WHERE application_name != ''
GROUP BY application_name
ORDER BY count DESC;

-- Connection utilization
SELECT
  count(*) AS current,
  (SELECT setting::int FROM pg_settings WHERE name = 'max_connections') AS max,
  round(count(*)::numeric /
    (SELECT setting::int FROM pg_settings WHERE name = 'max_connections') * 100, 2) AS pct
FROM pg_stat_activity;
```

### Query Monitoring

```sql
-- Currently running queries
SELECT
  pid,
  usename,
  application_name,
  state,
  now() - query_start AS duration,
  query
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY duration DESC;

-- Long-running queries (>5 min)
SELECT
  pid,
  usename,
  now() - query_start AS duration,
  query
FROM pg_stat_activity
WHERE state = 'active'
AND query_start < now() - interval '5 minutes'
ORDER BY duration DESC;

-- Queries with most calls (requires pg_stat_statements)
SELECT
  query,
  calls,
  round(total_exec_time::numeric / 1000, 2) AS total_seconds,
  round(mean_exec_time::numeric, 2) AS avg_ms
FROM pg_stat_statements
ORDER BY calls DESC
LIMIT 10;

-- Slowest queries
SELECT
  query,
  calls,
  round(mean_exec_time::numeric, 2) AS avg_ms,
  round(max_exec_time::numeric, 2) AS max_ms
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;
```

### Lock Monitoring

```sql
-- Current locks
SELECT
  relation::regclass,
  mode,
  granted,
  pid
FROM pg_locks
WHERE relation IS NOT NULL
ORDER BY relation;

-- Blocked queries
SELECT
  blocked.pid AS blocked_pid,
  blocked.usename AS blocked_user,
  blocked.query AS blocked_query,
  blocking.pid AS blocking_pid,
  blocking.usename AS blocking_user,
  blocking.query AS blocking_query
FROM pg_stat_activity blocked
JOIN pg_stat_activity blocking
ON blocking.pid = ANY(pg_blocking_pids(blocked.pid));

-- Lock wait times
SELECT
  pid,
  usename,
  now() - query_start AS wait_time,
  query
FROM pg_stat_activity
WHERE wait_event_type = 'Lock'
ORDER BY wait_time DESC;
```

### Table Statistics

```sql
-- Table sizes
SELECT
  schemaname || '.' || tablename AS table,
  pg_size_pretty(pg_total_relation_size(schemaname || '.' || tablename)) AS total_size,
  pg_size_pretty(pg_table_size(schemaname || '.' || tablename)) AS table_size,
  pg_size_pretty(pg_indexes_size(schemaname || '.' || tablename)) AS index_size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname || '.' || tablename) DESC;

-- Row counts
SELECT
  schemaname || '.' || tablename AS table,
  n_live_tup AS row_count,
  n_dead_tup AS dead_rows
FROM pg_stat_user_tables
ORDER BY n_live_tup DESC;

-- Tables needing vacuum
SELECT
  schemaname || '.' || tablename AS table,
  n_dead_tup AS dead_rows,
  last_vacuum,
  last_autovacuum
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY n_dead_tup DESC;
```

### Index Statistics

```sql
-- Index usage
SELECT
  schemaname || '.' || tablename AS table,
  indexrelname AS index,
  idx_scan AS scans,
  idx_tup_read AS tuples_read,
  pg_size_pretty(pg_relation_size(indexrelid)) AS size
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;

-- Unused indexes
SELECT
  schemaname || '.' || tablename AS table,
  indexrelname AS index,
  pg_size_pretty(pg_relation_size(indexrelid)) AS size
FROM pg_stat_user_indexes
WHERE idx_scan = 0
AND indexrelname NOT LIKE '%pkey%';

-- Missing index suggestions (from seq scans)
SELECT
  schemaname || '.' || relname AS table,
  seq_scan,
  seq_tup_read,
  idx_scan,
  n_live_tup AS rows
FROM pg_stat_user_tables
WHERE seq_scan > idx_scan
AND n_live_tup > 10000
ORDER BY seq_tup_read DESC;
```

### Database Size

```sql
-- Database size
SELECT pg_size_pretty(pg_database_size(current_database()));

-- Total size by schema
SELECT
  schema_name,
  pg_size_pretty(sum(table_size)) AS total_size
FROM (
  SELECT
    pg_catalog.pg_namespace.nspname AS schema_name,
    pg_relation_size(pg_catalog.pg_class.oid) AS table_size
  FROM pg_catalog.pg_class
  JOIN pg_catalog.pg_namespace ON relnamespace = pg_namespace.oid
) t
GROUP BY schema_name
ORDER BY sum(table_size) DESC;
```

## Performance Optimization

### Query Optimization

```sql
-- Explain query plan
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM your_table WHERE condition;

-- Key things to look for:
-- - Seq Scan on large tables (add index)
-- - High cost estimates
-- - Actual time much higher than planned
-- - Many rows filtered (improve WHERE)
```

### Index Guidelines

```sql
-- B-tree (default) - equality, range
CREATE INDEX idx_name ON table(column);

-- Multi-column - for combined queries
CREATE INDEX idx_name ON table(col1, col2);

-- Partial - for filtered queries
CREATE INDEX idx_active ON table(column) WHERE active = true;

-- Expression - for computed values
CREATE INDEX idx_lower ON table(lower(email));

-- Covering - include columns for index-only scans
CREATE INDEX idx_name ON table(key) INCLUDE (data);
```

### Common Optimizations

```sql
-- Add missing primary key index
CREATE INDEX IF NOT EXISTS idx_table_id ON table(id);

-- Index foreign keys
CREATE INDEX IF NOT EXISTS idx_table_fk ON table(foreign_key_id);

-- Index frequently filtered columns
CREATE INDEX IF NOT EXISTS idx_table_status ON table(status);

-- Analyze table statistics
ANALYZE table_name;

-- Vacuum dead rows
VACUUM table_name;
VACUUM ANALYZE table_name;
```

## Troubleshooting

### Connection Issues

**Too many connections**:
```sql
-- Find and terminate idle connections
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE state = 'idle'
AND query_start < now() - interval '10 minutes'
AND usename != 'postgres';
```

**Connection refused**:
- Check max_connections setting
- Verify connection string
- Check firewall/security groups
- Verify role exists and has permissions

### Query Issues

**Slow queries**:
1. Run EXPLAIN ANALYZE
2. Check for Seq Scans
3. Add appropriate indexes
4. Check table statistics (ANALYZE)

**Deadlocks**:
```sql
-- View deadlock info (after the fact)
SELECT * FROM pg_stat_activity
WHERE state = 'idle in transaction';

-- Prevention
-- - Acquire locks in consistent order
-- - Keep transactions short
-- - Use appropriate isolation levels
```

**Statement timeout**:
```sql
-- Check current setting
SHOW statement_timeout;

-- Set for session
SET statement_timeout = '60s';

-- Set for query
SET LOCAL statement_timeout = '120s';
```

### Space Issues

**Disk full**:
```sql
-- Find largest tables
SELECT
  schemaname || '.' || tablename AS table,
  pg_size_pretty(pg_total_relation_size(schemaname || '.' || tablename)) AS size
FROM pg_tables
ORDER BY pg_total_relation_size(schemaname || '.' || tablename) DESC
LIMIT 10;

-- Vacuum to reclaim space
VACUUM FULL table_name;

-- Delete old data
DELETE FROM logs WHERE created_at < now() - interval '30 days';
```

**Table bloat**:
```sql
-- Check for bloat
SELECT
  schemaname || '.' || tablename AS table,
  n_dead_tup AS dead_rows,
  n_live_tup AS live_rows,
  round(n_dead_tup::numeric / nullif(n_live_tup, 0) * 100, 2) AS dead_pct
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY dead_pct DESC;

-- Fix bloat
VACUUM ANALYZE table_name;
```

## Configuration

### Key Settings

```sql
-- View settings
SHOW max_connections;
SHOW statement_timeout;
SHOW work_mem;
SHOW shared_buffers;

-- Common settings
max_connections = 100          -- Connection limit
statement_timeout = '30s'      -- Query timeout
work_mem = '64MB'              -- Memory per operation
shared_buffers = '256MB'       -- Shared memory
```

### Connection Pooling

For high-traffic applications, use a connection pooler:
- **PgBouncer**: Lightweight, session/transaction pooling
- **Supavisor**: Supabase's pooler

## Extensions

### Common Extensions

```sql
-- List installed extensions
SELECT * FROM pg_extension;

-- Useful extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";  -- UUID functions
CREATE EXTENSION IF NOT EXISTS "pgcrypto";   -- Encryption
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";  -- Query stats
CREATE EXTENSION IF NOT EXISTS "pg_trgm";    -- Fuzzy text search
```

## Quick Checklist

### Performance
- [ ] Indexes on frequently queried columns?
- [ ] Indexes on foreign keys?
- [ ] Table statistics up to date (ANALYZE)?
- [ ] No excessive dead rows (VACUUM)?
- [ ] Appropriate work_mem setting?

### Connections
- [ ] Connection pooling enabled?
- [ ] Reasonable max_connections?
- [ ] No connection leaks in application?
- [ ] Idle connections being cleaned up?

### Monitoring
- [ ] pg_stat_statements enabled?
- [ ] Logging slow queries?
- [ ] Monitoring connection count?
- [ ] Alerting on lock contention?
