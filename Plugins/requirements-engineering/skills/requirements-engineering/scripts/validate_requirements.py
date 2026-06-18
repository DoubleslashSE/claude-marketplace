#!/usr/bin/env python3
"""Validate a requirements repository and (optionally) emit a Mermaid DAG.

Usage:
    python validate_requirements.py <reqs_dir> [--mermaid OUT.mmd] [--json]

<reqs_dir> is a directory of one-requirement-per-file YAML files (e.g.
requirements/reqs). Each file may also contain a YAML list of requirements, or a
mapping with a top-level `requirements:` list — all are accepted.

Checks performed:
  ERROR  - duplicate ids
  ERROR  - missing required fields (id, title, type, statement, priority, status)
  ERROR  - invalid enum values (type, priority, status, verification.method)
  ERROR  - dangling references in derived_from / depends_on / conflicts_with
  ERROR  - cycles in the derived_from + depends_on graph (must be acyclic)
  ERROR  - non-stakeholder requirement missing derived_from
  WARN   - functional/nonfunctional requirement missing a verification block
  WARN   - orphan (non-stakeholder requirement whose parents don't reach a stakeholder)
  WARN   - unresolved conflicts_with links

Exit code is non-zero if any ERROR is found, so it can gate a workflow.
"""
import argparse
import glob
import json
import os
import sys

try:
    import yaml
except ImportError:
    sys.stderr.write(
        "PyYAML is required. Install it with:\n"
        "    pip install pyyaml --break-system-packages\n"
    )
    sys.exit(2)

TYPES = {"stakeholder", "system", "functional", "nonfunctional", "interface", "constraint"}
PRIORITIES = {"must", "should", "could", "wont"}
STATUSES = {"proposed", "accepted", "implemented", "verified", "deprecated"}
METHODS = {"test", "analysis", "inspection", "demonstration"}
REQUIRED = ["id", "title", "type", "statement", "priority", "status"]
NEEDS_VERIFICATION = {"functional", "nonfunctional"}


def load_requirements(reqs_dir):
    """Return (list_of_req_dicts, list_of_load_errors)."""
    reqs, errors = [], []
    paths = sorted(
        glob.glob(os.path.join(reqs_dir, "**", "*.yaml"), recursive=True)
        + glob.glob(os.path.join(reqs_dir, "**", "*.yml"), recursive=True)
    )
    for path in paths:
        try:
            with open(path, "r", encoding="utf-8") as fh:
                data = yaml.safe_load(fh)
        except yaml.YAMLError as exc:
            errors.append(f"{os.path.basename(path)}: YAML parse error: {exc}")
            continue
        if data is None:
            continue
        if isinstance(data, dict) and "requirements" in data and isinstance(data["requirements"], list):
            items = data["requirements"]
        elif isinstance(data, list):
            items = data
        else:
            items = [data]
        for item in items:
            if not isinstance(item, dict):
                errors.append(f"{os.path.basename(path)}: expected a mapping, got {type(item).__name__}")
                continue
            item.setdefault("_file", os.path.basename(path))
            reqs.append(item)
    return reqs, errors


