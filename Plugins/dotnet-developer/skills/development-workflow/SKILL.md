---
name: development-workflow
description: General .NET development workflow patterns. Use when implementing features, fixing bugs, or refactoring code.
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
---

# .NET Development Workflow

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    DEVELOPMENT WORKFLOW                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐                                               │
│  │  Understand  │  Read requirements, explore codebase          │
│  │    Task      │                                               │
│  └──────────────┘                                               │
│         │                                                       │
│         ▼                                                       │
│  ┌──────────────┐                                               │
│  │  Implement   │  Write code following patterns                │
│  │   Changes    │                                               │
│  └──────────────┘                                               │
│         │                                                       │
│         ▼                                                       │
│  ┌──────────────┐     ┌──────────────┐                         │
│  │   Validate   │────▶│   Report     │                         │
│  │ Build/Test/  │     │   Results    │                         │
│  │   Analyze    │     │              │                         │
│  └──────────────┘     └──────────────┘                         │
│         │                    │                                  │
│         ▼                    ▼                                  │
│    ┌─────────┐         ┌──────────┐                            │
│    │  PASS?  │───NO───▶│   Fix    │                            │
│    └─────────┘         │  Issues  │                            │
│         │              └──────────┘                            │
│         │                    │                                  │
│        YES                   │                                  │
│         │                    │                                  │
│         ▼                    │                                  │
│  ┌──────────────┐           │                                  │
│  │   Ready to   │◀──────────┘                                  │
│  │    Commit    │         (re-validate)                        │
│  └──────────────┘                                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Phase 1: Understand the Task

### Feature Implementation
1. Read the feature requirements/user story
2. Identify affected components
3. Check existing patterns in codebase
4. Plan the implementation approach

### Bug Fix
1. Reproduce the bug
2. Identify root cause
3. Find related code
4. Plan the fix

### Refactoring
1. Understand current implementation
2. Identify what needs to change
3. Ensure test coverage exists
4. Plan incremental changes

## Phase 2: Implement Changes

### Follow Existing Patterns
```csharp
// Find existing patterns
// Look for similar implementations in the codebase
// Follow established conventions

// Example: If services follow this pattern
public class ExistingService : IExistingService
{
    private readonly IRepository _repository;
    private readonly ILogger<ExistingService> _logger;

    public ExistingService(IRepository repository, ILogger<ExistingService> logger)
    {
        _repository = repository;
        _logger = logger;
    }
}

// New service should follow same pattern
public class NewService : INewService
{
    private readonly IRepository _repository;
    private readonly ILogger<NewService> _logger;

    public NewService(IRepository repository, ILogger<NewService> logger)
    {
        _repository = repository;
        _logger = logger;
    }
}
```

### Make Small, Incremental Changes
1. One logical change at a time
2. Build after each change to catch errors early
3. Run relevant tests frequently
4. Keep commits focused

## Phase 3: Validate Changes

### Validation Steps
```bash
# 1. Build (catch compilation errors)
dotnet build --no-incremental

# 2. Run tests (verify behavior)
dotnet test --no-build

# 3. Static analysis (code quality)
dotnet build /p:TreatWarningsAsErrors=true
dotnet format --verify-no-changes
```

### Quality Gates
| Gate | Requirement | Blocking |
|------|-------------|----------|
| Build | 0 errors | Yes |
| Tests | 100% pass | Yes |
| Critical Warnings | 0 | No |
| All Warnings | < 10 | No |

## Phase 4: Fix Issues

### Build Errors
1. Read error message carefully
2. Go to the file and line indicated
3. Fix the issue
4. Rebuild to verify

### Test Failures
1. Read the assertion failure
2. Check expected vs actual
3. Determine if test or code is wrong
4. Fix and re-run test

### Analysis Warnings
1. Review each warning
2. Apply fix or suppress with justification
3. Use `dotnet format` for auto-fixable issues

## Validation Before Commit

### Checklist
- [ ] `dotnet build` succeeds with no errors
- [ ] `dotnet test` passes all tests
- [ ] No new critical analyzer warnings
- [ ] Code follows existing patterns
- [ ] Changes are focused on the task

### Commands
```bash
# Full validation
dotnet build --no-incremental && \
dotnet test --no-build && \
dotnet format --verify-no-changes
```

## Best Practices

### Code Organization
```csharp
// Group related code
// 1. Fields
private readonly IService _service;

// 2. Constructors
public MyClass(IService service) => _service = service;

// 3. Public methods
public void Execute() { }

// 4. Private methods
private void Helper() { }
```

### Error Handling
```csharp
// Be specific with exceptions
public User GetUser(int id)
{
    var user = _repository.Find(id);
    if (user == null)
        throw new EntityNotFoundException($"User {id} not found");
    return user;
}

// Use guard clauses
public void Process(Request request)
{
    ArgumentNullException.ThrowIfNull(request);
    ArgumentException.ThrowIfNullOrEmpty(request.Name);

    // Main logic
}
```

### Async/Await
```csharp
// Always use async suffix
public async Task<User> GetUserAsync(int id)
{
    return await _repository.FindAsync(id);
}

// Don't block on async
// BAD
var user = GetUserAsync(id).Result;

// GOOD
var user = await GetUserAsync(id);
```

### Dependency Injection
```csharp
// Register services
services.AddScoped<IUserService, UserService>();
services.AddSingleton<ICacheService, MemoryCacheService>();
services.AddTransient<IEmailSender, SmtpEmailSender>();

// Inject via constructor
public class UserController
{
    private readonly IUserService _userService;

    public UserController(IUserService userService)
    {
        _userService = userService;
    }
}
```

## Common Patterns

See [patterns.md](patterns.md) for detailed implementation patterns.
