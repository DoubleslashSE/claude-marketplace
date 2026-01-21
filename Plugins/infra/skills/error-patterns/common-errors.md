# Common Errors Catalog

## Database Errors

### Connection Errors

#### `FATAL: too many connections for role`

**Cause**: Connection pool exhausted or connection leak

**Immediate Fix**:
```sql
-- Check current connections
SELECT count(*), usename FROM pg_stat_activity GROUP BY usename;

-- Check max connections
SHOW max_connections;

-- Terminate idle connections (use carefully)
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE state = 'idle'
AND query_start < now() - interval '10 minutes';
```

**Root Cause Fix**:
- Implement connection pooling (Supavisor, PgBouncer)
- Add connection timeout settings
- Fix connection leaks in application

**Prevention**:
- Monitor connection count
- Alert at 80% capacity
- Use connection pooler

---

#### `connection refused` / `could not connect to server`

**Cause**: Database server unreachable

**Check**:
1. Is database service running?
2. Is network path clear?
3. Is connection string correct?
4. Is IP whitelisted?

**Immediate Fix**:
- Restart database service
- Check firewall rules
- Verify DNS resolution

---

#### `connection timeout`

**Cause**: Network latency or overloaded server

**Check**:
```sql
-- Check for blocking queries
SELECT * FROM pg_stat_activity WHERE state != 'idle';
```

**Immediate Fix**:
- Increase connection timeout
- Investigate slow queries
- Check network path

---

### Query Errors

#### `ERROR: statement timeout`

**Cause**: Query exceeded allowed execution time

**Check**:
```sql
-- Find the slow query
SELECT query, calls, mean_time, max_time
FROM pg_stat_statements
ORDER BY max_time DESC LIMIT 10;
```

**Immediate Fix**:
```sql
-- Increase timeout temporarily
SET statement_timeout = '60s';
```

**Root Cause Fix**:
- Add missing indexes
- Optimize query
- Reduce data set with better filters

---

#### `ERROR: deadlock detected`

**Cause**: Circular transaction locks

**Check**:
```sql
-- View locks
SELECT * FROM pg_locks WHERE NOT granted;
```

**Immediate Fix**:
```sql
-- Identify and terminate blocking transaction
SELECT pg_terminate_backend(pid);
```

**Root Cause Fix**:
- Ensure consistent lock ordering
- Reduce transaction scope
- Add retry logic

---

#### `ERROR: relation "table_name" does not exist`

**Cause**: Table missing or wrong schema

**Check**:
```sql
-- List tables in schema
SELECT table_name FROM information_schema.tables
WHERE table_schema = 'public';
```

**Fix**:
- Run missing migration
- Check schema prefix in query
- Verify deployment completed

---

### Permission Errors

#### `ERROR: permission denied for table`

**Cause**: Role lacks required privileges

**Check**:
```sql
-- Check grants
SELECT * FROM information_schema.role_table_grants
WHERE table_name = 'your_table';
```

**Fix**:
```sql
GRANT SELECT, INSERT, UPDATE ON your_table TO your_role;
```

---

## API Errors

### HTTP Status Codes

#### `401 Unauthorized`

**Cause**: Missing or invalid authentication

**Check**:
- Is Authorization header present?
- Is token format correct (Bearer)?
- Is token expired?
- Is token signed with correct key?

**Fix**:
- Refresh token
- Check token generation
- Verify JWT secret configuration

---

#### `403 Forbidden`

**Cause**: Authenticated but not authorized

**Check** (Supabase):
```sql
-- Check RLS policies
SELECT * FROM pg_policies WHERE tablename = 'your_table';
```

**Fix**:
- Update RLS policies
- Check user role/claims
- Verify resource ownership

---

#### `429 Too Many Requests`

**Cause**: Rate limit exceeded

**Check**:
- Review rate limit headers
- Check request patterns

**Immediate Fix**:
- Implement exponential backoff
- Reduce request frequency

**Root Cause Fix**:
- Add caching
- Batch requests
- Request rate limit increase

---

#### `500 Internal Server Error`

**Cause**: Unhandled server exception

