---
description: Quick build check without full validation
---

# Build Check

Build: **$ARGUMENTS**

## Build Command

```bash
# Standard build
dotnet build --no-incremental

# Release build
dotnet build --configuration Release --no-incremental

# Specific project
dotnet build path/to/Project.csproj --no-incremental
```

## What This Checks

- **Compilation**: All code compiles without errors
- **References**: All project and package references resolve
- **Syntax**: No syntax errors in code
- **Types**: All type references are valid

## Common Build Errors

| Code | Description | Quick Fix |
|------|-------------|-----------|
| CS0103 | Name not found | Check spelling, add using |
| CS0246 | Type not found | Add package/project reference |
| CS1061 | Member not found | Check type, fix member name |
| CS0029 | Type conversion | Add cast or fix types |
| MSB3202 | Project not found | Fix ProjectReference path |

## Output Format

```markdown
## Build Report

### Status: PASS/FAIL

### Build Output
{Build command output}

### Errors (if any)
| Location | Code | Message |
|----------|------|---------|
| File.cs:45 | CS0103 | The name 'x' does not exist |

### Warnings (if any)
| Location | Code | Message |
|----------|------|---------|
| File.cs:23 | CS0168 | Variable declared but never used |

### Summary
- Projects Built: X
- Errors: X
- Warnings: X
- Duration: Xs

### Next Steps
- PASS: Run `/dotnet-developer:validate` for full check
- FAIL: Fix errors and rebuild
```

## Quick Troubleshooting

**Restore packages first:**
```bash
dotnet restore
```

**Clear caches:**
```bash
dotnet nuget locals all --clear
```

**Clean before build:**
```bash
dotnet clean && dotnet build
```

## Usage

```
/dotnet-developer:build                    # Build solution
/dotnet-developer:build src/MyApp          # Build specific project
/dotnet-developer:build --release          # Release configuration
```
