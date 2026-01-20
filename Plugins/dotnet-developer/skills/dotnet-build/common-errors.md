# Common .NET Build Errors and Fixes

## CS0103: The name 'X' does not exist in the current context

**Cause**: Variable, method, or type not declared or not in scope.

**Fixes**:
```csharp
// 1. Check spelling
var customer = GetCustomer();  // Not 'Customer'

// 2. Add using statement
using System.Linq;  // For LINQ methods

// 3. Check scope
if (true)
{
    var x = 1;
}
Console.WriteLine(x);  // Error: x out of scope

// 4. Qualify with namespace
System.Console.WriteLine("Hello");
```

## CS0246: The type or namespace 'X' could not be found

**Cause**: Missing reference or using statement.

**Fixes**:
```bash
# 1. Add package reference
dotnet add package Newtonsoft.Json
```

```csharp
// 2. Add using statement
using Newtonsoft.Json;

// 3. Check target framework compatibility
// Ensure package supports your framework version
```

```xml
<!-- 4. Add project reference -->
<ItemGroup>
  <ProjectReference Include="..\Domain\Domain.csproj" />
</ItemGroup>
```

## CS1061: 'Type' does not contain a definition for 'X'

**Cause**: Method or property doesn't exist on type.

**Fixes**:
```csharp
// 1. Check type is correct
IEnumerable<int> numbers = GetNumbers();
numbers.Count();  // Error: IEnumerable has no Count()
numbers.Count();  // Fix: Use LINQ Count() method with using System.Linq

// 2. Check interface implementation
public interface IService
{
    void Execute();  // Add missing method
}

// 3. Cast to correct type
var obj = GetObject();
((ISpecificType)obj).SpecificMethod();
```

## CS0029: Cannot implicitly convert type 'X' to 'Y'

**Cause**: Type mismatch in assignment or return.

**Fixes**:
```csharp
// 1. Explicit cast
object obj = GetObject();
string str = (string)obj;

// 2. Use conversion method
int number = int.Parse("123");
string text = number.ToString();

// 3. Fix return type
public string GetValue()  // Not 'int'
{
    return "value";
}

// 4. Use 'as' for safe cast
var specific = obj as SpecificType;
if (specific != null) { }
```

## CS0120: An object reference is required for non-static member

**Cause**: Accessing instance member from static context.

**Fixes**:
```csharp
// 1. Make member static
public static void DoSomething() { }

// 2. Create instance
var instance = new MyClass();
instance.DoSomething();

// 3. Access through instance in static method
public static void StaticMethod()
{
    var instance = new MyClass();
    instance.InstanceMethod();
}
```

## CS0234: The type or namespace 'X' does not exist in 'Y'

**Cause**: Namespace exists but type doesn't.

**Fixes**:
```csharp
// 1. Check exact namespace
using System.Collections.Generic;  // Not System.Collections

// 2. Check assembly reference
// Ensure correct package is referenced

// 3. Check .NET version
// Some types moved in .NET Core/5+
```

## CS0019: Operator 'X' cannot be applied to operands of type 'Y' and 'Z'

**Cause**: Invalid operator usage between types.

**Fixes**:
```csharp
// 1. Convert types
string a = "5";
int b = 3;
int result = int.Parse(a) + b;  // Convert string to int

// 2. Use correct comparison
object obj = GetObject();
if (obj?.Equals(other) == true)  // Not == for objects

// 3. Implement operator
public static MyType operator +(MyType a, MyType b)
{
    return new MyType(a.Value + b.Value);
}
```

## CS0161: Not all code paths return a value

**Cause**: Method missing return statement in some branches.

**Fixes**:
```csharp
// BAD
public int GetValue(bool condition)
{
    if (condition)
        return 1;
    // Missing return
}

// GOOD
public int GetValue(bool condition)
{
    if (condition)
        return 1;
    return 0;  // Default return
}

// OR use expression
public int GetValue(bool condition) => condition ? 1 : 0;
```

## CS0535: Class does not implement interface member

**Cause**: Interface method not implemented.

**Fixes**:
```csharp
public interface IService
{
    void Execute();
    Task<int> GetValueAsync();
}

public class Service : IService
{
    // Implement all members
    public void Execute() { }

    public Task<int> GetValueAsync()
    {
        return Task.FromResult(0);
    }
}
```

## MSB3202: The project file 'X' was not found

**Cause**: ProjectReference path is incorrect.

**Fixes**:
```xml
<!-- Check relative path -->
<ItemGroup>
  <!-- Verify path exists -->
  <ProjectReference Include="..\Domain\Domain.csproj" />
</ItemGroup>
```

```bash
# Verify file exists
ls ../Domain/Domain.csproj
```

## NU1101: Unable to find package 'X'

**Cause**: Package doesn't exist or source not configured.

**Fixes**:
```bash
# 1. Check package name spelling
dotnet add package Newtonsoft.Json  # Not NewtonsoftJson

# 2. Add package source
dotnet nuget add source https://api.nuget.org/v3/index.json

# 3. Check nuget.config
```

```xml
<!-- nuget.config -->
<configuration>
  <packageSources>
    <add key="nuget.org" value="https://api.nuget.org/v3/index.json" />
  </packageSources>
</configuration>
```

## NU1605: Detected package downgrade

**Cause**: Dependency version conflict.

**Fixes**:
```xml
<!-- 1. Set explicit version -->
<ItemGroup>
  <PackageReference Include="Microsoft.Extensions.Logging" Version="8.0.0" />
</ItemGroup>

<!-- 2. Use Directory.Packages.props for central management -->
<Project>
  <PropertyGroup>
    <ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally>
  </PropertyGroup>
  <ItemGroup>
    <PackageVersion Include="Microsoft.Extensions.Logging" Version="8.0.0" />
  </ItemGroup>
</Project>
```

## General Troubleshooting

```bash
# Clear all caches
dotnet nuget locals all --clear

# Force restore
dotnet restore --force

# Clean and rebuild
dotnet clean && dotnet build

# Check SDK version
dotnet --version

# List installed workloads
dotnet workload list
```
