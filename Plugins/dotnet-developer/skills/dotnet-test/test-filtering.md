# Advanced Test Filtering

## Filter Syntax

### Operators
| Operator | Meaning | Example |
|----------|---------|---------|
| `=` | Exact match | `Name=TestMethod` |
| `!=` | Not equal | `Category!=Integration` |
| `~` | Contains | `FullyQualifiedName~Service` |
| `!~` | Not contains | `FullyQualifiedName!~Slow` |
| `&` | AND | `Category=Unit&Priority=1` |
| `\|` | OR | `Category=Unit\|Category=Fast` |
| `!` | NOT | `!Category=Integration` |
| `()` | Grouping | `(Category=Unit\|Category=Fast)&!Slow` |

### Properties
| Property | Description | Example |
|----------|-------------|---------|
| `FullyQualifiedName` | Full test name with namespace | `Namespace.Class.Method` |
| `Name` | Method name only | `CreateOrder_Valid_Returns` |
| `ClassName` | Test class name | `OrderServiceTests` |
| `DisplayName` | Human-readable name | `"Create Order Test"` |
| `Category` | xUnit Trait Category | `Unit`, `Integration` |
| `Priority` | Test priority trait | `1`, `2`, `3` |

## xUnit Traits

### Defining Traits
```csharp
public class OrderServiceTests
{
    [Fact]
    [Trait("Category", "Unit")]
    [Trait("Priority", "1")]
    public void CreateOrder_Valid_ReturnsOrder() { }

    [Fact]
    [Trait("Category", "Integration")]
    [Trait("Feature", "Orders")]
    public void CreateOrder_PersistsToDatabase() { }
}
```

### Custom Trait Attributes
```csharp
// Create reusable trait attribute
public class UnitTestAttribute : FactAttribute
{
    public UnitTestAttribute()
    {
        DisplayName = "Unit Test";
    }
}

[AttributeUsage(AttributeTargets.Method)]
public class CategoryAttribute : Attribute, ITraitAttribute
{
    public CategoryAttribute(string category) { }
}

// Usage
[UnitTest]
[Category("Orders")]
public void MyTest() { }
```

## NUnit Categories

### Defining Categories
```csharp
[TestFixture]
public class OrderServiceTests
{
    [Test]
    [Category("Unit")]
    public void CreateOrder_Valid_ReturnsOrder() { }

    [Test]
    [Category("Integration")]
    [Category("Database")]
    public void CreateOrder_PersistsToDatabase() { }
}
```

### Filter NUnit Tests
```bash
# Single category
dotnet test --filter "TestCategory=Unit"

# Exclude category
dotnet test --filter "TestCategory!=Integration"
```

## MSTest Categories

### Defining Categories
```csharp
[TestClass]
public class OrderServiceTests
{
    [TestMethod]
    [TestCategory("Unit")]
    public void CreateOrder_Valid_ReturnsOrder() { }

    [TestMethod]
    [TestCategory("Integration")]
    [Priority(1)]
    public void CreateOrder_PersistsToDatabase() { }
}
```

### Filter MSTest
```bash
# Category filter
dotnet test --filter "TestCategory=Unit"

# Priority filter
dotnet test --filter "Priority=1"
```

## Common Filter Patterns

### Development Workflow
```bash
# Run only unit tests (fast feedback)
dotnet test --filter "Category=Unit"

# Run smoke tests
dotnet test --filter "Category=Smoke"

# Run everything except slow tests
dotnet test --filter "Category!=Slow"
```

### Feature-Based
```bash
# Run tests for specific feature
dotnet test --filter "FullyQualifiedName~Orders"

# Run tests for multiple features
dotnet test --filter "FullyQualifiedName~Orders|FullyQualifiedName~Payments"
```

### CI Pipeline Stages
```bash
# Stage 1: Fast unit tests
dotnet test --filter "Category=Unit" --parallel

# Stage 2: Integration tests
dotnet test --filter "Category=Integration"

# Stage 3: E2E tests
dotnet test --filter "Category=E2E" -- RunConfiguration.DisableParallelization=true
```

### Class-Based
```bash
# Run all tests in specific class
dotnet test --filter "ClassName=OrderServiceTests"

# Run tests in multiple classes
dotnet test --filter "ClassName=OrderServiceTests|ClassName=PaymentServiceTests"
```

### Excluding Tests
```bash
# Exclude integration tests
dotnet test --filter "Category!=Integration"

# Exclude multiple categories
dotnet test --filter "Category!=Integration&Category!=E2E"

# Exclude by namespace
dotnet test --filter "FullyQualifiedName!~Integration"
```

## Project-Level Filtering

### xunit.runner.json
```json
{
  "$schema": "https://xunit.net/schema/current/xunit.runner.schema.json",
  "parallelizeAssembly": false,
  "parallelizeTestCollections": true,
  "maxParallelThreads": 4
}
```

### .runsettings Filter
```xml
<RunSettings>
  <RunConfiguration>
    <TestCaseFilter>Category=Unit</TestCaseFilter>
  </RunConfiguration>
</RunSettings>
```

## Complex Filter Examples

```bash
# Unit tests for Orders feature, excluding slow ones
dotnet test --filter "(Category=Unit&FullyQualifiedName~Orders)&Category!=Slow"

# High priority tests across multiple categories
dotnet test --filter "Priority=1&(Category=Unit|Category=Integration)"

# Specific namespace, specific category
dotnet test --filter "FullyQualifiedName~MyApp.Tests.Services&Category=Unit"

# Everything except database tests in CI
dotnet test --filter "Category!=Database&Category!=E2E"
```

## Tips

1. **Quote filters with special characters**
   ```bash
   dotnet test --filter "FullyQualifiedName~MyApp.Tests"
   ```

2. **Escape pipe on Unix**
   ```bash
   dotnet test --filter "Category=Unit\|Category=Fast"
   ```

3. **Use contains (~) over equals (=) for flexibility**
   ```bash
   dotnet test --filter "FullyQualifiedName~Service"  # More flexible
   ```

4. **Combine with verbosity for debugging filters**
   ```bash
   dotnet test --filter "Category=Unit" -v d  # See which tests match
   ```
