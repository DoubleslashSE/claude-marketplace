#!/usr/bin/env python3
"""
Stop Hook - Long-Running Workflow Controller

Implements Ralph Wiggum pattern for extended autonomous execution:
- Intercepts Claude's exit attempts
- Checks for workflow completion markers
- Blocks exit if workflow is incomplete, providing context to continue
- Allows exit only when WORKFLOW_COMPLETE is detected or max iterations reached

This enables workflows to run for hours, iterating until the goal is achieved.

Usage in settings.json:
{
  "hooks": {
    "Stop": [{
      "matcher": ".*",
      "hooks": [{
        "type": "command",
        "command": "python .claude/hooks/stop.py"
      }]
    }]
  }
}
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path

# Resolve paths relative to this script
SCRIPT_DIR = Path(__file__).parent.resolve()
CLAUDE_DIR = SCRIPT_DIR.parent
STATE_FILE = CLAUDE_DIR / 'workflow-state.json'
ITERATION_FILE = CLAUDE_DIR / '.iteration-count'
PROGRESS_FILE = CLAUDE_DIR / 'claude-progress.txt'

# Completion markers that signal workflow is done
COMPLETION_MARKERS = [
    'WORKFLOW_COMPLETE',
    '## WORKFLOW_COMPLETE',
    '<promise>COMPLETE</promise>',
    'PR created. Workflow complete.',
    'All stories verified. Pull request created.',
]

# Default max iterations (safety limit)
DEFAULT_MAX_ITERATIONS = 100

# Blockers that should allow exit (escalation needed)
ESCALATION_MARKERS = [
    'BLOCKER:',
    'ESCALATION_REQUIRED',
    'HUMAN_INTERVENTION_NEEDED',
    'MAX_RETRIES_EXCEEDED',
]


def load_state():
    """Load workflow state if it exists."""
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding='utf-8'))
        except (json.JSONDecodeError, IOError):
            pass
    return None


def get_iteration_count():
    """Get current iteration count."""
    if ITERATION_FILE.exists():
        try:
            return int(ITERATION_FILE.read_text(encoding='utf-8').strip())
        except (ValueError, IOError):
            pass
    return 0


def increment_iteration():
    """Increment and save iteration count."""
    count = get_iteration_count() + 1
    try:
        ITERATION_FILE.write_text(str(count), encoding='utf-8')
    except IOError:
        pass
    return count


def reset_iterations():
    """Reset iteration count (on workflow completion)."""
    try:
        if ITERATION_FILE.exists():
            ITERATION_FILE.unlink()
    except IOError:
        pass


def log_progress(message):
    """Log to progress file."""
    try:
        PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(PROGRESS_FILE, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] [STOP_HOOK] {message}\n")
    except IOError:
        pass


def check_completion(stop_hook_data):
    """
    Check if the workflow is complete.

    Returns:
        (is_complete: bool, reason: str)
    """
    # Get transcript/output from stop hook data
    transcript = stop_hook_data.get('transcript', '')
    last_output = stop_hook_data.get('lastAssistantMessage', '')

    # Check for completion markers in recent output
    combined = f"{transcript}\n{last_output}"

    for marker in COMPLETION_MARKERS:
        if marker in combined:
            return True, f"Completion marker found: {marker}"

    # Check workflow state for completion
    state = load_state()
    if state:
        if state.get('status') == 'completed':
            return True, "Workflow state is 'completed'"

        # Check if all stories are completed
        stories = state.get('stories', [])
        if stories:
            all_done = all(s.get('status') == 'completed' for s in stories)
            if all_done:
                return True, "All stories marked as completed"

    # Check for escalation markers (allow exit for human intervention)
    for marker in ESCALATION_MARKERS:
        if marker in combined:
            return True, f"Escalation required: {marker}"

    return False, "Workflow incomplete"


def get_continuation_context():
    """Get context for continuing the workflow."""
    state = load_state()
    iteration = get_iteration_count()

    context_lines = [
        "",
        "=" * 60,
        "WORKFLOW CONTINUATION (Stop Hook Triggered)",
        "=" * 60,
        f"Iteration: {iteration}",
    ]

    if state:
        context_lines.append(f"Goal: {state.get('goal', 'Unknown')}")
        context_lines.append(f"Phase: {state.get('currentPhase', 'Unknown')}")

        stories = state.get('stories', [])
        completed = sum(1 for s in stories if s.get('status') == 'completed')
        in_progress = [s for s in stories if s.get('status') in ['in_progress', 'testing', 'review']]
        pending = [s for s in stories if s.get('status') == 'pending']

        context_lines.append(f"Progress: {completed}/{len(stories)} stories completed")

        if in_progress:
            current = in_progress[0]
            context_lines.append(f"\nCURRENT STORY: [{current['id']}] {current['title']}")
            context_lines.append(f"Status: {current['status']}")
            context_lines.append(f"Attempts: {current.get('attempts', 0)}")

            checks = current.get('verificationChecks', {})
            if checks:
                checks_str = ', '.join(f"{k}={'PASS' if v else 'PENDING'}" for k, v in checks.items())
                context_lines.append(f"Verification: {checks_str}")

        if pending:
            context_lines.append(f"\nNEXT: [{pending[0]['id']}] {pending[0]['title']}")

        blockers = [b for b in state.get('blockers', []) if not b.get('resolved')]
        if blockers:
            context_lines.append("\nBLOCKERS:")
            for b in blockers:
                context_lines.append(f"  - [{b.get('severity', 'medium')}] {b['description']}")

    context_lines.extend([
        "",
        "INSTRUCTIONS:",
        "1. The workflow is NOT complete. Continue from where you left off.",
        "2. Check current story status and continue implementation/verification.",
        "3. Run build and tests before marking any story complete.",
        "4. Output WORKFLOW_COMPLETE only when ALL stories are verified and PR is created.",
        "",
        "Run: python .claude/core/state.py status",
        "=" * 60,
    ])

    return '\n'.join(context_lines)


def main():
    """
    Main stop hook entry point.

    Per Ralph Wiggum pattern:
    - If workflow is complete, allow exit
    - If not complete, block exit and provide continuation context
    """
    try:
        input_data = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        # Can't parse input - allow exit to prevent infinite loop
        print(json.dumps({'decision': 'allow'}))
        return

    # Get max iterations from environment or use default
    max_iterations = int(os.environ.get('MAX_WORKFLOW_ITERATIONS', DEFAULT_MAX_ITERATIONS))

    # Increment iteration counter
    iteration = increment_iteration()

    # Safety check: allow exit if max iterations reached
    if iteration >= max_iterations:
        log_progress(f"Max iterations ({max_iterations}) reached - allowing exit")
        reset_iterations()
        print(json.dumps({
            'decision': 'allow',
            'reason': f'Max iterations ({max_iterations}) reached - safety exit'
        }))
        return

    # Check if workflow is complete
    is_complete, reason = check_completion(input_data)

    if is_complete:
        log_progress(f"Workflow complete: {reason}")
        reset_iterations()
        print(json.dumps({
            'decision': 'allow',
            'reason': reason
        }))
    else:
        log_progress(f"Iteration {iteration}: Blocking exit - {reason}")

        # Get continuation context
        context = get_continuation_context()

        # Block exit and provide continuation context
        # The 'block' decision tells Claude Code to continue with the provided prompt
        print(json.dumps({
            'decision': 'block',
            'reason': f'Workflow incomplete (iteration {iteration}/{max_iterations})',
            'continuePrompt': context
        }))


if __name__ == '__main__':
    main()
