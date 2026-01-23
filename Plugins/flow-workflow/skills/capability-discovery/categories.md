# Capability Category Definitions

## Overview

Capability categories provide an abstraction layer between workflow phases and specific plugin implementations. This enables technology-agnostic orchestration with transparent delegation.

## Category Definitions

### requirements-gathering

**Purpose**: Structured elicitation of project requirements from stakeholders

**When Used**: DISCUSS phase, when understanding what to build

**Keywords**: `requirements`, `interview`, `elicitation`, `stakeholder`, `gathering`, `discover`, `needs`

**Expected Behaviors**:
- Conduct structured interviews
- Ask clarifying questions
- Document functional requirements
- Document non-functional requirements
- Identify constraints and assumptions

**Default Agent**: `flow-workflow:defaults/interviewer`

---

### codebase-analysis

**Purpose**: Understanding existing code, patterns, and architecture

**When Used**: DISCUSS phase (for brownfield projects), PLAN phase (for implementation planning)

**Keywords**: `codebase`, `analyze`, `reverse-engineer`, `patterns`, `architecture`, `existing`, `legacy`

**Expected Behaviors**:
- Scan project structure
- Identify design patterns
- Detect technologies in use
- Find integration points
- Document existing behavior

**Default Agent**: `flow-workflow:defaults/researcher`

---

### brainstorming

**Purpose**: Creative exploration of ideas and options

**When Used**: DISCUSS phase, when exploring possible approaches

**Keywords**: `brainstorm`, `ideation`, `workshop`, `creative`, `explore`, `options`, `ideas`

**Expected Behaviors**:
- Facilitate idea generation
- Divergent thinking exercises
- Option comparison
- Trade-off analysis
- Convergent selection

**Default Agent**: `flow-workflow:defaults/interviewer` (with brainstorming prompts)

---

### tdd-implementation

**Purpose**: Test-driven development with RED-GREEN-REFACTOR cycle

**When Used**: EXECUTE phase, when implementing with tests first

**Keywords**: `tdd`, `test-driven`, `red-green`, `refactor`, `tests first`, `failing test`

**Expected Behaviors**:
- Write failing tests first (RED)
- Implement minimal code to pass (GREEN)
- Refactor for quality (REFACTOR)
- Maintain test coverage
- Follow clean code principles

**Default Agent**: `flow-workflow:defaults/executor` (with TDD guidance)

---

### code-implementation

**Purpose**: General code writing and modification

**When Used**: EXECUTE phase, for any coding task

**Keywords**: `implement`, `developer`, `code`, `write`, `create`, `build`, `feature`

**Expected Behaviors**:
- Write production code
- Follow project conventions
- Handle errors appropriately
- Integrate with existing code
- Document as needed

**Default Agent**: `flow-workflow:defaults/executor`

---

### infrastructure

**Purpose**: DevOps, CI/CD, and infrastructure tasks

**When Used**: EXECUTE phase, for deployment and operations

**Keywords**: `infra`, `devops`, `pipeline`, `deploy`, `docker`, `kubernetes`, `ci`, `cd`, `terraform`, `azure`

**Expected Behaviors**:
- Configure build pipelines
- Write deployment scripts
- Manage infrastructure as code
- Set up environments
- Configure monitoring

**Default Agent**: `flow-workflow:defaults/executor` (with infrastructure guidance)

---

### code-review

**Purpose**: Quality validation of implemented code

**When Used**: VERIFY phase, after implementation

**Keywords**: `review`, `quality`, `clean code`, `solid`, `dry`, `kiss`, `standards`

**Expected Behaviors**:
- Review code for quality
- Check adherence to standards
- Identify potential issues
- Suggest improvements
- Validate best practices

**Default Agent**: `flow-workflow:validator`

---

### requirements-validation

**Purpose**: Verify implementation meets requirements

**When Used**: VERIFY phase, for acceptance testing

**Keywords**: `validate`, `verification`, `compliance`, `acceptance`, `requirements`, `uat`

**Expected Behaviors**:
- Check requirements coverage
- Validate acceptance criteria
- Identify gaps
- Conduct UAT
- Document compliance

