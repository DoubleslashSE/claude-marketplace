---
name: static-analysis
description: .NET static analysis and code quality tools. Use when configuring analyzers, fixing warnings, or enforcing code standards.
allowed-tools: Read, Grep, Glob, Bash
---

# .NET Static Analysis

## Built-in Analyzers

### .NET Analyzers
.NET SDK includes analyzers for code quality and style. Enable in project file:

```xml
<PropertyGroup>
  <!-- Enable all .NET analyzers -->
  <EnableNETAnalyzers>true</EnableNETAnalyzers>

  <!-- Analysis level (latest, 8.0, 7.0, etc.) -->
  <AnalysisLevel>latest</AnalysisLevel>

  <!-- Analysis mode: Default, Minimum, Recommended, All -->
  <AnalysisMode>Recommended</AnalysisMode>
</PropertyGroup>
```

### Analysis Categories
| Category | Prefix | Focus |
|----------|--------|-------|
| Design | CA1xxx | API design guidelines |
| Globalization | CA2xxx | Internationalization |
| Performance | CA18xx | Performance optimizations |
| Security | CA2xxx, CA3xxx | Security vulnerabilities |
| Usage | CA2xxx | Correct API usage |
| Naming | CA17xx | Naming conventions |
| Reliability | CA2xxx | Error handling, resources |

## Running Analysis

### With Build
```bash
# Build with analyzers (default)
dotnet build

# Ensure analyzers run
dotnet build /p:RunAnalyzersDuringBuild=true

# Treat warnings as errors
dotnet build /p:TreatWarningsAsErrors=true

# Run only analyzers (no compile)
dotnet build /p:RunAnalyzers=true /p:RunCodeAnalysis=true
```

### As Separate Step
```bash
# Format check (style only)
dotnet format --verify-no-changes

# Format and fix
dotnet format

# Analyze specific project
dotnet build src/MyApp/MyApp.csproj /p:TreatWarningsAsErrors=true
```

## Configuring Rules

### EditorConfig
```ini
# .editorconfig
root = true

[*.cs]
# Naming conventions
dotnet_naming_rule.private_fields_should_be_camel_case.severity = warning
dotnet_naming_rule.private_fields_should_be_camel_case.symbols = private_fields
dotnet_naming_rule.private_fields_should_be_camel_case.style = camel_case_style

dotnet_naming_symbols.private_fields.applicable_kinds = field
dotnet_naming_symbols.private_fields.applicable_accessibilities = private

dotnet_naming_style.camel_case_style.capitalization = camel_case
dotnet_naming_style.camel_case_style.required_prefix = _

# Code style
csharp_style_var_for_built_in_types = true:suggestion
csharp_style_expression_bodied_methods = when_on_single_line:suggestion
csharp_prefer_braces = true:warning

# Analyzer rules
dotnet_diagnostic.CA1062.severity = warning  # Validate arguments
dotnet_diagnostic.CA2007.severity = none     # Don't require ConfigureAwait
dotnet_diagnostic.IDE0044.severity = warning # Make field readonly
```

### GlobalAnalyzerConfig
```ini
# .globalconfig
is_global = true

# Apply to all projects
dotnet_diagnostic.CA1062.severity = warning
dotnet_diagnostic.CA2000.severity = error
```

### Project-Level
```xml
<PropertyGroup>
  <!-- Suppress in entire project -->
  <NoWarn>$(NoWarn);CA1062;CA2007</NoWarn>

  <!-- Treat specific as error -->
  <WarningsAsErrors>$(WarningsAsErrors);CA2000</WarningsAsErrors>
</PropertyGroup>
```

## Suppressing Warnings

### Code-Level Suppression
```csharp
// Suppress on member
[SuppressMessage("Design", "CA1062:Validate arguments",
    Justification = "Validated by framework")]
public void Process(Request request) { }

// Suppress on line
#pragma warning disable CA1062
public void Process(Request request) { }
#pragma warning restore CA1062

// Suppress all in file
[assembly: SuppressMessage("Design", "CA1062")]
```

### Global Suppressions
```csharp
// GlobalSuppressions.cs
using System.Diagnostics.CodeAnalysis;

[assembly: SuppressMessage("Design", "CA1062",
    Scope = "namespaceanddescendants",
    Target = "~N:MyApp.Controllers")]
```

## Common Analyzer Rules

### CA1062 - Validate Arguments
```csharp
// Warning: parameter 'request' is never validated
public void Process(Request request)
{
    request.Execute();  // CA1062
}

// Fixed
public void Process(Request request)
{
    ArgumentNullException.ThrowIfNull(request);
    request.Execute();
}
```

### CA2007 - ConfigureAwait
```csharp
// Warning in library code
await SomeAsync();  // CA2007

// Fixed
await SomeAsync().ConfigureAwait(false);

// Or suppress in application code (.editorconfig)
dotnet_diagnostic.CA2007.severity = none
```

### CA1822 - Mark Members Static
```csharp
// Warning: can be static
public int Calculate(int x) => x * 2;  // CA1822

// Fixed
public static int Calculate(int x) => x * 2;
```

### IDE0044 - Make Field Readonly
```csharp
// Warning
private int _value;  // IDE0044

// Fixed
private readonly int _value;
```

### CA2000 - Dispose Objects
```csharp
// Warning: not disposed
public void Process()
{
    var stream = new FileStream("file.txt", FileMode.Open);
}  // CA2000

// Fixed
public void Process()
{
    using var stream = new FileStream("file.txt", FileMode.Open);
}
```

## dotnet format

### Check Formatting
```bash
# Check without changes
dotnet format --verify-no-changes

# Check specific files
dotnet format --include "src/**/*.cs" --verify-no-changes

# Exclude paths
dotnet format --exclude "**/Migrations/**"
```

### Apply Fixes
```bash
# Fix all issues
dotnet format

# Fix style issues only
dotnet format style

# Fix analyzers only
dotnet format analyzers

# Fix specific severity
dotnet format --severity warn
```

### Targeting
```bash
# Whitespace only
dotnet format whitespace

# Style and analyzers
dotnet format style
dotnet format analyzers

# Specific diagnostics
dotnet format --diagnostics CA1062 IDE0044
```

## Third-Party Analyzers

### StyleCop.Analyzers
```bash
dotnet add package StyleCop.Analyzers
```

```ini
# .editorconfig
# Configure StyleCop rules
dotnet_diagnostic.SA1101.severity = none  # Prefix local calls with this
dotnet_diagnostic.SA1200.severity = none  # Using directives placement
dotnet_diagnostic.SA1633.severity = none  # File header
```

### Roslynator
```bash
dotnet add package Roslynator.Analyzers
```

### SonarAnalyzer
```bash
dotnet add package SonarAnalyzer.CSharp
```

## CI Integration

### Quality Gate Script
```bash
#!/bin/bash
# Run build with analysis
dotnet build --no-restore /p:TreatWarningsAsErrors=true

# Check format
dotnet format --verify-no-changes

# Exit with error if any issues
exit $?
```

### Azure DevOps
```yaml
- task: DotNetCoreCLI@2
  displayName: 'Build with Analysis'
  inputs:
    command: build
    arguments: '/p:TreatWarningsAsErrors=true'
```

See [analyzers.md](analyzers.md) for detailed analyzer configurations.
