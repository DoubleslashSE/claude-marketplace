# Requirements Engineering

A plugin that turns the messy work of figuring out *what to build* into a durable,
traceable requirements repository — and keeps it that way as the project evolves.

## What it does

Once installed, this plugin adds a skill that helps you:

- **Interview your way to requirements.** It asks focused questions in small batches,
  reflects your answers back as concrete, testable statements, and follows the
  threads that matter — instead of making you fill in a blank template.
- **Capture requirements as structured, traceable records.** Each requirement is an
  atomic, uniquely-identified, verifiable item linked to the higher-level need it
  serves, so you can always answer "why does this exist?" and "what breaks if we drop it?"
- **Record the decisions behind the requirements** as architecture decision records
  (MADR format), with the options considered and the trade-offs accepted.
- **Generate the readable spec** — a Software Requirements Specification organized to
  the ISO/IEC/IEEE 29148 standard, produced from the underlying records so it never
  drifts out of sync.
- **Keep an audit trail.** An append-only ledger records every material change.
- **Validate the whole repository** — a built-in checker flags requirements with no
  way to verify them, broken or circular traceability links, and orphaned items.

## When it kicks in

The skill triggers when you ask to spec something out, capture or organize
requirements, write a decision record, or turn notes / a feature brief into a proper
specification — and automatically when you're working in a folder that already
contains a requirements repository.

## What it produces

A `requirements/` folder containing per-requirement records, decision records, a
generated SRS document, a traceability graph, and a change ledger.

## Notes

The validator uses Python with the PyYAML package. If it isn't already available,
install it with `pip install pyyaml`.

## Sharing

Send the `.plugin` file to teammates; each person installs it from the chat preview.
For wider distribution, publish it to a marketplace your team installs from.
