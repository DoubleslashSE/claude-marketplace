# Claude Code Plugin Marketplace

A collection of plugins for [Claude Code](https://claude.com/claude-code) that extend its capabilities with specialized workflows, skills, and agents.

## Available Plugins

| Plugin | Description | Version |
|--------|-------------|---------|
| [business-analyst](./Plugins/business-analyst) | Senior Business Analyst for requirements gathering, codebase analysis, stakeholder interviews, and SRS document generation | 1.1.0 |
| [claude-automation](./Plugins/claude-automation) | Automation tooling for Claude Code: autonomous script builder and related harnesses | 1.0.0 |
| [dotnet-developer](./Plugins/dotnet-developer) | General .NET development workflow with automated validation through build, test, and static analysis quality gates | 1.0.0 |
| [dotnet-tdd](./Plugins/dotnet-tdd) | Test-Driven Development for .NET following TDD, SOLID, DRY, KISS, YAGNI, and CQS principles | 1.2.2 |
| [flow-workflow](./Plugins/flow-workflow) | Lightweight meta-orchestrator that leverages your plugin ecosystem through capability-based routing | 2.0.4 |
| [infra](./Plugins/infra) | Infrastructure troubleshooting for diagnosing and resolving issues across GitHub Actions, Railway, Supabase, and Postgres | 1.0.0 |
| [node-tdd](./Plugins/node-tdd) | Node.js Test-Driven Development with TypeScript support, SOLID principles, clean code practices, and functional patterns | 1.1.1 |
| [requirements-engineering](./Plugins/requirements-engineering) | Interactively elicit and maintain software requirements as a living, traceable repository: SRS docs, MADR ADRs, a traceability DAG, and a decision ledger, with a validator enforcing atomic, verifiable requirements | 0.1.0 |
| [workshop-facilitator](./Plugins/workshop-facilitator) | Workshop facilitation for design thinking, brainstorming, and collaborative problem-solving sessions | 1.0.1 |

## Installation

Install a plugin by pointing Claude Code to the plugin directory:

```bash
claude --plugin-dir ./Plugins/dotnet-tdd
```

## Repository Structure

```
Plugins/
├── business-analyst/        # Requirements & SRS generation
├── claude-automation/       # Autonomous script builder & harnesses
├── dotnet-developer/        # .NET development workflow
├── dotnet-tdd/              # .NET TDD plugin
├── flow-workflow/           # Meta-orchestrator for plugin routing
├── infra/                   # Infrastructure troubleshooting
├── node-tdd/                # Node.js TDD plugin
├── requirements-engineering/ # Requirements elicitation, SRS, ADRs & traceability
├── workshop-facilitator/    # Workshop facilitation
└── [future-plugins]/
```

## Plugin Anatomy

Each plugin follows a standard structure:

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json      # Required: Plugin manifest
├── agents/              # Optional: Subagent definitions
├── commands/            # Optional: Slash commands
├── hooks/               # Optional: Event hooks
├── skills/              # Optional: Knowledge files
└── README.md            # Plugin documentation
```

### plugin.json

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "What the plugin does",
  "author": "Your Name <email>",
  "commands": ["./commands/command.md"],
  "agents": ["./agents/agent.md"],
  "skills": ["./skills/skill-name"],
  "hooks": "./hooks/hooks.json"
}
```

## Contributing

Want to add a plugin? Submit a PR with your plugin in the `Plugins/` directory following the structure above.

## License

MIT
