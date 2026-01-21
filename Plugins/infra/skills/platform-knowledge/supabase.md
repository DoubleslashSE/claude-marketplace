# Supabase Platform Guide

## Overview

Supabase is an open-source Firebase alternative providing Postgres database, authentication, instant APIs, realtime subscriptions, storage, and edge functions.

## Architecture

```
Supabase Project
├── Database (Postgres)
│   ├── Schemas (public, auth, storage)
│   ├── Extensions
│   └── Migrations
├── Auth
│   ├── Providers (email, OAuth)
│   ├── Policies
│   └── Hooks
├── Storage
│   ├── Buckets
│   └── Policies
├── Realtime
│   └── Subscriptions
├── Edge Functions
└── API (PostgREST + Kong)
```

## MCP Tools Reference

### Project Management

```
mcp__plugin_supabase_supabase__list_projects
mcp__plugin_supabase_supabase__get_project(project_id)
```

### Database

```
mcp__plugin_supabase_supabase__list_tables(project_id, schemas)
mcp__plugin_supabase_supabase__list_extensions(project_id)
mcp__plugin_supabase_supabase__list_migrations(project_id)
mcp__plugin_supabase_supabase__execute_sql(project_id, query)
mcp__plugin_supabase_supabase__apply_migration(project_id, name, query)
```

### Monitoring

```
mcp__plugin_supabase_supabase__get_logs(project_id, service)
# Services: api, postgres, auth, storage, realtime, edge-function

mcp__plugin_supabase_supabase__get_advisors(project_id, type)
# Types: security, performance
```

### Configuration

```
mcp__plugin_supabase_supabase__get_project_url(project_id)
mcp__plugin_supabase_supabase__get_anon_key(project_id)
mcp__plugin_supabase_supabase__generate_typescript_types(project_id)
```

### Edge Functions

```
mcp__plugin_supabase_supabase__list_edge_functions(project_id)
mcp__plugin_supabase_supabase__get_edge_function(project_id, function_slug)
mcp__plugin_supabase_supabase__deploy_edge_function(project_id, name, ...)
```

## Authentication

### Configuration

Key settings in Auth dashboard:
- Site URL (for redirects)
- Redirect URLs (whitelist)
- JWT expiry
- Email templates
- OAuth providers

### Common Patterns

```sql
-- Get current user
SELECT auth.uid();

-- Get user role
SELECT auth.role();

-- Get JWT claims
SELECT auth.jwt();
```

### RLS with Auth

```sql
-- Allow users to read own data
CREATE POLICY "Users read own data"
ON user_profiles
FOR SELECT
USING (auth.uid() = user_id);

-- Allow users to update own data
CREATE POLICY "Users update own data"
ON user_profiles
FOR UPDATE
USING (auth.uid() = user_id);
```

### Troubleshooting Auth

**Login fails with `invalid_grant`**:
- Refresh token expired
- Clear stored tokens
- Re-authenticate

**Email not sending**:
- Check SMTP configuration
- Verify email templates
- Check rate limits

**OAuth redirect fails**:
- Verify redirect URL is whitelisted
- Check provider configuration
- Verify Site URL setting

## Row Level Security (RLS)

### Enable RLS

```sql
ALTER TABLE your_table ENABLE ROW LEVEL SECURITY;
```

### Policy Types

```sql
-- SELECT policy
CREATE POLICY "name" ON table FOR SELECT USING (condition);

-- INSERT policy
CREATE POLICY "name" ON table FOR INSERT WITH CHECK (condition);

-- UPDATE policy (both)
CREATE POLICY "name" ON table FOR UPDATE
USING (read_condition) WITH CHECK (write_condition);

-- DELETE policy
CREATE POLICY "name" ON table FOR DELETE USING (condition);

-- All operations
CREATE POLICY "name" ON table FOR ALL USING (condition);
```

### Common RLS Patterns

