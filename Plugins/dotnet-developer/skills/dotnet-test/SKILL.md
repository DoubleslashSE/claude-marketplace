---
name: dotnet-test
description: .NET test execution patterns and diagnostics. Use when running tests, analyzing test failures, or configuring test options.
allowed-tools: Read, Grep, Glob, Bash
---

# .NET Test Execution

## Basic Test Commands

```bash
# Run all tests in solution
dotnet test

# Run tests in specific project
dotnet test tests/MyApp.Tests/MyApp.Tests.csproj

# Run without build (faster if already built)
dotnet test --no-build

# Run without restore
dotnet test --no-restore
```

## Test Filtering

### By Name
```bash
# Filter by fully qualified name (contains)
dotnet test --filter "FullyQualifiedName~OrderService"

# Filter by test name (exact match)
dotnet test --filter "Name=CreateOrder_ValidInput_ReturnsOrder"

# Filter by display name
dotnet test --filter "DisplayName~Create Order"
```

### By Category/Trait
```bash
# Filter by trait (xUnit)
dotnet test --filter "Category=Unit"
dotnet test --filter "Category!=Integration"

# Multiple trait filters
dotnet test --filter "Category=Unit&Priority=High"
dotnet test --filter "Category=Unit|Category=Integration"
```

### By Class/Namespace
```bash
# Filter by class name
dotnet test --filter "ClassName=OrderServiceTests"

# Filter by namespace
dotnet test --filter "FullyQualifiedName~MyApp.Tests.Services"
```

### Complex Filters
```bash
# Combine with operators
# & (and), | (or), ! (not), ~ (contains), = (equals)

# Unit tests except slow ones
dotnet test --filter "Category=Unit&Category!=Slow"

# All tests in namespace containing "Order"
dotnet test --filter "FullyQualifiedName~Order&Category!=Integration"
```

## Test Output

### Verbosity Levels
```bash
# Quiet (minimal output)
dotnet test --verbosity quiet
dotnet test -v q

# Normal (default)
dotnet test --verbosity normal

# Detailed (shows all test names)
dotnet test --verbosity detailed
dotnet test -v d

# Diagnostic (maximum output)
dotnet test --verbosity diagnostic
```

### Logger Options
```bash
# Console logger with verbosity
dotnet test --logger "console;verbosity=detailed"

# TRX (Visual Studio Test Results)
dotnet test --logger trx

# JUnit format (for CI systems)
dotnet test --logger "junit;LogFileName=results.xml"

# HTML report
dotnet test --logger "html;LogFileName=results.html"

# Multiple loggers
dotnet test --logger trx --logger "console;verbosity=detailed"
```

### Results Directory
```bash
# Specify results output directory
dotnet test --results-directory ./TestResults
```

## Code Coverage

### Collect Coverage
```bash
# Basic coverage collection
dotnet test --collect:"XPlat Code Coverage"

# With Coverlet
dotnet test /p:CollectCoverage=true

# Coverlet with specific format
dotnet test /p:CollectCoverage=true /p:CoverletOutputFormat=cobertura

# Multiple formats
dotnet test /p:CollectCoverage=true /p:CoverletOutputFormat=\"opencover,cobertura\"
```

### Coverage Thresholds
```bash
# Fail if coverage below threshold
dotnet test /p:CollectCoverage=true /p:Threshold=80

# Per-type thresholds
dotnet test /p:CollectCoverage=true /p:ThresholdType=line /p:Threshold=80
```

### Coverage Reports
```bash
# Install report generator
dotnet tool install -g dotnet-reportgenerator-globaltool

# Generate HTML report
reportgenerator -reports:coverage.cobertura.xml -targetdir:coveragereport
```

## Parallel Execution

```bash
# Control parallelism
dotnet test --parallel

# Limit parallel workers
dotnet test -- RunConfiguration.MaxCpuCount=4

# Disable parallel execution
dotnet test -- RunConfiguration.DisableParallelization=true
```

## Test Timeouts

```bash
# Set test timeout (milliseconds)
dotnet test -- RunConfiguration.TestSessionTimeout=60000
```

```csharp
// Per-test timeout (xUnit)
[Fact(Timeout = 5000)]
public void SlowTest() { }

// Per-test timeout (NUnit)
[Test, Timeout(5000)]
public void SlowTest() { }
```

## Configuration Files

### runsettings
```xml
<!-- test.runsettings -->
<?xml version="1.0" encoding="utf-8"?>
<RunSettings>
  <RunConfiguration>
    <MaxCpuCount>4</MaxCpuCount>
    <ResultsDirectory>./TestResults</ResultsDirectory>
    <TestSessionTimeout>600000</TestSessionTimeout>
  </RunConfiguration>
  <DataCollectionRunSettings>
    <DataCollectors>
      <DataCollector friendlyName="XPlat Code Coverage">
        <Configuration>
          <Format>cobertura</Format>
          <Exclude>[*]*.Migrations.*</Exclude>
        </Configuration>
      </DataCollector>
    </DataCollectors>
  </DataCollectionRunSettings>
</RunSettings>
```

```bash
# Use runsettings file
dotnet test --settings test.runsettings
```

## Test Failure Analysis

### Common Failure Patterns

| Pattern | Cause | Fix |
|---------|-------|-----|
| Assert.Equal failed | Expected != Actual | Check logic, verify test data |
| NullReferenceException | Null not handled | Add null checks, verify setup |
| TimeoutException | Test too slow | Optimize or increase timeout |
| ObjectDisposedException | Using disposed object | Fix lifetime management |
| InvalidOperationException | Invalid state | Check test setup/order |

### Debugging Failed Tests
```bash
# Run single failing test with detailed output
dotnet test --filter "FullyQualifiedName~FailingTest" -v d

# Enable blame mode to catch hangs
dotnet test --blame

# Blame with hang detection
dotnet test --blame-hang --blame-hang-timeout 60s
```

## Watch Mode

```bash
# Run tests on file changes
dotnet watch test

# Watch specific project
dotnet watch --project tests/MyApp.Tests test

# Watch with filter
dotnet watch test --filter "Category=Unit"
```

## CI/CD Integration

### Exit Codes
| Code | Meaning |
|------|---------|
| 0 | All tests passed |
| 1 | Tests failed |
| 2 | Command line error |

### CI Examples
```bash
# Azure DevOps
- task: DotNetCoreCLI@2
  inputs:
    command: test
    arguments: '--configuration Release --logger trx'

# GitHub Actions
- run: dotnet test --configuration Release --logger "trx;LogFileName=test-results.trx"
```

See [test-filtering.md](test-filtering.md) for advanced filtering patterns.
