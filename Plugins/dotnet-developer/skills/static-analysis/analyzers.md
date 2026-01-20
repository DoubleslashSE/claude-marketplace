# .NET Analyzer Reference

## Microsoft.CodeAnalysis.NetAnalyzers

Built into .NET SDK. Configure in project:

```xml
<PropertyGroup>
  <EnableNETAnalyzers>true</EnableNETAnalyzers>
  <AnalysisLevel>latest-all</AnalysisLevel>
</PropertyGroup>
```

### Key Rules

#### Design (CA1xxx)
| Rule | Description | Severity |
|------|-------------|----------|
| CA1002 | Don't expose generic lists | Warning |
| CA1014 | Mark assemblies with CLSCompliant | Info |
| CA1024 | Use properties where appropriate | Info |
| CA1031 | Don't catch general exceptions | Warning |
| CA1032 | Implement standard exception constructors | Warning |
| CA1040 | Avoid empty interfaces | Warning |
| CA1051 | Don't declare visible instance fields | Warning |
| CA1062 | Validate arguments of public methods | Warning |

#### Performance (CA18xx)
| Rule | Description | Severity |
|------|-------------|----------|
| CA1802 | Use literals where appropriate | Info |
| CA1805 | Don't initialize unnecessarily | Info |
| CA1812 | Avoid uninstantiated internal classes | Warning |
| CA1822 | Mark members as static | Info |
| CA1825 | Avoid zero-length array allocations | Info |
| CA1827 | Don't use Count/Length when Any | Warning |
| CA1829 | Use Length/Count property | Warning |
| CA1836 | Prefer IsEmpty over Count | Info |

#### Security (CA2xxx, CA3xxx, CA5xxx)
| Rule | Description | Severity |
|------|-------------|----------|
| CA2100 | Review SQL queries for vulnerabilities | Warning |
| CA2119 | Seal methods that satisfy private interfaces | Warning |
| CA2200 | Rethrow to preserve stack details | Warning |
| CA2213 | Disposable fields should be disposed | Warning |
| CA3001 | Review code for SQL injection | Warning |
| CA3003 | Review code for file path injection | Warning |
| CA5350 | Don't use weak crypto algorithms | Warning |
| CA5351 | Don't use broken crypto algorithms | Error |

#### Reliability (CA2xxx)
| Rule | Description | Severity |
|------|-------------|----------|
| CA2000 | Dispose objects before losing scope | Warning |
| CA2007 | Consider calling ConfigureAwait | Warning |
| CA2008 | Don't create tasks without passing TaskScheduler | Warning |
| CA2012 | Use ValueTasks correctly | Warning |
| CA2016 | Forward CancellationToken | Info |

## StyleCop.Analyzers

```bash
dotnet add package StyleCop.Analyzers --version 1.2.0-beta.556
```

### Configuration (stylecop.json)
```json
{
  "$schema": "https://raw.githubusercontent.com/DotNetAnalyzers/StyleCopAnalyzers/master/StyleCop.Analyzers/StyleCop.Analyzers/Settings/stylecop.schema.json",
  "settings": {
    "documentationRules": {
      "companyName": "MyCompany",
      "documentInterfaces": true,
      "documentExposedElements": true,
      "documentInternalElements": false
    },
    "orderingRules": {
      "usingDirectivesPlacement": "outsideNamespace"
    },
    "namingRules": {
      "allowCommonHungarianPrefixes": false
    }
  }
}
```

### Key Rules

#### Documentation (SA16xx)
| Rule | Description | Default |
|------|-------------|---------|
| SA1600 | Elements should be documented | Warning |
| SA1601 | Partial elements should be documented | Warning |
| SA1633 | File should have header | Warning |

#### Layout (SA15xx)
| Rule | Description | Default |
|------|-------------|---------|
| SA1500 | Braces should not be omitted | Warning |
| SA1501 | Statement should not be on single line | Warning |
| SA1502 | Element should not be on single line | Warning |

#### Ordering (SA12xx)
| Rule | Description | Default |
|------|-------------|---------|
| SA1200 | Using directives placement | Warning |
| SA1201 | Element order | Warning |
| SA1202 | Element order by access | Warning |

#### Naming (SA13xx)
| Rule | Description | Default |
|------|-------------|---------|
| SA1300 | Element should begin with upper case | Warning |
| SA1302 | Interface names should begin with I | Warning |
| SA1309 | Field names should not begin with underscore | Warning |

