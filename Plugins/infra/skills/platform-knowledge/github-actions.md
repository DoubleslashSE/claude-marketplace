# GitHub Actions Platform Guide

## Overview

GitHub Actions is a CI/CD platform that automates build, test, and deployment workflows directly from GitHub repositories.

## Architecture

```
Repository
├── .github/
│   ├── workflows/          # Workflow definitions
│   │   ├── ci.yml
│   │   └── deploy.yml
│   └── actions/            # Custom actions
│       └── my-action/
│           └── action.yml
```

## Workflow Structure

```yaml
name: CI                          # Workflow name
on:                               # Triggers
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:                              # Global env vars
  NODE_VERSION: '20'

jobs:
  build:                          # Job ID
    runs-on: ubuntu-latest        # Runner
    strategy:                     # Matrix builds
      matrix:
        node: [18, 20]
    steps:
      - uses: actions/checkout@v4 # Action
      - run: npm install          # Command
```

## Key Concepts

### Triggers (on)

```yaml
# Push/PR triggers
on:
  push:
    branches: [main]
    paths:
      - 'src/**'
    tags:
      - 'v*'
  pull_request:
    types: [opened, synchronize]

# Scheduled triggers
on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight

# Manual triggers
on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Deploy environment'
        required: true
        default: 'staging'
```

### Jobs and Steps

```yaml
jobs:
  job1:
    runs-on: ubuntu-latest
    outputs:
      version: ${{ steps.get-version.outputs.version }}
    steps:
      - id: get-version
        run: echo "version=1.0.0" >> $GITHUB_OUTPUT

  job2:
    needs: job1  # Dependency
    runs-on: ubuntu-latest
    steps:
      - run: echo ${{ needs.job1.outputs.version }}
```

### Environment and Secrets

```yaml
jobs:
  deploy:
    environment: production  # Environment (for approvals)
    env:
      NODE_ENV: production
    steps:
      - run: echo ${{ secrets.API_KEY }}
      - run: echo ${{ vars.PUBLIC_URL }}
```

### Caching

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-npm-
```

### Artifacts

```yaml
# Upload
- uses: actions/upload-artifact@v4
  with:
    name: build
    path: dist/

# Download
- uses: actions/download-artifact@v4
  with:
    name: build
```

## Debugging

### Enable Debug Logging

Set repository secret:
```
ACTIONS_STEP_DEBUG = true
```

### View Logs via CLI

```bash
# List recent runs
gh run list --limit 20

# View run status
gh run view <run-id>

# View full logs
gh run view <run-id> --log

# View failed step logs only
gh run view <run-id> --log-failed

# Watch running workflow
gh run watch <run-id>

# Re-run failed jobs
gh run rerun <run-id> --failed
```

### Debug Locally with act

```bash
# Install act
brew install act

# Run workflow locally
act push

# Run specific job
act -j build

# Run with secrets
act -s MY_SECRET=value
```

## Common Issues and Solutions

### Workflow Not Triggering

**Check**:
1. Branch name matches trigger
2. Path filters don't exclude changes
3. Workflow file syntax is valid
4. No `[skip ci]` in commit message

**Debug**:
```yaml
# Add to see what triggered
- run: |
    echo "Event: ${{ github.event_name }}"
    echo "Ref: ${{ github.ref }}"
    echo "SHA: ${{ github.sha }}"
```

### Secrets Not Available

**Common causes**:
- Secret defined in org, not repo
- Fork PR (secrets hidden by default)
- Wrong environment scope
- Typo in secret name

**Check**:
```yaml
- run: |
    if [ -z "${{ secrets.MY_SECRET }}" ]; then
      echo "Secret is empty!"
    fi
```

### Cache Miss

**Check**:
```yaml
- uses: actions/cache@v4
  id: cache
  with:
    path: ~/.npm
    key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}

- if: steps.cache.outputs.cache-hit != 'true'
  run: echo "Cache miss - installing fresh"
```

### Out of Memory

**Solutions**:
```yaml
# Increase Node memory
- run: npm run build
  env:
    NODE_OPTIONS: '--max-old-space-size=4096'

# Use larger runner
runs-on: ubuntu-latest-4-cores
```

### Timeout

**Adjust limits**:
```yaml
jobs:
  build:
    timeout-minutes: 30  # Job timeout
    steps:
      - run: npm test
        timeout-minutes: 10  # Step timeout
```

## Best Practices

### Workflow Efficiency

```yaml
# Use concurrency to cancel redundant runs
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

# Fail fast in matrix
strategy:
  fail-fast: true
  matrix:
    node: [18, 20, 22]
```

### Security

```yaml
# Minimal permissions
permissions:
  contents: read
  packages: write

# Pin action versions
- uses: actions/checkout@v4.1.1  # Specific version

# Validate inputs
- run: |
    if [[ ! "${{ inputs.env }}" =~ ^(dev|staging|prod)$ ]]; then
      echo "Invalid environment"
      exit 1
    fi
```

### Reusable Workflows

```yaml
# .github/workflows/reusable-build.yml
on:
  workflow_call:
    inputs:
      node-version:
        required: true
        type: string
    secrets:
      npm-token:
        required: true

# Usage
jobs:
  build:
    uses: ./.github/workflows/reusable-build.yml
    with:
      node-version: '20'
    secrets:
      npm-token: ${{ secrets.NPM_TOKEN }}
```

## Useful Expressions

```yaml
# Conditionals
if: github.ref == 'refs/heads/main'
if: contains(github.event.head_commit.message, '[deploy]')
if: always()  # Run even if previous failed
if: failure()  # Run only if previous failed

# String operations
${{ format('Hello {0}', github.actor) }}
${{ join(matrix.node, ', ') }}

# JSON
${{ toJSON(github.event) }}
${{ fromJSON(steps.output.outputs.data).version }}
```

## CLI Reference

```bash
# Workflows
gh workflow list
gh workflow view <name>
gh workflow run <name>
gh workflow disable <name>
gh workflow enable <name>

# Runs
gh run list [--status success|failure|...]
gh run view <id> [--log|--log-failed]
gh run watch <id>
gh run rerun <id> [--failed]
gh run cancel <id>
gh run download <id>

# Secrets
gh secret list
gh secret set NAME
gh secret delete NAME
```
