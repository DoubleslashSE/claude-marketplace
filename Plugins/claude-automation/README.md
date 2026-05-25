# Claude Automation Plugin

Automation tooling for Claude Code. Skills in this plugin help you build autonomous scripts, agent harnesses, and orchestration patterns that drive Claude Code with minimal human intervention.

## Skills

| Skill | Purpose |
|-------|---------|
| `autonomous-script-builder` | Generate bash scripts that drive Claude Code in autonomous loops (cron, GitHub Actions, on-demand). Encodes the interview flow, the adversarial-reviewer pattern, and locking/ledger conventions. |

## When to use

The `autonomous-script-builder` skill activates whenever you ask for a script whose job is "wake up, figure out what to do, ask Claude Code to do it, commit the result." Examples:

- "I want a scout script that picks one improvement per run and implements it"
- "Write me a script that implements the plan in PLAN.md"
- "I need a script that picks up GitHub issues with a specific label and works them"
- "Make a CI failure handler that files an issue when the build breaks"
- "A nightly script that updates dependencies and opens a PR"

The skill walks through a short interview (trigger model, work selection, completion criterion, reviewer scope, mutex strategy, resources, output destination) and then emits two files: an executable `<name>.sh` and a `<name>.DECISIONS.md` recording which branches the interview took.

## Conventions encoded

Every script the skill produces includes:

- Strict bash (`set -euo pipefail`, `IFS=$'\n\t'`)
- An adversarial reviewer pass (separate Claude invocation) by default — its notes and the implementor's verdict are posted as comments on the draft PR so a human can review them in context
- A self-improving learnings loop — every `LEARN_EVERY` runs (default 5), a *distiller* invocation reads the recent reviewer + verdict history and updates `LEARNINGS.md` with patterns from notes the implementor actually addressed; the implementor reads `LEARNINGS.md` at the start of every run
- Mutex/lock (sentinel label or lockfile)
- An explicit resource manifest in the prompt
- A markdown ledger appropriate to the mode (candidate ledger, plan checklist, or append-only journal)
- One unit of work per run
- Defined exit codes (0=done, 1=error, 2=nothing-to-do, 3=locked)

## Installation

Add via the marketplace, or install directly:

```bash
claude --plugin-dir ./Plugins/claude-automation
```

## License

MIT