**Check**:
- Server logs for stack trace
- Recent deployments
- Database connectivity

**Fix**:
- Deploy code fix
- Rollback if recent deployment
- Fix configuration

---

#### `502 Bad Gateway`

**Cause**: Upstream server unavailable

**Check**:
- Is upstream service running?
- Health check status
- Network connectivity

**Fix**:
- Restart upstream service
- Check service discovery
- Verify configuration

---

#### `503 Service Unavailable`

**Cause**: Server overloaded or maintenance

**Check**:
- CPU/memory usage
- Request queue depth
- Deployment in progress

**Fix**:
- Scale up resources
- Wait for deployment
- Investigate resource usage

---

#### `504 Gateway Timeout`

**Cause**: Upstream took too long

**Check**:
- Slow queries in logs
- Network latency
- Upstream service health

**Fix**:
- Optimize slow operations
- Increase timeouts
- Add caching

---

## Authentication Errors

### Supabase Auth

#### `invalid_grant`

**Cause**: Refresh token invalid or expired

**Fix**:
- Clear stored tokens
- Re-authenticate user
- Check token storage

---

#### `email_not_confirmed`

**Cause**: Email verification pending

**Fix**:
- Resend confirmation email
- Check email delivery
- Verify email configuration

---

#### `user_banned`

**Cause**: User account banned

**Fix**:
- Review ban reason
- Unban if appropriate
- Check audit logs

---

## Build/Deploy Errors

### GitHub Actions

#### `Process completed with exit code 1`

**Cause**: Command/script failed

**Check**:
- Command output above error
- Exit code meaning for specific tool

**Common causes**:
- Test failures
- Lint errors
- Build errors
- Missing dependencies

---

#### `Resource not accessible by integration`

**Cause**: GitHub App/Action lacks permissions

**Fix**:
- Check workflow permissions block
- Verify token scope
- Check repository settings

---

### Railway

#### `Build failed`

**Cause**: Build command error

**Check**:
- Build logs
- Package.json scripts
- Environment variables

**Fix**:
- Fix build script
- Add missing dependencies
- Set required env vars

---

#### `Health check failed`

**Cause**: App not responding to health check

**Check**:
- Is app listening on correct port?
- Does health endpoint return 200?
- Is startup fast enough?

**Fix**:
```toml
# railway.toml
[deploy]
healthcheckPath = "/health"
healthcheckTimeout = 300
```

---

## Resource Errors

### Memory

#### `ENOMEM` / `JavaScript heap out of memory`

**Cause**: Process exceeded memory limit

**Check**:
- Memory usage trends
- Memory leaks in application
- Data size being processed

**Immediate Fix**:
```bash
# Node.js
NODE_OPTIONS="--max-old-space-size=4096"
```

**Root Cause Fix**:
- Profile memory usage
- Fix memory leaks
- Implement streaming for large data

---

### Disk

#### `ENOSPC: no space left on device`

**Cause**: Disk full

**Check**:
```bash
df -h
du -sh /* | sort -rh | head -10
```

**Fix**:
- Clean up old files
- Increase disk size
- Archive old data

---

### CPU

#### Service slow/unresponsive

**Cause**: CPU saturation

**Check**:
- CPU usage metrics
- Running processes
- Slow operations

**Fix**:
- Optimize CPU-intensive operations
- Add caching
- Scale horizontally

---

## Network Errors

### DNS

#### `ENOTFOUND` / `getaddrinfo failed`

**Cause**: DNS resolution failed

**Check**:
```bash
nslookup hostname
dig hostname
```

**Fix**:
- Verify hostname spelling
- Check DNS configuration
- Use IP temporarily

---

### Timeout

#### `ETIMEDOUT`

**Cause**: Connection attempt timed out

**Check**:
- Is target reachable?
- Firewall rules
- Network path

**Fix**:
- Increase timeout
- Check security groups
- Verify endpoint

---

### Connection Reset

#### `ECONNRESET`

**Cause**: Connection forcibly closed

**Check**:
- Server logs for errors
- Load balancer timeouts
- Keep-alive settings

**Fix**:
- Implement retry logic
- Check timeout configurations
- Verify server health