**Default Agent**: `flow-workflow:validator`

---

## Keyword Matching Algorithm

### Scoring Rules

```
1. Exact keyword match: +10 points
2. Partial match (word contains keyword): +3 points
3. Keyword in first sentence: +5 bonus
4. Multiple keywords from same category: +2 each after first
5. Project type match: +10 bonus
```

### Confidence Levels

| Score | Confidence | Meaning |
|-------|------------|---------|
| 25+ | High | Strong match, safe to delegate |
| 15-24 | Medium | Good match, may need verification |
| <15 | Low | Weak match, consider default |

### Matching Example

**Description**: "TDD implementation specialist for .NET. Write minimal code that makes tests pass."

```
Keyword matches:
- "TDD" → tdd-implementation (+10)
- "implementation" → code-implementation (+10)
- "tests" → tdd-implementation (+10)
- ".NET" → (project type indicator)

Scores:
- tdd-implementation: 20 + 5 (first sentence) = 25 (High)
- code-implementation: 10 (Low)

Winner: tdd-implementation
```

---

## Project Type Routing

### When Multiple Capabilities Match

If multiple plugins match a capability, filter by project type:

```
Capability: tdd-implementation
Matches:
- dotnet-tdd:implementer (description contains ".NET")
- node-tdd:implementer (description contains "Node.js")

Detected project type: dotnet

Selected: dotnet-tdd:implementer (+10 project bonus)
```

### Project Type Keywords

| Project Type | Description Keywords |
|--------------|---------------------|
| dotnet | `.NET`, `dotnet`, `C#`, `csharp`, `NuGet` |
| node | `Node.js`, `node`, `JavaScript`, `TypeScript`, `npm`, `yarn` |
| python | `Python`, `pip`, `pytest`, `Django`, `Flask` |
| go | `Go`, `golang`, `Gin`, `Echo` |
| rust | `Rust`, `Cargo`, `crate` |
| java | `Java`, `Maven`, `Gradle`, `Spring` |

---

## Default Agent Summary

| Capability | Default Agent | Why |
|------------|---------------|-----|
| requirements-gathering | defaults/interviewer | General interview skills |
| brainstorming | defaults/interviewer | Facilitation skills overlap |
| codebase-analysis | defaults/researcher | General research skills |
| tdd-implementation | defaults/executor | TDD guidance built in |
| code-implementation | defaults/executor | General coding skills |
| infrastructure | defaults/executor | Infra guidance built in |
| code-review | validator | Review is built-in function |
| requirements-validation | validator | UAT is built-in function |

---

## Capability Gap Handling

### When No Plugin Matches

1. Log warning to FLOW.md with timestamp
2. Announce to user: "Using built-in agent (no plugin matched)"
3. Use appropriate default agent
4. Suggest plugin installation if capability is important

### Suggested Plugins by Capability

| Missing Capability | Suggested Plugin Type |
|-------------------|----------------------|
| requirements-gathering | business-analyst |
| brainstorming | workshop-facilitator |
| codebase-analysis | business-analyst |
| tdd-implementation | dotnet-tdd, node-tdd |
| code-implementation | developer plugin for project type |
| infrastructure | devops-azure-infrastructure, infra-plugin |
| code-review | tdd plugin with reviewer |
| requirements-validation | business-analyst |

---

## Delegation Announcement Templates

### Plugin Match

```markdown
**Delegating requirements-gathering** → business-analyst:stakeholder-interviewer

Matched via keyword scoring:
- Keywords: requirements, interview, stakeholder
- Score: 30 (High confidence)
- Project type: dotnet (neutral)
```

### Default Agent

```markdown
**Using built-in agent** for infrastructure → flow-workflow:defaults/executor

No installed plugin matched this capability.
- Searched: 5 plugins
- Keywords tried: infra, devops, pipeline, deploy

Consider installing: devops-azure-infrastructure or similar
```

### Short Form (For Logs)

```
→ requirements-gathering: business-analyst:stakeholder-interviewer (keyword match)
→ infrastructure: defaults/executor (no plugin match)
```
