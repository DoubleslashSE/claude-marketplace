# XML Task Format Reference

## Complete Task Schema

```xml
<task id="TASK-XXX" status="pending|in_progress|completed|blocked|skipped">
  <!-- Required: Short, descriptive name (5-10 words) -->
  <name>Implement user authentication service</name>

  <!-- Required: What this task accomplishes (1-2 sentences) -->
  <description>
    Create the core authentication service with login and logout methods,
    integrated with the existing user repository.
  </description>

  <!-- Optional: Task IDs this depends on (comma-separated) -->
  <depends>TASK-001, TASK-002</depends>

  <!-- Required: Files this task will create or modify -->
  <files>
    <file action="create">src/services/AuthService.ts</file>
    <file action="modify">src/config/services.ts</file>
    <file action="delete">src/legacy/OldAuth.ts</file>
  </files>

  <!-- Required: Specific actions to take (2-5 typically) -->
  <actions>
    <action>Create AuthService class with login() and logout() methods</action>
    <action>Inject UserRepository dependency via constructor</action>
    <action>Add AuthService to dependency injection container</action>
    <action>Remove legacy authentication code</action>
  </actions>

  <!-- Required: How to verify task completion -->
  <verify>
    <step>npm test -- AuthService</step>
    <step>npm run build</step>
    <step>Manual: Verify login works with test credentials</step>
  </verify>

  <!-- Required: Criteria that define "done" -->
  <done>
    <criterion>AuthService class exists at specified path</criterion>
    <criterion>Login succeeds with valid credentials</criterion>
    <criterion>Login fails gracefully with invalid credentials</criterion>
    <criterion>Logout clears session state</criterion>
  </done>

  <!-- Required: Conventional commit message for this task -->
  <commit>feat(auth): add AuthService with login/logout functionality</commit>
</task>
```

## Element Reference

### `<task>` (Root Element)

| Attribute | Type | Required | Values |
|-----------|------|----------|--------|
| `id` | string | Yes | TASK-XXX format |
| `status` | enum | Yes | pending, in_progress, completed, blocked, skipped |

### `<name>`

Short, descriptive task name. Should:
- Be 5-10 words
- Start with a verb (Implement, Add, Create, Fix, Update, Remove)
- Be specific enough to distinguish from other tasks
- Not include technical jargon unless necessary

**Examples:**
```xml
<name>Add user registration endpoint</name>
<name>Fix cart total calculation bug</name>
<name>Create email notification service</name>
```

### `<description>`

Fuller explanation of what the task accomplishes. Should:
- Be 1-2 sentences
- Explain the "what" and optionally "why"
- Provide context for implementer
- Not duplicate the name

**Examples:**
```xml
<description>
  Implement the /api/users/register endpoint that accepts email and password,
  validates input, and creates a new user account with proper password hashing.
</description>
```

### `<depends>`

Comma-separated list of task IDs that must complete before this task. Should:
- Only include direct dependencies
- Not create circular references
- Be re-evaluated if dependency is blocked

**Examples:**
```xml
<depends>TASK-001</depends>
<depends>TASK-001, TASK-002, TASK-003</depends>
```

### `<files>`

Container for file operations. Each `<file>` element specifies:

| Attribute | Values | Description |
|-----------|--------|-------------|
| `action` | create | New file to create |
| `action` | modify | Existing file to change |
| `action` | delete | File to remove |
| `action` | rename | File to rename (use `from` attribute) |

**Examples:**
```xml
<files>
  <file action="create">src/services/NewService.ts</file>
  <file action="modify">src/index.ts</file>
  <file action="delete">src/deprecated/OldService.ts</file>
  <file action="rename" from="src/temp.ts">src/final.ts</file>
</files>
```

### `<actions>`

Container for specific steps. Each `<action>` should be:
- A single, concrete step
- Written as an imperative statement
- Achievable without ambiguity
- Listed in execution order

**Examples:**
```xml
<actions>
  <action>Create UserService class in src/services/</action>
  <action>Add getById method that queries the database</action>
  <action>Add create method that validates and inserts user</action>
  <action>Export UserService from services/index.ts</action>
</actions>
```

### `<verify>`

Container for verification steps. Each `<step>` can be:
- A command to run
- A manual check to perform
- A condition to confirm

**Command Steps:**
```xml
<verify>
  <step>npm test -- UserService.test.ts</step>
  <step>npm run build</step>
  <step>npm run lint -- src/services/UserService.ts</step>
</verify>
```

