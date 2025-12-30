# Claude Code Workflows

A collection of autonomous workflows for [Claude Code](https://claude.com/claude-code) that enable extended, high-quality code production with minimal human intervention.

## Overview

These workflows leverage Claude Code's multi-agent capabilities to orchestrate complex software development tasks. Each workflow is designed to run autonomously for extended periods (1-4+ hours) while maintaining code quality through structured processes, quality gates, and periodic checkpoints.

## Available Workflows

### .NET / Multi-Agent Autonomous Workflow

**Location:** `dotnet/multi-agent-autonomous-workflow/`

A hierarchical multi-agent system designed for .NET projects following Clean Architecture and CQRS patterns.

**Features:**
- 7 specialized agents (Analyst, Architect, Developer, Tester, Reviewer, Security, DevOps)
- TDD-driven development with coverage thresholds
- Quality gates at each workflow phase
- OWASP Top 10 security compliance checks
- Automatic progress reporting for long sessions
- Knowledge accumulation through lessons learned
- State persistence for session resumability

**Tech Stack:**
- .NET 10 with Clean Architecture
- CQRS with MediatR
- FluentValidation
- Entity Framework Core
- xUnit + Moq for testing

## Installation

1. Copy the desired workflow's `.claude/` directory into your project root
2. Configure the hooks in your Claude Code settings if needed
3. Activate the workflow using the skill trigger

**Example activation:**
```
Use the multi-agent workflow to: Build a user authentication system
```

## Workflow Structure

Each workflow follows a consistent structure:

```
.claude/
├── agents/           # Specialized agent prompts
│   ├── analyst.md
│   ├── architect.md
│   ├── developer.md
│   ├── tester.md
│   ├── reviewer.md
│   ├── security.md
│   └── devops.md
├── hooks/            # Safety and audit hooks
│   ├── safety.py     # PreToolUse safety checks
│   ├── audit.py      # PostToolUse logging
│   └── state.py      # Workflow state management
├── skills/           # Skill definitions
│   └── {workflow-name}/
│       └── SKILL.md  # Main orchestration guide
├── workflow-state-schema.json
└── lessons-learned.md
```

## Key Concepts

### Hierarchical Agent Architecture

```
ORCHESTRATOR (Main Claude instance)
├── ANALYST     → Requirements & user stories
├── ARCHITECT   → Technical design
├── DEVELOPER   → TDD implementation
├── TESTER      → Verification
├── REVIEWER    → Code quality
├── SECURITY    → Security review
└── DEVOPS      → Infrastructure
```

### Quality Gates

| Gate | Phase | Checks |
|------|-------|--------|
| G1 | Pre-Implementation | Design clarity, AC defined |
| G2 | Post-Implementation | Build passes, tests pass |
| G3 | Coverage | Meets threshold (70-90%) |
| G4 | Security | OWASP compliance |
| G5 | Review | Architecture compliance |

### Self-Critique & Reflection

Each agent includes:
- **Thinking Process:** Documented reasoning before action
- **Reflection:** Self-verification before handoff
- **Confidence Rating:** High/Medium/Low to guide escalation

### Autonomous Features

- **State Persistence:** Workflows survive context limits
- **Checkpoints:** Human review every N stories
- **Smart Retry:** Root cause analysis on failures
- **Progress Reports:** Automatic status updates
- **Knowledge Accumulation:** Lessons learned for future sessions

## Safety Features

- **Blocked Patterns:** Dangerous operations auto-blocked (rm -rf, DROP TABLE, etc.)
- **Confirmation Required:** Sensitive operations require approval (git push, migrations)
- **Protected Files:** Secrets and credentials cannot be modified
- **Audit Logging:** All tool usage logged for debugging

## Customization

### Adjusting Strictness

```
Use multi-agent workflow (strict mode) to: Build payment processing
```

| Level | TDD | Review | Coverage |
|-------|-----|--------|----------|
| strict | Full | Comprehensive | 90%+ |
| balanced | Core logic | Pragmatic | 80%+ |
| fast | Minimal | Quick | 70%+ |

### Adding New Agents

1. Create agent definition in `.claude/agents/{name}.md`
2. Define: Role, Allowed Tools, Responsibilities, Output Format
3. Add spawn pattern to SKILL.md
4. Update files reference

## Contributing

When adding new workflows:

1. Follow the established directory structure
2. Include all required agent definitions
3. Document activation and configuration
4. Add safety hooks for dangerous operations
5. Include quality gates appropriate to the tech stack

## License

MIT

---

*Built for autonomous software development with Claude Code*
