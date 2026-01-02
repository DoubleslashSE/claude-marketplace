#!/usr/bin/env python3
"""
Workflow State Management - Minimal Core

Essential infrastructure for long-running autonomous workflows:
- State persistence (survive interruptions)
- Story tracking (pending → in_progress → completed)
- Verification gates (build/test must pass)
- Blockers and escalation
- User intervention (pause for human action)
- Session recovery

Everything else is handled by agent reasoning.

State file: .claude/workflow-state.json
Progress file: .claude/claude-progress.txt
"""

import json
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, List, Dict, Any


# Paths
SCRIPT_DIR = Path(__file__).parent.resolve()
CLAUDE_DIR = SCRIPT_DIR.parent
PROJECT_ROOT = CLAUDE_DIR.parent
STATE_FILE = CLAUDE_DIR / 'workflow-state.json'
PROGRESS_FILE = CLAUDE_DIR / 'claude-progress.txt'
ITERATION_FILE = CLAUDE_DIR / '.iteration-count'


# =============================================================================
# Utilities
# =============================================================================

def generate_workflow_id() -> str:
    return str(uuid.uuid4())[:8]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def get_elapsed_time(start_iso: str) -> str:
    try:
        start = datetime.fromisoformat(start_iso.replace('Z', '+00:00'))
        elapsed = datetime.now(timezone.utc) - start
        hours = int(elapsed.total_seconds() // 3600)
        minutes = int((elapsed.total_seconds() % 3600) // 60)
        return f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"
    except:
        return "unknown"


# =============================================================================
# Iteration Tracking (Stop Hook Integration)
# =============================================================================

def get_iteration_count() -> int:
    if ITERATION_FILE.exists():
        try:
            return int(ITERATION_FILE.read_text(encoding='utf-8').strip())
        except (ValueError, IOError):
            pass
    return 0


def increment_iteration() -> int:
    count = get_iteration_count() + 1
    try:
        ITERATION_FILE.write_text(str(count), encoding='utf-8')
    except IOError:
        pass
    return count


def reset_iterations() -> None:
    try:
        if ITERATION_FILE.exists():
            ITERATION_FILE.unlink()
    except IOError:
        pass


# =============================================================================
# State Persistence
# =============================================================================

def load_state() -> Optional[Dict[str, Any]]:
    if not STATE_FILE.exists():
        return None
    try:
        return json.loads(STATE_FILE.read_text(encoding='utf-8'))
    except (json.JSONDecodeError, IOError):
        return None


def save_state(state: Dict[str, Any]) -> bool:
    try:
        state['lastUpdated'] = now_iso()
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        STATE_FILE.write_text(json.dumps(state, indent=2), encoding='utf-8')
        return True
    except IOError:
        return False


def create_initial_state(goal: str) -> Dict[str, Any]:
    return {
        'workflowId': generate_workflow_id(),
        'startedAt': now_iso(),
        'lastUpdated': now_iso(),
        'goal': goal,
        'status': 'in_progress',  # in_progress | awaiting_user | completed
        'currentPhase': 'analysis',
        'stories': [],
        'blockers': [],
        'userIntervention': None,
        'metrics': {
            'storiesCompleted': 0,
            'totalAttempts': 0
        }
    }


# =============================================================================
# Workflow Lifecycle
# =============================================================================

def initialize_workflow(goal: str) -> Dict[str, Any]:
    state = create_initial_state(goal)
    save_state(state)
    log_progress(f"Workflow initialized: {goal}")
    return state


def complete_workflow() -> bool:
    state = load_state()
    if not state:
        return False
    state['status'] = 'completed'
    state['completedAt'] = now_iso()
    reset_iterations()
    log_progress("Workflow completed")
    return save_state(state)


def update_phase(phase: str) -> bool:
    state = load_state()
    if not state:
        return False
    state['currentPhase'] = phase
    log_progress(f"Phase: {phase}")
    return save_state(state)


# =============================================================================
# Story Management
# =============================================================================

def add_story(title: str, size: str = 'M', security_sensitive: bool = False) -> str:
    state = load_state()
    if not state:
        return None

    story_num = len(state['stories']) + 1
    story_id = f"S{story_num}"

    story = {
        'id': story_id,
        'title': title,
        'size': size.upper(),
        'securitySensitive': security_sensitive,
        'status': 'pending',  # pending | in_progress | completed | blocked
        'attempts': 0,
        'verificationChecks': {
            'buildPasses': False,
            'testsPasses': False,
            'reviewApproved': False
        },
        'createdAt': now_iso()
    }

    state['stories'].append(story)
    save_state(state)
    log_progress(f"Added story: [{story_id}] {title}", story_id=story_id)
    return story_id


def update_story_status(story_id: str, status: str) -> bool:
    state = load_state()
    if not state:
        return False

    for story in state['stories']:
        if story['id'] == story_id:
            old_status = story['status']
            story['status'] = status
            story['lastUpdated'] = now_iso()

            if status == 'in_progress':
                story['attempts'] = story.get('attempts', 0) + 1
                state['metrics']['totalAttempts'] += 1
            elif status == 'completed':
                state['metrics']['storiesCompleted'] += 1

            log_progress(f"[{story_id}] {old_status} → {status}", story_id=story_id)
            return save_state(state)

    return False


def update_verification(story_id: str, check: str, passed: bool) -> bool:
    state = load_state()
    if not state:
        return False

    for story in state['stories']:
        if story['id'] == story_id:
            story['verificationChecks'][check] = passed
            status = "PASS" if passed else "FAIL"
            log_progress(f"[{story_id}] {check}: {status}", story_id=story_id)
            return save_state(state)

    return False


def get_next_story() -> Optional[Dict[str, Any]]:
    state = load_state()
    if not state:
        return None

    # First: any in_progress story
    for story in state['stories']:
        if story['status'] == 'in_progress':
            return story

    # Next: first pending story
    for story in state['stories']:
        if story['status'] == 'pending':
            return story

    return None


def get_incomplete_stories() -> List[Dict[str, Any]]:
    state = load_state()
    if not state:
        return []
    return [s for s in state['stories'] if s['status'] not in ['completed', 'blocked']]


# =============================================================================
# Blockers
# =============================================================================

def add_blocker(description: str, severity: str = 'medium') -> int:
    state = load_state()
    if not state:
        return -1

    blocker = {
        'description': description,
        'severity': severity,
        'createdAt': now_iso(),
        'resolved': False
    }
    state['blockers'].append(blocker)
    index = len(state['blockers']) - 1
    log_progress(f"BLOCKER [{severity}]: {description}")
    save_state(state)
    return index


def resolve_blocker(index: int) -> bool:
    state = load_state()
    if not state or index >= len(state['blockers']):
        return False

    state['blockers'][index]['resolved'] = True
    state['blockers'][index]['resolvedAt'] = now_iso()
    log_progress(f"Blocker {index} resolved")
    return save_state(state)


# =============================================================================
# User Intervention
# =============================================================================

def await_user_fix(description: str, check_command: str = None) -> Dict[str, Any]:
    """Pause workflow for user intervention. Stop hook will allow exit."""
    state = load_state()
    if not state:
        return {'error': 'No active workflow'}

    state['status'] = 'awaiting_user'
    state['userIntervention'] = {
        'description': description,
        'checkCommand': check_command,
        'requestedAt': now_iso(),
        'resolved': False
    }

    save_state(state)
    log_progress(f"AWAITING USER: {description}")

    return {
        'status': 'awaiting_user',
        'description': description,
        'instructions': [
            f"1. Fix: {description}",
            f"2. Verify: {check_command}" if check_command else "2. Test your fix",
            "3. Resume: python .claude/core/state.py user-fix-complete",
            "4. Restart Claude Code"
        ]
    }


def user_fix_complete(notes: str = None) -> Dict[str, Any]:
    """Signal that user has fixed the issue."""
    state = load_state()
    if not state:
        return {'error': 'No active workflow'}

    if state.get('userIntervention'):
        state['userIntervention']['resolved'] = True
        state['userIntervention']['resolvedAt'] = now_iso()
        state['userIntervention']['notes'] = notes

    state['status'] = 'in_progress'
    save_state(state)
    log_progress(f"User fix complete: {notes or 'No notes'}")

    return {'status': 'resumed', 'notes': notes}


def check_user_intervention() -> Dict[str, Any]:
    """Check if awaiting user intervention."""
    state = load_state()
    if not state:
        return {'awaiting': False}

    if state.get('status') == 'awaiting_user':
        intervention = state.get('userIntervention', {})
        return {
            'awaiting': True,
            'description': intervention.get('description'),
            'checkCommand': intervention.get('checkCommand')
        }

    return {'awaiting': False}


# =============================================================================
# Progress Logging
# =============================================================================

def log_progress(message: str, story_id: str = None) -> None:
    try:
        PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime('%H:%M:%S')
        prefix = f"[{story_id}]" if story_id else ""
        with open(PROGRESS_FILE, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {prefix} {message}\n")
    except IOError:
        pass


def get_progress(lines: int = 50) -> List[str]:
    if not PROGRESS_FILE.exists():
        return []
    try:
        all_lines = PROGRESS_FILE.read_text(encoding='utf-8').strip().split('\n')
        return all_lines[-lines:]
    except IOError:
        return []


# =============================================================================
# Recovery
# =============================================================================

def get_status() -> Dict[str, Any]:
    """Get current workflow status."""
    state = load_state()
    if not state:
        return {'active': False}

    stories = state.get('stories', [])
    completed = sum(1 for s in stories if s['status'] == 'completed')

    return {
        'active': True,
        'workflowId': state.get('workflowId'),
        'goal': state.get('goal'),
        'status': state.get('status'),
        'phase': state.get('currentPhase'),
        'elapsed': get_elapsed_time(state.get('startedAt', '')),
        'stories': f"{completed}/{len(stories)}",
        'nextStory': get_next_story(),
        'blockers': [b for b in state.get('blockers', []) if not b.get('resolved')]
    }


def recover() -> Dict[str, Any]:
    """Check for existing workflow to resume."""
    state = load_state()
    if not state:
        return {'found': False, 'message': 'No existing workflow'}

    if state.get('status') == 'completed':
        return {'found': False, 'message': 'Previous workflow completed'}

    status = get_status()
    log_progress("Session recovered")

    return {
        'found': True,
        'workflowId': state.get('workflowId'),
        'goal': state.get('goal'),
        'phase': state.get('currentPhase'),
        'stories': status['stories'],
        'nextStory': status['nextStory'],
        'message': 'Resuming existing workflow'
    }


# =============================================================================
# Git Recovery (Simple)
# =============================================================================

def _git(args: List[str]) -> Optional[str]:
    try:
        result = subprocess.run(
            ['git'] + args,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True
        )
        return result.stdout.strip() if result.returncode == 0 else None
    except:
        return None


def mark_checkpoint(description: str = "Working state") -> Optional[str]:
    """Create a git commit as checkpoint."""
    _git(['add', '-A'])
    result = _git(['commit', '-m', f"checkpoint: {description}", '--allow-empty'])
    if result is not None:
        commit = _git(['rev-parse', 'HEAD'])
        log_progress(f"Checkpoint: {commit[:8] if commit else 'unknown'}")
        return commit
    return None


def rollback() -> bool:
    """Rollback to last checkpoint."""
    result = _git(['reset', '--hard', 'HEAD~1'])
    if result is not None:
        log_progress("Rolled back to previous checkpoint")
        return True
    return False


# =============================================================================
# CLI Interface
# =============================================================================

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Workflow State Management - Minimal Core")
        print("")
        print("Usage: python state.py <command> [args]")
        print("")
        print("Lifecycle:")
        print("  init <goal>              Initialize new workflow")
        print("  complete                 Mark workflow complete")
        print("  status                   Show current status")
        print("  recover                  Check for workflow to resume")
        print("")
        print("Stories:")
        print("  add-story <title> [--size S|M|L|XL] [--security]")
        print("  update <story_id> <status>   pending|in_progress|completed|blocked")
        print("  verify <story_id> <check> --passed|--failed")
        print("  next                     Get next story to work on")
        print("")
        print("Blockers:")
        print("  blocker <description> [--severity low|medium|high]")
        print("  resolve <index>          Resolve blocker by index")
        print("")
        print("User Intervention:")
        print("  await-user <description> [--check <command>]")
        print("  user-fix-complete [--notes <notes>]")
        print("")
        print("Git:")
        print("  checkpoint [description]  Create git checkpoint")
        print("  rollback                  Rollback to last checkpoint")
        print("")
        sys.exit(0)

    cmd = sys.argv[1]

    # Lifecycle
    if cmd == 'init':
        goal = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else 'Unnamed workflow'
        result = initialize_workflow(goal)
        print(f"Initialized: {result['workflowId']}")

    elif cmd == 'complete':
        if complete_workflow():
            print("Workflow completed")
        else:
            print("Failed to complete workflow", file=sys.stderr)
            sys.exit(1)

    elif cmd == 'status':
        status = get_status()
        if not status['active']:
            print("No active workflow")
        else:
            print(f"Workflow: {status['workflowId']}")
            print(f"Goal: {status['goal']}")
            print(f"Status: {status['status']}")
            print(f"Phase: {status['phase']}")
            print(f"Elapsed: {status['elapsed']}")
            print(f"Stories: {status['stories']}")
            if status['nextStory']:
                ns = status['nextStory']
                print(f"Next: [{ns['id']}] {ns['title']}")
            if status['blockers']:
                print(f"Blockers: {len(status['blockers'])}")

    elif cmd == 'recover':
        result = recover()
        print(json.dumps(result, indent=2))

    # Stories
    elif cmd == 'add-story':
        if len(sys.argv) < 3:
            print("Usage: add-story <title> [--size S|M|L|XL] [--security]", file=sys.stderr)
            sys.exit(1)

        title = sys.argv[2]
        size = 'M'
        security = False

        args = sys.argv[3:]
        for i, arg in enumerate(args):
            if arg == '--size' and i + 1 < len(args):
                size = args[i + 1]
            elif arg == '--security':
                security = True

        story_id = add_story(title, size, security)
        print(f"Added: {story_id}")

    elif cmd == 'update':
        if len(sys.argv) < 4:
            print("Usage: update <story_id> <status>", file=sys.stderr)
            sys.exit(1)
        if update_story_status(sys.argv[2], sys.argv[3]):
            print(f"Updated {sys.argv[2]} → {sys.argv[3]}")
        else:
            print("Update failed", file=sys.stderr)
            sys.exit(1)

    elif cmd == 'verify':
        if len(sys.argv) < 4:
            print("Usage: verify <story_id> <check> --passed|--failed", file=sys.stderr)
            sys.exit(1)
        passed = '--passed' in sys.argv
        if update_verification(sys.argv[2], sys.argv[3], passed):
            print(f"Verified {sys.argv[2]}.{sys.argv[3]}: {'PASS' if passed else 'FAIL'}")
        else:
            print("Verify failed", file=sys.stderr)
            sys.exit(1)

    elif cmd == 'next':
        story = get_next_story()
        if story:
            print(f"[{story['id']}] {story['title']} ({story['status']})")
        else:
            print("No pending stories")

    # Blockers
    elif cmd == 'blocker':
        if len(sys.argv) < 3:
            print("Usage: blocker <description> [--severity low|medium|high]", file=sys.stderr)
            sys.exit(1)
        desc = sys.argv[2]
        severity = 'medium'
        if '--severity' in sys.argv:
            idx = sys.argv.index('--severity')
            if idx + 1 < len(sys.argv):
                severity = sys.argv[idx + 1]
        index = add_blocker(desc, severity)
        print(f"Blocker {index}: {desc}")

    elif cmd == 'resolve':
        if len(sys.argv) < 3:
            print("Usage: resolve <index>", file=sys.stderr)
            sys.exit(1)
        if resolve_blocker(int(sys.argv[2])):
            print(f"Resolved blocker {sys.argv[2]}")
        else:
            print("Resolve failed", file=sys.stderr)
            sys.exit(1)

    # User Intervention
    elif cmd == 'await-user':
        if len(sys.argv) < 3:
            print("Usage: await-user <description> [--check <command>]", file=sys.stderr)
            sys.exit(1)
        desc = sys.argv[2]
        check_cmd = None
        if '--check' in sys.argv:
            idx = sys.argv.index('--check')
            if idx + 1 < len(sys.argv):
                check_cmd = sys.argv[idx + 1]
        result = await_user_fix(desc, check_cmd)
        print(json.dumps(result, indent=2))

    elif cmd == 'user-fix-complete':
        notes = None
        if '--notes' in sys.argv:
            idx = sys.argv.index('--notes')
            if idx + 1 < len(sys.argv):
                notes = sys.argv[idx + 1]
        result = user_fix_complete(notes)
        print(json.dumps(result, indent=2))

    # Git
    elif cmd == 'checkpoint':
        desc = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else 'Working state'
        commit = mark_checkpoint(desc)
        if commit:
            print(f"Checkpoint: {commit[:8]}")
        else:
            print("Checkpoint failed", file=sys.stderr)
            sys.exit(1)

    elif cmd == 'rollback':
        if rollback():
            print("Rolled back")
        else:
            print("Rollback failed", file=sys.stderr)
            sys.exit(1)

    # Progress
    elif cmd == 'progress':
        lines = int(sys.argv[2]) if len(sys.argv) > 2 else 20
        for line in get_progress(lines):
            print(line)

    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        sys.exit(1)