### Common Overrides (.editorconfig)
```ini
# Disable file headers
dotnet_diagnostic.SA1633.severity = none

# Allow underscore prefix for private fields
dotnet_diagnostic.SA1309.severity = none

# Allow using inside namespace
dotnet_diagnostic.SA1200.severity = none

# Don't require this. prefix
dotnet_diagnostic.SA1101.severity = none
```

## Roslynator

```bash
dotnet add package Roslynator.Analyzers
dotnet add package Roslynator.Formatting.Analyzers
dotnet add package Roslynator.CodeAnalysis.Analyzers
```

### Key Rules

#### Code Analysis (RCS1xxx)
| Rule | Description |
|------|-------------|
| RCS1001 | Add braces |
| RCS1003 | Add braces to if-else |
| RCS1018 | Add accessibility modifiers |
| RCS1036 | Remove redundant empty line |
| RCS1037 | Remove trailing whitespace |
| RCS1038 | Remove empty statement |
| RCS1049 | Simplify boolean comparison |
| RCS1058 | Use compound assignment |
| RCS1061 | Merge if statement with nested if |
| RCS1073 | Convert if to return statement |
| RCS1077 | Optimize LINQ method call |
| RCS1085 | Use auto-implemented property |
| RCS1118 | Mark local variable as const |
| RCS1123 | Add parentheses when necessary |
| RCS1138 | Add summary to documentation |
| RCS1139 | Add summary element to documentation |
| RCS1140 | Add exception to documentation |
| RCS1146 | Use conditional access |
| RCS1155 | Use StringComparison |
| RCS1163 | Unused parameter |
| RCS1168 | Parameter name differs |
| RCS1169 | Make field read-only |
| RCS1170 | Use read-only auto-implemented property |
| RCS1175 | Unused this parameter |
| RCS1181 | Convert comment to documentation comment |
| RCS1192 | Unnecessary usage of verbatim string literal |
| RCS1197 | Optimize StringBuilder.Append/AppendLine |
| RCS1202 | Avoid NullReferenceException |
| RCS1206 | Use conditional access instead of conditional expression |
| RCS1214 | Unnecessary interpolated string |
| RCS1220 | Use pattern matching instead of combination of 'is' and cast |
| RCS1225 | Make class sealed |
| RCS1229 | Use async/await when necessary |
| RCS1236 | Use exception filter |
| RCS1241 | Implement non-generic counterpart |
| RCS1246 | Use element access |

## SonarAnalyzer.CSharp

```bash
dotnet add package SonarAnalyzer.CSharp
```

### Key Security Rules

| Rule | Description |
|------|-------------|
| S2068 | Credentials should not be hard-coded |
| S2077 | SQL queries should be parameterized |
| S2078 | LDAP queries should be parameterized |
| S2092 | Cookies should be secure |
| S3330 | Cookies should be "HttpOnly" |
| S5042 | Expanding archive files is security sensitive |
| S5122 | CORS allows all domains |
| S5131 | XSS vulnerabilities |

## Recommended Configuration

### Minimal (Start Here)
```xml
<PropertyGroup>
  <EnableNETAnalyzers>true</EnableNETAnalyzers>
  <AnalysisLevel>latest-recommended</AnalysisLevel>
</PropertyGroup>
```

### Comprehensive
```xml
<PropertyGroup>
  <EnableNETAnalyzers>true</EnableNETAnalyzers>
  <AnalysisLevel>latest-all</AnalysisLevel>
  <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
</PropertyGroup>

<ItemGroup>
  <PackageReference Include="StyleCop.Analyzers" Version="1.2.0-beta.556" PrivateAssets="all" />
  <PackageReference Include="Roslynator.Analyzers" Version="4.6.0" PrivateAssets="all" />
</ItemGroup>
```

### .editorconfig Base
```ini
root = true

[*.cs]
# Core rules
dotnet_diagnostic.CA1062.severity = warning
dotnet_diagnostic.CA2000.severity = warning
dotnet_diagnostic.CA2007.severity = none  # Not needed in apps
dotnet_diagnostic.CA1822.severity = suggestion

# StyleCop overrides
dotnet_diagnostic.SA1101.severity = none  # No this. prefix required
dotnet_diagnostic.SA1200.severity = none  # Using placement flexible
dotnet_diagnostic.SA1309.severity = none  # Allow _privateField
dotnet_diagnostic.SA1633.severity = none  # No file headers required
```