**Manual Steps:**
```xml
<verify>
  <step>Manual: Navigate to /users page and confirm list renders</step>
  <step>Manual: Create a user and verify it appears in the list</step>
</verify>
```

**Mixed Steps:**
```xml
<verify>
  <step>npm test -- integration</step>
  <step>Manual: Verify no console errors in browser</step>
  <step>curl http://localhost:3000/health returns 200</step>
</verify>
```

### `<done>`

Container for completion criteria. Each `<criterion>` should be:
- Observable/measurable
- Binary (either met or not)
- Specific to this task

**Examples:**
```xml
<done>
  <criterion>UserService class exists and exports correctly</criterion>
  <criterion>All unit tests pass</criterion>
  <criterion>TypeScript compiles without errors</criterion>
  <criterion>API endpoint returns expected response format</criterion>
</done>
```

### `<commit>`

Conventional commit message for this task. Format:
```
<type>(<scope>): <description>
```

**Examples:**
```xml
<commit>feat(user): add UserService with CRUD operations</commit>
<commit>fix(auth): handle expired token gracefully</commit>
<commit>refactor(api): extract validation into middleware</commit>
<commit>test(cart): add edge case coverage for empty cart</commit>
```

## Task Templates by Type

### Feature Task
```xml
<task id="TASK-XXX" status="pending">
  <name>Add [feature name]</name>
  <description>Implement [feature] that allows [user action]</description>
  <files>
    <file action="create">[new file path]</file>
    <file action="modify">[integration point]</file>
  </files>
  <actions>
    <action>Create [component/service/class]</action>
    <action>Implement [core functionality]</action>
    <action>Add [integration/wiring]</action>
    <action>Write tests for [scenarios]</action>
  </actions>
  <verify>
    <step>[test command]</step>
    <step>[build command]</step>
  </verify>
  <done>
    <criterion>Feature is accessible via [entry point]</criterion>
    <criterion>Tests cover [scenarios]</criterion>
  </done>
  <commit>feat([scope]): add [feature description]</commit>
</task>
```

### Bug Fix Task
```xml
<task id="TASK-XXX" status="pending">
  <name>Fix [bug description]</name>
  <description>Resolve issue where [problem description]</description>
  <files>
    <file action="modify">[file with bug]</file>
  </files>
  <actions>
    <action>Identify root cause in [location]</action>
    <action>Apply fix by [correction]</action>
    <action>Add regression test</action>
  </actions>
  <verify>
    <step>[test command]</step>
    <step>Manual: Verify [original issue] no longer occurs</step>
  </verify>
  <done>
    <criterion>Original issue no longer reproduces</criterion>
    <criterion>Regression test passes</criterion>
    <criterion>No new issues introduced</criterion>
  </done>
  <commit>fix([scope]): [bug fix description]</commit>
</task>
```

### Refactor Task
```xml
<task id="TASK-XXX" status="pending">
  <name>Refactor [component] to [improvement]</name>
  <description>Restructure [code area] to improve [quality attribute]</description>
  <files>
    <file action="modify">[files to refactor]</file>
  </files>
  <actions>
    <action>Extract [method/class/module]</action>
    <action>Rename [identifiers] for clarity</action>
    <action>Update [dependent code]</action>
  </actions>
  <verify>
    <step>[full test suite]</step>
    <step>[build command]</step>
  </verify>
  <done>
    <criterion>All existing tests still pass</criterion>
    <criterion>No functional behavior changed</criterion>
    <criterion>[Quality improvement] achieved</criterion>
  </done>
  <commit>refactor([scope]): [refactoring description]</commit>
</task>
```

## Parsing Tasks

### Extract Tasks from ITEM-XXX.md
```javascript
// Regex pattern to extract tasks
const taskPattern = /<task[^>]*>([\s\S]*?)<\/task>/g;

// Extract status
const statusPattern = /status="([^"]+)"/;

// Extract ID
const idPattern = /id="([^"]+)"/;
```

### Update Task Status
```javascript
// Find task by ID and update status
const updateStatus = (planContent, taskId, newStatus) => {
  const pattern = new RegExp(
    `(<task[^>]*id="${taskId}"[^>]*status=")([^"]+)(")`,
    'g'
  );
  return planContent.replace(pattern, `$1${newStatus}$3`);
};
```
