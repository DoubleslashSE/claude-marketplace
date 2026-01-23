---
name: capability-discovery
description: Dynamic plugin enumeration and capability mapping with delegation priority and explicit routing announcements
triggers:
  - plugin discovery
  - capability mapping
  - agent routing
  - plugin enumeration
  - delegation
---

# Capability Discovery Skill

This skill enables dynamic discovery and mapping of installed plugins to abstract capability categories, allowing the workflow to route tasks to appropriate agents without hardcoding plugin names. It includes explicit delegation announcements so users understand routing decisions.

## Core Principles

1. **Technology Agnostic**: Map capabilities, not specific plugins
2. **Dynamic Discovery**: Scan at runtime, not compile time
3. **Graceful Fallback**: Use internal default agents when no plugin matches
4. **Project-Aware Routing**: Prefer plugins matching detected project type
5. **Transparent Delegation**: Always announce why a particular agent was chosen

## Capability Categories

| Capability | Purpose | Phase | Default Agent |
|------------|---------|-------|---------------|
| `requirements-gathering` | Structured requirements elicitation | DISCUSS | defaults/interviewer |
| `brainstorming` | Ideation and option exploration | DISCUSS | defaults/interviewer |
| `codebase-analysis` | Understanding existing code | DISCUSS, PLAN | defaults/researcher |
| `tdd-implementation` | Test-driven development | EXECUTE | defaults/executor |
| `code-implementation` | General code writing | EXECUTE | defaults/executor |
| `infrastructure` | DevOps/infra tasks | EXECUTE | defaults/executor |
| `code-review` | Quality validation | VERIFY | validator |
| `requirements-validation` | Requirements compliance | VERIFY | validator |

## Discovery Process

### Step 1: Enumerate Installed Plugins

```markdown
1. Locate Plugins/ directory
2. List all subdirectories (each is a plugin)
3. For each plugin:
   a. Read .claude-plugin/plugin.json for metadata
   b. Scan agents/*.md for agent definitions
   c. Scan commands/*.md for command definitions
4. Build plugin registry
```

### Step 2: Extract Descriptions

For each agent/command file, extract the description from YAML frontmatter:

```yaml
---
name: implementer
description: TDD implementation specialist for .NET. Use to write minimal code that makes tests pass.
model: opus
tools: [Read, Write, Edit, Bash, Grep, Glob]
---
```

### Step 3: Map to Capabilities (Keyword Scoring)

Apply keyword matching to descriptions:

```markdown
For each plugin agent/command:
  1. Tokenize description into words (lowercase)
  2. Match against capability keywords
  3. Calculate score:
     - Exact keyword match: +10 points
     - Partial match (word contains keyword): +3 points
     - Keyword in first sentence: +5 bonus
     - Multiple keywords from same category: +2 each after first
  4. Assign to highest-scoring capability
  5. Record match confidence (High: 25+, Medium: 15-24, Low: <15)
```

### Step 4: Detect Project Type

Scan project root for technology indicators:

| File Pattern | Project Type | Keywords |
|--------------|--------------|----------|
| `*.csproj`, `*.sln` | dotnet | .NET, dotnet, C#, csharp |
| `package.json`, `*.js`, `*.ts` | node | Node.js, JavaScript, TypeScript |
| `*.py`, `requirements.txt` | python | Python, pip, pytest |
| `go.mod`, `*.go` | go | Go, golang |
| `Cargo.toml`, `*.rs` | rust | Rust, Cargo |
| `pom.xml`, `build.gradle` | java | Java, Maven, Gradle |

### Step 5: Cache Results in FLOW.md

Store capability mappings in the Capabilities Cache section of FLOW.md.

## Delegation Priority System

When routing a task to an agent, follow this priority order:

### Priority 1: Project-Type Match

If project is detected (e.g., dotnet), prefer plugins with matching technology keywords in their description.

```markdown
Detected: dotnet project
Capability needed: tdd-implementation

Matches:
- dotnet-tdd:implementer (description: "TDD for .NET") → Score: 35 + project bonus
- node-tdd:implementer (description: "TDD for Node.js") → Score: 30

Winner: dotnet-tdd:implementer (project type match)
```

### Priority 2: Exact Keyword Match

Prefer agents with exact keyword matches over partial matches.

### Priority 3: Agent Over Command

When both an agent and a command match a capability, prefer the agent (more capable).

### Priority 4: Internal Default

When no plugin matches the capability, use the appropriate default agent.

## Delegation Announcement Pattern

**CRITICAL**: Always announce delegation decisions to the user with reasoning.

### When Plugin Found

```markdown
**Delegating [capability]** → [plugin-name]:[agent-name]

Matched via keyword scoring:
- Keywords: [matched keywords]
- Score: [score] (High confidence)
- Project type: [type] (matched)

Spawning agent...
```

### When Using Default

```markdown
**Using built-in agent** for [capability] → flow-workflow:defaults/[agent]

No installed plugin matched this capability.
- Searched: [N] plugins
- Keywords tried: [keywords]

Consider installing: [suggested plugin type]
```

### Quick Delegation (For Status/Logs)

```markdown
→ [capability]: [plugin:agent] (keyword match)
→ [capability]: defaults/[agent] (no plugin match)
```

## Routing Logic

### When Phase Needs Capability

```markdown
1. Determine capability needed for current task
2. Look up FLOW.md capability cache
3. If cache stale (>24h) or missing, re-scan plugins
4. If multiple matches for capability:
   a. Filter by project type preference
   b. Prefer exact keyword matches
   c. Prefer agents over commands
5. If single match:
   a. Announce delegation with reasoning
   b. Return agent reference
6. If no match:
   a. Announce using default
   b. Return default agent reference
```

### Capability → Phase Mapping

| Phase | Primary Capability | Secondary Capabilities |
|-------|-------------------|----------------------|
| DISCUSS | requirements-gathering | brainstorming, codebase-analysis |
| PLAN | (internal coordinator) | codebase-analysis |
| EXECUTE | code-implementation | tdd-implementation, infrastructure |
| VERIFY | code-review | requirements-validation |

## Default Agents

When no plugin matches a capability:

| Capability | Default Agent | Location |
|------------|---------------|----------|
| requirements-gathering | interviewer | flow-workflow:defaults/interviewer |
| brainstorming | interviewer | flow-workflow:defaults/interviewer |
| codebase-analysis | researcher | flow-workflow:defaults/researcher |
| tdd-implementation | executor | flow-workflow:defaults/executor |
| code-implementation | executor | flow-workflow:defaults/executor |
| infrastructure | executor | flow-workflow:defaults/executor |
| code-review | validator | flow-workflow:validator |
| requirements-validation | validator | flow-workflow:validator |

## Re-Discovery Triggers

Re-scan plugins when:

1. `/flow:start` is run on uninitialized project
2. FLOW.md capability cache is older than 24 hours
3. Requested capability returns no match (try fresh scan)
4. User explicitly requests refresh via `/flow:status --refresh`

## Capability Gap Logging

When no plugin matches a capability, log in FLOW.md:

```markdown
## Capability Warnings

**[TIMESTAMP]**: No plugin found for capability 'infrastructure'
- Searched: 5 plugins
- Keywords tried: infra, devops, pipeline, deploy
- Using: flow-workflow:defaults/executor
- Suggestion: Consider installing a DevOps plugin
```

## Integration Points

- **State Management**: Cache capability map in FLOW.md
- **Coordinator Agent**: Performs discovery on initialization, uses for routing
- **Smart Continuation**: Uses cached capabilities for agent selection

See `categories.md` for detailed capability category definitions.
