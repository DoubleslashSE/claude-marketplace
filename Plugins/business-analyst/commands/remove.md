---
description: Remove, deprecate, or modify existing requirements. Supports deleting by ID, marking as deprecated, or reverting the last session's additions.
---

# Remove or Modify Requirements

Remove/modify: **$ARGUMENTS**

## Overview

This command lets you remove, deprecate, or revert requirements in an existing `.business-analyst/` project. All removals are logged in the changelog for audit trail.

**IDs are never reused** — deleted requirement IDs remain in the changelog as "removed" entries.

## Modes

### Mode 1: Remove by ID
```bash
/business-analyst:remove FR-013
/business-analyst:remove FR-013 FR-014 NFR-SEC-003
```

### Mode 2: Deprecate (soft remove)
```bash
/business-analyst:remove --deprecate FR-013
```
Marks the requirement as "Deprecated" rather than deleting it. It remains in the file but is excluded from SRS generation and counts.

### Mode 3: Revert Last Session
```bash
/business-analyst:remove --revert-last
```
Removes all requirements added in the most recent session (using session log from `project.json`).

## Process

### Step 1: Load Project

1. Locate `.business-analyst/` directory
2. Read `project.json` for session history
3. If no project: "No project found."

### Step 2: Find Target Requirements

**For remove by ID:**
1. Search requirement files for the specified IDs
2. If an ID is not found: "FR-099 not found. Skipping."
3. Display each found requirement:
   > "Found FR-013: {description} (Priority: Must, Added: {date})
   > Are you sure you want to remove this? (yes/no)"

**For revert last session:**
1. Read the last session entry from `project.json.sessions`
2. Identify all requirements added in that session
3. Display them:
   > "Last session ({date}) added {N} requirements:
   > - FR-013: {title}
   > - FR-014: {title}
   > - NFR-SEC-003: {title}
   >
   > Remove all of these? (yes/no/select)"

### Step 3: Confirm and Execute

**Always require explicit confirmation before removing.**

For each confirmed removal:

1. **Remove** the requirement from the appropriate file (or mark as Deprecated)
2. **Do NOT decrement counters** — IDs are never reused
3. **Update traceability** — remove from traceability.md
4. **Update data dictionary** — flag data elements that were only referenced by removed requirements
5. **Log the removal** in changelog.md:
   ```
   ### Removed
   - FR-013: {title} — Reason: {user-provided reason or "User requested removal"}
   ```

### Step 4: Impact Report

After removal, report any impact:

```markdown
## Removal Summary

### Removed
| ID | Title | Was Priority |
|----|-------|-------------|
| FR-013 | {title} | Must |

### Impact
- **Traceability**: BO-002 now has no implementing requirements (was linked via FR-013)
- **Dependencies**: FR-020 depended on FR-013 — review needed
- **Risk register**: RISK-004 referenced FR-013 — may need update
- **Data dictionary**: DE-007 was only used by FR-013 — consider removing

### Counters
| Category | Before | After |
|----------|--------|-------|
| Functional | 14 | 13 |
```

## Safety Checks

- **Must-Have removal warning**: If removing a Must-priority requirement:
  > "FR-013 is marked as Must Have. Removing it may significantly impact project scope. Are you sure?"

- **Dependency warning**: If other requirements depend on the one being removed:
  > "FR-020 depends on FR-013. Removing FR-013 may break this dependency. Proceed?"

- **Bulk removal limit**: If removing more than 10 requirements at once:
  > "You're about to remove {N} requirements. This is a large change. Please confirm by typing 'confirm remove {N}'."

## Usage Examples

```bash
# Remove a single requirement
/business-analyst:remove FR-013

# Remove multiple
/business-analyst:remove FR-013 FR-014 NFR-SEC-003

# Soft-remove (deprecate, keeps in file but excluded from SRS)
/business-analyst:remove --deprecate FR-013

# Undo the last session's additions
/business-analyst:remove --revert-last

# Remove with reason
/business-analyst:remove FR-013 --reason "Replaced by FR-025"
```
