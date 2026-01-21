# Railway Platform Guide

## Overview

Railway is a deployment platform that provides instant deploys, automatic SSL, and environment management for applications.

## Architecture

```
Railway Project
├── Environments (dev, staging, prod)
│   └── Services
│       ├── Application (from GitHub)
│       ├── Database (Postgres, Redis, etc.)
│       └── Cron Jobs
└── Variables (Environment-specific)
```

## Configuration Files

### railway.toml

```toml
[build]
# Build settings
builder = "nixpacks"          # or "dockerfile"
buildCommand = "npm run build"
watchPatterns = ["src/**"]

[deploy]
# Deployment settings
startCommand = "npm start"
healthcheckPath = "/health"
healthcheckTimeout = 300      # seconds
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 3

[environments]
# Environment overrides
[environments.production]
[environments.production.deploy]
healthcheckTimeout = 100
```

### nixpacks.toml

```toml
[phases.setup]
nixPkgs = ["nodejs-18_x", "yarn"]

[phases.install]
cmds = ["yarn install"]

[phases.build]
cmds = ["yarn build"]

[start]
cmd = "yarn start"
```

### Procfile

```
web: npm start
worker: npm run worker
```

## Deployment Process

```
1. Git Push / Manual Deploy
         │
         ▼
2. Build Phase (nixpacks/Dockerfile)
         │
         ▼
3. Deploy Phase (start command)
         │
         ▼
4. Health Check
         │
         ├── Pass → Traffic routed
         └── Fail → Rollback
```

## CLI Reference

### Project Management

```bash
# Login
railway login

# Link to project
railway link

# View project info
railway status

# Open dashboard
railway open
```

### Environment Variables

```bash
# List variables
railway variables

# Set variable
railway variables set KEY=value

# Delete variable
railway variables delete KEY

# Show in different environment
railway variables --environment production
```

### Deployments

```bash
# Deploy current directory
railway up

# View deployment status
railway status

# View logs
railway logs
railway logs --follow
railway logs --deployment <id>
```

### Services

```bash
# List services
railway service list

# View service info
railway service

# Create new service
railway service create
```

## Common Issues and Solutions

### Build Failures

**Nixpacks detection failed**:
```toml
# Specify provider in nixpacks.toml
providers = ["node"]
```

**Missing system dependencies**:
```toml
[phases.setup]
nixPkgs = ["pkg-config", "openssl"]
aptPkgs = ["libssl-dev"]
```

**Build command not found**:
```toml
[build]
buildCommand = "npm run build"  # Must match package.json
```

### Deployment Failures

**Health check failing**:
1. Ensure app binds to `0.0.0.0`, not `localhost`
2. Use correct PORT environment variable
3. Increase healthcheckTimeout

```javascript
// Correct port binding
const port = process.env.PORT || 3000;
app.listen(port, '0.0.0.0', () => {
  console.log(`Server running on port ${port}`);
});
```

**Start command failing**:
```toml
[deploy]
startCommand = "node dist/index.js"  # Full path needed
```

### Environment Variables

**Variable not loading**:
- Check environment is correct (dev vs prod)
- Verify variable is linked to service
- Redeploy after adding variable

**Reference other variables**:
```bash
# Railway supports variable references
DATABASE_URL=${{Postgres.DATABASE_URL}}
```

### Memory/Resource Issues

**Out of memory**:
- Check memory limit in Railway dashboard
- Optimize application memory usage
- Consider splitting services

**Cold starts**:
- Railway sleeps inactive services (free tier)
- Add keep-alive pings
- Upgrade to paid plan

## Connection Strings

### Postgres

```
postgresql://user:password@host:port/database
```

Available as `DATABASE_URL` when Postgres service is added.

### Redis

```
redis://user:password@host:port
```

Available as `REDIS_URL` when Redis service is added.

### Connecting to Supabase

```bash
# Set Supabase URL and key as variables
railway variables set SUPABASE_URL=https://xxx.supabase.co
railway variables set SUPABASE_KEY=your-anon-key
railway variables set SUPABASE_SERVICE_KEY=your-service-key
```

## Networking

### Custom Domains

1. Add domain in Railway dashboard
2. Configure DNS CNAME to `railway.app`
3. SSL automatically provisioned

### Private Networking

Services in same project can communicate via internal DNS:
```
http://service-name.railway.internal
```

### TCP Proxy

For non-HTTP services (databases, etc.):
1. Enable TCP proxy in service settings
2. Use provided external port

## Debugging

### View Logs

```bash
# Recent logs
railway logs

# Follow live
railway logs -f

# Specific deployment
railway logs --deployment <deployment-id>

# Search for errors
railway logs 2>&1 | grep -i error
```

### Check Status

```bash
# Project status
railway status

# Deployment status
# Check dashboard for detailed status
railway open
```

### Local Testing

```bash
# Run with Railway variables
railway run npm start

# Shell with variables
railway shell
```

## Best Practices

### Deployment

```toml
# Always configure health checks
[deploy]
healthcheckPath = "/health"
healthcheckTimeout = 60

# Set restart policy
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 3
```

### Environment Management

```bash
# Use separate environments
railway environment create staging
railway environment create production

# Set environment-specific variables
railway variables set NODE_ENV=production --environment production
```

### Monitoring

1. Set up log drains for external monitoring
2. Configure alerting on deployment failures
3. Monitor resource usage in dashboard

### Security

1. Never commit secrets to repository
2. Use Railway variables for all secrets
3. Use service keys (not anon) for server-side Supabase access
4. Restrict access via project members

## Quick Troubleshooting Checklist

- [ ] Build command matches package.json script?
- [ ] Start command correct and path complete?
- [ ] App listening on `0.0.0.0:$PORT`?
- [ ] Health check endpoint returning 200?
- [ ] All required environment variables set?
- [ ] Variables in correct environment?
- [ ] Memory limits sufficient?
- [ ] Recent changes deployed?
