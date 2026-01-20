---
name: dotnet-build
description: .NET build configuration and error handling. Use when building projects, diagnosing build errors, or configuring build options.
allowed-tools: Read, Grep, Glob, Bash
---

# .NET Build Configuration

## Build Commands

### Basic Build
```bash
# Build solution/project
dotnet build

# Build specific project
dotnet build src/MyApp/MyApp.csproj

# Build with configuration
dotnet build --configuration Release
dotnet build -c Debug

# Clean build (no incremental)
dotnet build --no-incremental

# Build without restoring packages
dotnet build --no-restore
```

### Build Output
```bash
# Specify output directory
dotnet build --output ./artifacts

# Build for specific runtime
dotnet build --runtime win-x64
dotnet build --runtime linux-x64

# Build framework-specific
dotnet build --framework net8.0
```

## Build Configurations

### Debug vs Release
```xml
<!-- Default configurations in .csproj -->
<PropertyGroup Condition="'$(Configuration)' == 'Debug'">
  <DefineConstants>DEBUG;TRACE</DefineConstants>
  <Optimize>false</Optimize>
  <DebugType>full</DebugType>
</PropertyGroup>

<PropertyGroup Condition="'$(Configuration)' == 'Release'">
  <DefineConstants>TRACE</DefineConstants>
  <Optimize>true</Optimize>
  <DebugType>pdbonly</DebugType>
</PropertyGroup>
```

### Warnings as Errors
```xml
<!-- Treat all warnings as errors -->
<PropertyGroup>
  <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
</PropertyGroup>

<!-- Treat specific warnings as errors -->
<PropertyGroup>
  <WarningsAsErrors>CS0168;CS0219</WarningsAsErrors>
</PropertyGroup>

<!-- Suppress specific warnings -->
<PropertyGroup>
  <NoWarn>$(NoWarn);CS1591</NoWarn>
</PropertyGroup>
```

## Multi-Project Solutions

### Solution Build
```bash
# Build entire solution
dotnet build MySolution.sln

# Build specific projects from solution
dotnet build MySolution.sln --project src/Api

# Parallel build (default)
dotnet build --maxcpucount

# Sequential build
dotnet build --maxcpucount:1
```

### Project Dependencies
```xml
<!-- ProjectReference in .csproj -->
<ItemGroup>
  <ProjectReference Include="..\Domain\Domain.csproj" />
  <ProjectReference Include="..\Infrastructure\Infrastructure.csproj" />
</ItemGroup>
```

## Build Error Categories

### Compilation Errors (CS)
| Code | Description | Common Fix |
|------|-------------|------------|
| CS0103 | Name does not exist | Check spelling, add using statement |
| CS0246 | Type/namespace not found | Add package reference, add using |
| CS1061 | Member does not exist | Check type, update interface |
| CS0029 | Cannot convert type | Add cast, fix type mismatch |
| CS0120 | Object reference required | Make static or instantiate |

### Project Errors (MSB)
| Code | Description | Common Fix |
|------|-------------|------------|
| MSB3202 | Project file not found | Fix path in ProjectReference |
| MSB4019 | Target file not found | Restore packages |
| MSB3644 | Framework not installed | Install SDK |
| MSB3245 | Reference not resolved | Restore packages, check path |

### NuGet Errors (NU)
| Code | Description | Common Fix |
|------|-------------|------------|
| NU1101 | Package not found | Check package name/source |
| NU1103 | Version not found | Check available versions |
| NU1202 | Incompatible framework | Update package or framework |
| NU1605 | Downgrade detected | Resolve version conflicts |

## Package Restoration

```bash
# Restore packages
dotnet restore

# Restore with specific source
dotnet restore --source https://api.nuget.org/v3/index.json

# Clear NuGet cache
dotnet nuget locals all --clear

# List packages
dotnet list package
dotnet list package --outdated
```

## Build Diagnostics

### Verbose Output
```bash
# Detailed build output
dotnet build --verbosity detailed
dotnet build -v d

# Diagnostic output (most verbose)
dotnet build --verbosity diagnostic

# Minimal output
dotnet build --verbosity quiet
```

### Binary Log
```bash
# Generate binary log for analysis
dotnet build -bl

# View with MSBuild Structured Log Viewer
# Download from: https://msbuildlog.com/
```

## Clean Operations

```bash
# Clean build artifacts
dotnet clean

# Clean specific configuration
dotnet clean --configuration Release

# Force clean (delete bin/obj manually)
rm -rf **/bin **/obj
```

## Common Build Issues

### Framework Mismatch
```xml
<!-- Ensure consistent framework across projects -->
<PropertyGroup>
  <TargetFramework>net8.0</TargetFramework>
</PropertyGroup>
```

### Missing SDK
```bash
# Check installed SDKs
dotnet --list-sdks

# Install specific version via global.json
{
  "sdk": {
    "version": "8.0.100"
  }
}
```

### Locked Files
```bash
# Kill processes holding files (Windows)
taskkill /F /IM dotnet.exe

# Kill processes (Linux/Mac)
pkill dotnet
```

See [common-errors.md](common-errors.md) for detailed error resolutions.