```sql
-- Public read, authenticated write
CREATE POLICY "Public read" ON posts
FOR SELECT USING (true);

CREATE POLICY "Auth write" ON posts
FOR INSERT WITH CHECK (auth.role() = 'authenticated');

-- User owns row
CREATE POLICY "Owner access" ON items
FOR ALL USING (auth.uid() = user_id);

-- Role-based
CREATE POLICY "Admin access" ON admin_data
FOR ALL USING (auth.jwt()->>'role' = 'admin');

-- Time-based
CREATE POLICY "Active only" ON subscriptions
FOR SELECT USING (expires_at > now());
```

### Debugging RLS

```sql
-- View policies on table
SELECT * FROM pg_policies WHERE tablename = 'your_table';

-- Test as specific user
SET request.jwt.claims = '{"sub": "user-uuid", "role": "authenticated"}';
SELECT * FROM your_table;
RESET request.jwt.claims;
```

## Realtime

### Enable Realtime

```sql
-- Enable on table
ALTER PUBLICATION supabase_realtime ADD TABLE your_table;

-- For UPDATE/DELETE events, need full replica identity
ALTER TABLE your_table REPLICA IDENTITY FULL;
```

### Troubleshooting Realtime

**Not receiving updates**:
1. Table added to publication?
2. REPLICA IDENTITY FULL set?
3. RLS allows SELECT?
4. Client subscribed correctly?

```sql
-- Check publication
SELECT * FROM pg_publication_tables
WHERE pubname = 'supabase_realtime';

-- Check replica identity
SELECT relreplident FROM pg_class WHERE relname = 'your_table';
-- 'f' = full, 'd' = default (pk only), 'n' = nothing
```

## Storage

### Bucket Policies

```sql
-- Public bucket
CREATE POLICY "Public read" ON storage.objects
FOR SELECT USING (bucket_id = 'public');

-- Authenticated upload
CREATE POLICY "Auth upload" ON storage.objects
FOR INSERT WITH CHECK (
  bucket_id = 'uploads'
  AND auth.role() = 'authenticated'
);

-- User folder pattern
CREATE POLICY "User folders" ON storage.objects
FOR ALL USING (
  bucket_id = 'user-files'
  AND (storage.foldername(name))[1] = auth.uid()::text
);
```

## Edge Functions

### Structure

```typescript
// supabase/functions/my-function/index.ts
import { serve } from "https://deno.land/std@0.168.0/http/server.ts"

serve(async (req) => {
  const { name } = await req.json()

  return new Response(
    JSON.stringify({ message: `Hello ${name}!` }),
    { headers: { "Content-Type": "application/json" } }
  )
})
```

### Deployment

```
mcp__plugin_supabase_supabase__deploy_edge_function(
  project_id,
  name,
  entrypoint_path,
  verify_jwt,
  files
)
```

### Troubleshooting Edge Functions

**Function not responding**:
- Check logs via MCP `get_logs`
- Verify deployment succeeded
- Check function URL

**CORS errors**:
```typescript
const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

// Handle OPTIONS
if (req.method === 'OPTIONS') {
  return new Response('ok', { headers: corsHeaders })
}
```

## Advisories

### Running Advisors

```
# Security advisors
mcp__plugin_supabase_supabase__get_advisors(project_id, "security")

# Performance advisors
mcp__plugin_supabase_supabase__get_advisors(project_id, "performance")
```

### Common Security Advisories

- RLS not enabled
- Public schema exposed
- Weak JWT configuration
- Storage policies missing

### Common Performance Advisories

- Missing indexes
- Large tables without vacuuming
- Inefficient queries
- Connection pool settings

## Quick Troubleshooting Checklist

### API Issues
- [ ] RLS enabled and policies correct?
- [ ] API key correct (anon vs service_role)?
- [ ] Endpoint path correct?
- [ ] Request format correct?

### Auth Issues
- [ ] Site URL configured?
- [ ] Redirect URL whitelisted?
- [ ] Email configured (if using)?
- [ ] OAuth provider configured?

### Database Issues
- [ ] Migrations applied?
- [ ] RLS policies allowing access?
- [ ] Indexes on queried columns?
- [ ] Connection pool not exhausted?

### Realtime Issues
- [ ] Table in publication?
- [ ] REPLICA IDENTITY FULL?
- [ ] RLS allows SELECT?
- [ ] Client subscription correct?