def as_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def validate(reqs):
    errors, warnings = [], []

    # ID uniqueness + basic field/enum checks.
    by_id = {}
    for r in reqs:
        rid = r.get("id")
        loc = r.get("_file", "?")
        for field in REQUIRED:
            if not r.get(field):
                errors.append(f"[{loc}] missing required field '{field}'")
        if rid:
            if rid in by_id:
                errors.append(f"duplicate id '{rid}' (in {loc} and {by_id[rid].get('_file')})")
            else:
                by_id[rid] = r
        if r.get("type") and r["type"] not in TYPES:
            errors.append(f"[{rid}] invalid type '{r['type']}' (allowed: {sorted(TYPES)})")
        if r.get("priority") and r["priority"] not in PRIORITIES:
            errors.append(f"[{rid}] invalid priority '{r['priority']}'")
        if r.get("status") and r["status"] not in STATUSES:
            errors.append(f"[{rid}] invalid status '{r['status']}'")
        ver = r.get("verification")
        if ver is not None:
            if not isinstance(ver, dict) or not ver.get("method") or not ver.get("criterion"):
                errors.append(f"[{rid}] verification must have 'method' and 'criterion'")
            elif ver["method"] not in METHODS:
                errors.append(f"[{rid}] invalid verification.method '{ver['method']}'")

    ids = set(by_id)

    # Reference integrity + verification / derivation rules.
    for r in reqs:
        rid = r.get("id")
        for field in ("derived_from", "depends_on", "conflicts_with"):
            for ref in as_list(r.get(field)):
                if ref not in ids:
                    errors.append(f"[{rid}] {field} points at unknown id '{ref}'")
        if r.get("type") and r["type"] != "stakeholder" and not as_list(r.get("derived_from")):
            errors.append(f"[{rid}] non-stakeholder requirement has no derived_from (orphan edge)")
        if r.get("type") in NEEDS_VERIFICATION and not r.get("verification"):
            warnings.append(f"[{rid}] {r['type']} requirement has no verification block")
        for ref in as_list(r.get("conflicts_with")):
            if ref in ids:
                warnings.append(f"[{rid}] declares conflict with {ref} — ensure it is resolved")

    # Cycle detection over derived_from + depends_on.
    adj = {rid: [] for rid in ids}
    for r in reqs:
        rid = r.get("id")
        if rid not in adj:
            continue
        for ref in as_list(r.get("derived_from")) + as_list(r.get("depends_on")):
            if ref in ids:
                adj[rid].append(ref)

    WHITE, GREY, BLACK = 0, 1, 2
    color = {rid: WHITE for rid in ids}
    cycle_path = []

    def dfs(node, stack):
        color[node] = GREY
        stack.append(node)
        for nxt in adj[node]:
            if color[nxt] == GREY:
                i = stack.index(nxt)
                cycle_path.extend(stack[i:] + [nxt])
                return True
            if color[nxt] == WHITE and dfs(nxt, stack):
                return True
        stack.pop()
        color[node] = BLACK
        return False

    for rid in ids:
        if color[rid] == WHITE and dfs(rid, []):
            errors.append("cycle detected: " + " -> ".join(cycle_path))
            break

    # Orphan check: can each non-stakeholder reach a stakeholder via derived_from?
    parents = {r.get("id"): as_list(r.get("derived_from")) for r in reqs if r.get("id")}
    types = {r.get("id"): r.get("type") for r in reqs if r.get("id")}

    def reaches_stakeholder(rid, seen):
        if rid in seen:
            return False
        seen.add(rid)
        if types.get(rid) == "stakeholder":
            return True
        return any(reaches_stakeholder(p, seen) for p in parents.get(rid, []) if p in ids)

    for rid in ids:
        if types.get(rid) != "stakeholder" and not reaches_stakeholder(rid, set()):
            warnings.append(f"[{rid}] does not trace up to any stakeholder requirement")

    return errors, warnings, by_id, adj


def to_mermaid(by_id, adj):
    lines = ["graph TD"]
    # Node labels with id + short title.
    for rid, r in sorted(by_id.items()):
        title = str(r.get("title", "")).replace('"', "'")
        lines.append(f'    {san(rid)}["{rid}: {title}"]')
    # derived_from + depends_on edges (adj already merges both).
    for rid, r in sorted(by_id.items()):
        for ref in as_list(r.get("derived_from")):
            if ref in by_id:
                lines.append(f"    {san(ref)} --> {san(rid)}")
        for ref in as_list(r.get("depends_on")):
            if ref in by_id:
                lines.append(f"    {san(rid)} -.depends.-> {san(ref)}")
    return "\n".join(lines) + "\n"


def san(rid):
    return rid.replace("-", "_")


def main():
    ap = argparse.ArgumentParser(description="Validate a requirements repository.")
    ap.add_argument("reqs_dir", help="directory of requirement YAML files")
    ap.add_argument("--mermaid", metavar="OUT", help="write a Mermaid DAG to this path")
    ap.add_argument("--json", action="store_true", help="emit findings as JSON")
    args = ap.parse_args()

    if not os.path.isdir(args.reqs_dir):
        sys.stderr.write(f"Not a directory: {args.reqs_dir}\n")
        sys.exit(2)

    reqs, load_errors = load_requirements(args.reqs_dir)
    errors, warnings, by_id, adj = validate(reqs)
    errors = load_errors + errors

    if args.mermaid and by_id:
        with open(args.mermaid, "w", encoding="utf-8") as fh:
            fh.write(to_mermaid(by_id, adj))

    if args.json:
        print(json.dumps({
            "count": len(by_id),
            "errors": errors,
            "warnings": warnings,
        }, indent=2))
    else:
        print(f"Requirements loaded: {len(by_id)}")
        if errors:
            print(f"\nERRORS ({len(errors)}):")
            for e in errors:
                print(f"  ✗ {e}")
        if warnings:
            print(f"\nWARNINGS ({len(warnings)}):")
            for w in warnings:
                print(f"  ! {w}")
        if not errors and not warnings:
            print("✓ Clean — no errors or warnings.")
        elif not errors:
            print("\n✓ No errors (warnings only).")
        if args.mermaid and by_id:
            print(f"\nMermaid DAG written to {args.mermaid}")

    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
