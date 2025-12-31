#!/usr/bin/env python3
"""
Workflow State Management

Provides utilities for managing workflow state across sessions:
- Load/save workflow state
- Update story status
- Track checkpoints
- Validate state consistency

State file: .claude/workflow-state.json
"""

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, List, Dict, Any


STATE_FILE = Path('.claude/workflow-state.json')
PROGRESS_FILE = Path('.claude/claude-progress.txt')


def generate_workflow_id() -> str:
    """Generate a unique workflow ID."""
    return str(uuid.uuid4())[:8]


def now_iso() -> str:
    """Get current timestamp in ISO format."""
    return datetime.now(timezone.utc).isoformat()


def create_initial_state(goal: str, session_id: str = None) -> Dict[str, Any]:
    """Create a new workflow state."""
    return {
        'workflowId': generate_workflow_id(),
        'sessionId': session_id or 'unknown',
        'startedAt': now_iso(),
        'lastUpdated': now_iso(),
        'goal': goal,
        'status': 'in_progress',
        'currentPhase': 'analysis',
        'currentAgent': 'orchestrator',
        'stories': [],
        'decisions': [],
        'checkpoints': {
            'lastHumanReview': now_iso(),
            'storiesSinceReview': 0,
            'failedAttempts': 0
        },
        'blockers': [],
        'timeouts': {
            'storyMaxMinutes': 30,
            'iterationMaxMinutes': 10
        }
    }


def load_state() -> Optional[Dict[str, Any]]:
    """Load workflow state from file."""
    if not STATE_FILE.exists():
        return None
    try:
        return json.loads(STATE_FILE.read_text(encoding='utf-8'))
    except (json.JSONDecodeError, IOError):
        return None


def save_state(state: Dict[str, Any]) -> bool:
    """Save workflow state to file."""
    state['lastUpdated'] = now_iso()
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    try:
        STATE_FILE.write_text(json.dumps(state, indent=2), encoding='utf-8')
        return True
    except IOError:
        return False


def log_progress(message: str, story_id: str = None, agent: str = None) -> None:
    """
    Log progress to claude-progress.txt for session recovery.

    This file enables agents to quickly understand project state when
    starting fresh sessions, as recommended by Anthropic best practices.
    """
    PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    prefix = f"[{timestamp}]"
    if story_id:
        prefix += f" [{story_id}]"
    if agent:
        prefix += f" [{agent}]"

    entry = f"{prefix} {message}\n"

    try:
        with open(PROGRESS_FILE, 'a', encoding='utf-8') as f:
            f.write(entry)
    except IOError:
        pass  # Don't block on progress logging failures


def get_recent_progress(lines: int = 20) -> List[str]:
    """Get recent progress entries for session recovery."""
    if not PROGRESS_FILE.exists():
        return []

    try:
        content = PROGRESS_FILE.read_text(encoding='utf-8')
        all_lines = content.strip().split('\n')
        return all_lines[-lines:] if len(all_lines) > lines else all_lines
    except IOError:
        return []


def clear_progress() -> bool:
    """Clear progress file (typically on workflow completion)."""
    try:
        if PROGRESS_FILE.exists():
            # Archive to progress.old before clearing
            archive = Path('.claude/claude-progress.old')
            PROGRESS_FILE.rename(archive)
        return True
    except IOError:
        return False


def initialize_workflow(goal: str, session_id: str = None) -> Dict[str, Any]:
    """Initialize a new workflow or return existing if active."""
    existing = load_state()
    if existing and existing.get('status') == 'in_progress':
        # Resume existing workflow
        existing['sessionId'] = session_id or existing.get('sessionId')
        save_state(existing)
        log_progress(f"RESUMED workflow {existing['workflowId']} - Goal: {existing['goal']}")
        return existing

    # Create new workflow
    state = create_initial_state(goal, session_id)
    save_state(state)
    log_progress(f"STARTED workflow {state['workflowId']} - Goal: {goal}")
    return state


def add_story(
    title: str,
    size: str = 'M',
    acceptance_criteria: List[str] = None,
    security_sensitive: bool = False
) -> str:
    """
    Add a new story to the workflow. Returns story ID.

    Stories start as 'pending' and must go through 'verified' state
    before being marked 'completed' (fail-first pattern per Anthropic best practices).
    """
    state = load_state()
    if not state:
        raise ValueError('No active workflow. Call initialize_workflow first.')

    story_num = len(state['stories']) + 1
    story_id = f'S{story_num}'

    story = {
        'id': story_id,
        'title': title,
        'size': size,
        'status': 'pending',
        'acceptanceCriteria': acceptance_criteria or [],
        'securitySensitive': security_sensitive,
        'assignedAgent': None,
        'attempts': 0,
        'verificationChecks': {
            'testsPass': False,
            'coverageMet': False,
            'reviewApproved': False,
            'securityCleared': not security_sensitive  # Auto-clear if not sensitive
        },
        'createdAt': now_iso(),
        'lastUpdated': now_iso()
    }

    state['stories'].append(story)
    save_state(state)
    log_progress(f"Added story: {title} (size: {size})", story_id=story_id)
    return story_id


def update_story_status(
    story_id: str,
    status: str,
    agent: str = None
) -> bool:
    """
    Update a story's status.

    Valid statuses (in order):
    - pending: Not yet started
    - in_progress: Being implemented
    - testing: Implementation done, under test verification
    - review: Tests pass, under code review
    - verified: All checks passed, ready to mark complete
    - completed: Fully done and verified
    - blocked: Cannot proceed
    - skipped: Intentionally skipped
    """
    valid_statuses = ['pending', 'in_progress', 'testing', 'review', 'verified', 'completed', 'blocked', 'skipped']
    if status not in valid_statuses:
        return False

    state = load_state()
    if not state:
        return False

    for story in state['stories']:
        if story['id'] == story_id:
            old_status = story['status']
            story['status'] = status
            story['lastUpdated'] = now_iso()
            if agent:
                story['assignedAgent'] = agent
            if status == 'in_progress':
                story['attempts'] = story.get('attempts', 0) + 1

            # Update checkpoint counter only when fully completed
            if status == 'completed':
                # Enforce fail-first: must be verified before completed
                checks = story.get('verificationChecks', {})
                if not all([checks.get('testsPass'), checks.get('coverageMet'), checks.get('reviewApproved')]):
                    # If not all verified, force to verified status first
                    story['status'] = 'verified'
                    log_progress(f"Status: {old_status} -> verified (awaiting all checks)", story_id=story_id, agent=agent)
                else:
                    story['completedAt'] = now_iso()
                    state['checkpoints']['storiesSinceReview'] += 1
                    log_progress(f"COMPLETED - all verification checks passed", story_id=story_id, agent=agent)
            else:
                log_progress(f"Status: {old_status} -> {status}", story_id=story_id, agent=agent)

            save_state(state)
            return True

    return False


def update_verification_check(
    story_id: str,
    check_name: str,
    passed: bool,
    details: str = None
) -> bool:
    """
    Update a verification check for a story (fail-first pattern).

    Check names: testsPass, coverageMet, reviewApproved, securityCleared
    All checks must pass before a story can be marked completed.
    """
    valid_checks = ['testsPass', 'coverageMet', 'reviewApproved', 'securityCleared']
    if check_name not in valid_checks:
        return False

    state = load_state()
    if not state:
        return False

    for story in state['stories']:
        if story['id'] == story_id:
            if 'verificationChecks' not in story:
                story['verificationChecks'] = {
                    'testsPass': False,
                    'coverageMet': False,
                    'reviewApproved': False,
                    'securityCleared': not story.get('securitySensitive', False)
                }

            story['verificationChecks'][check_name] = passed
            story['lastUpdated'] = now_iso()

            status_str = "PASSED" if passed else "FAILED"
            detail_str = f" - {details}" if details else ""
            log_progress(f"Verification {check_name}: {status_str}{detail_str}", story_id=story_id)

            # Check if all verifications passed
            checks = story['verificationChecks']
            all_passed = all([
                checks.get('testsPass'),
                checks.get('coverageMet'),
                checks.get('reviewApproved'),
                checks.get('securityCleared', True)
            ])

            if all_passed and story['status'] not in ['completed', 'verified']:
                story['status'] = 'verified'
                log_progress("All verification checks PASSED - ready for completion", story_id=story_id)

            save_state(state)
            return True

    return False


def get_verification_status(story_id: str) -> Dict[str, Any]:
    """Get verification status for a story."""
    state = load_state()
    if not state:
        return {'error': 'No active workflow'}

    for story in state['stories']:
        if story['id'] == story_id:
            checks = story.get('verificationChecks', {})
            return {
                'story_id': story_id,
                'status': story['status'],
                'checks': checks,
                'all_passed': all([
                    checks.get('testsPass'),
                    checks.get('coverageMet'),
                    checks.get('reviewApproved'),
                    checks.get('securityCleared', True)
                ]),
                'pending_checks': [k for k, v in checks.items() if not v]
            }

    return {'error': f'Story {story_id} not found'}


def update_phase(phase: str, agent: str = None) -> bool:
    """Update the current workflow phase."""
    state = load_state()
    if not state:
        return False

    state['currentPhase'] = phase
    if agent:
        state['currentAgent'] = agent
    save_state(state)
    return True


def add_decision(title: str, choice: str, rationale: str) -> str:
    """Record an architecture decision."""
    state = load_state()
    if not state:
        raise ValueError('No active workflow.')

    decision_num = len(state['decisions']) + 1
    decision_id = f'ADR-{decision_num:03d}'

    decision = {
        'id': decision_id,
        'title': title,
        'choice': choice,
        'rationale': rationale,
        'date': datetime.now().strftime('%Y-%m-%d'),
        'status': 'accepted'
    }

    state['decisions'].append(decision)
    save_state(state)
    return decision_id


def add_blocker(description: str, severity: str = 'medium') -> None:
    """Add a blocker to the workflow."""
    state = load_state()
    if not state:
        return

    blocker = {
        'description': description,
        'severity': severity,
        'createdAt': now_iso(),
        'resolved': False
    }

    state['blockers'].append(blocker)
    state['status'] = 'blocked'
    save_state(state)
    log_progress(f"BLOCKER [{severity.upper()}]: {description}")


def resolve_blocker(index: int) -> bool:
    """Resolve a blocker by index."""
    state = load_state()
    if not state or index >= len(state['blockers']):
        return False

    state['blockers'][index]['resolved'] = True
    state['blockers'][index]['resolvedAt'] = now_iso()

    # Check if any unresolved blockers remain
    if not any(b for b in state['blockers'] if not b['resolved']):
        state['status'] = 'in_progress'

    save_state(state)
    return True


def should_checkpoint() -> bool:
    """Check if human review checkpoint is needed."""
    state = load_state()
    if not state:
        return False

    checkpoints = state.get('checkpoints', {})
    return checkpoints.get('storiesSinceReview', 0) >= 5


def record_human_review() -> None:
    """Record that a human review checkpoint occurred."""
    state = load_state()
    if not state:
        return

    state['checkpoints']['lastHumanReview'] = now_iso()
    state['checkpoints']['storiesSinceReview'] = 0
    save_state(state)


def set_timeout(story_minutes: int = None, iteration_minutes: int = None) -> bool:
    """Set timeout limits for stories and iterations."""
    state = load_state()
    if not state:
        return False

    if 'timeouts' not in state:
        state['timeouts'] = {'storyMaxMinutes': 30, 'iterationMaxMinutes': 10}

    if story_minutes is not None:
        state['timeouts']['storyMaxMinutes'] = story_minutes
    if iteration_minutes is not None:
        state['timeouts']['iterationMaxMinutes'] = iteration_minutes

    save_state(state)
    return True


def get_timeout() -> Dict[str, int]:
    """Get current timeout settings."""
    state = load_state()
    if not state:
        return {'storyMaxMinutes': 30, 'iterationMaxMinutes': 10}

    return state.get('timeouts', {'storyMaxMinutes': 30, 'iterationMaxMinutes': 10})


def check_story_timeout(story_id: str) -> Dict[str, Any]:
    """Check if a story has exceeded its timeout.

    Returns dict with:
    - exceeded: bool
    - elapsed_minutes: float
    - max_minutes: int
    - story_id: str
    """
    state = load_state()
    if not state:
        return {'exceeded': False, 'error': 'No active workflow'}

    timeouts = state.get('timeouts', {'storyMaxMinutes': 30})
    max_minutes = timeouts.get('storyMaxMinutes', 30)

    for story in state.get('stories', []):
        if story['id'] == story_id and story['status'] == 'in_progress':
            started = datetime.fromisoformat(story['lastUpdated'].replace('Z', '+00:00'))
            now = datetime.now(timezone.utc)
            elapsed = (now - started).total_seconds() / 60

            return {
                'exceeded': elapsed > max_minutes,
                'elapsed_minutes': round(elapsed, 1),
                'max_minutes': max_minutes,
                'story_id': story_id
            }

    return {'exceeded': False, 'story_id': story_id, 'error': 'Story not in progress'}


def complete_workflow() -> bool:
    """Mark the workflow as completed and archive progress file."""
    state = load_state()
    if not state:
        return False

    state['status'] = 'completed'
    state['completedAt'] = now_iso()
    save_state(state)

    # Log completion and archive progress
    stories = state.get('stories', [])
    completed = sum(1 for s in stories if s['status'] == 'completed')
    log_progress(f"WORKFLOW COMPLETED - {completed}/{len(stories)} stories done")
    clear_progress()  # Archive progress file

    return True


def get_session_recovery_info() -> Dict[str, Any]:
    """
    Get session recovery information per Anthropic best practices.

    This enables agents to quickly understand project state when
    starting fresh sessions.
    """
    state = load_state()
    recent_progress = get_recent_progress(15)

    if not state:
        return {
            'has_active_workflow': False,
            'recent_progress': recent_progress
        }

    stories = state.get('stories', [])
    current_story = next(
        (s for s in stories if s['status'] in ['in_progress', 'testing', 'review']),
        None
    )
    pending_stories = [s for s in stories if s['status'] == 'pending']
    verified_stories = [s for s in stories if s['status'] == 'verified']

    return {
        'has_active_workflow': True,
        'workflow_id': state.get('workflowId'),
        'goal': state.get('goal'),
        'status': state.get('status'),
        'current_phase': state.get('currentPhase'),
        'current_agent': state.get('currentAgent'),
        'current_story': {
            'id': current_story['id'],
            'title': current_story['title'],
            'status': current_story['status'],
            'attempts': current_story.get('attempts', 0),
            'verification': current_story.get('verificationChecks', {})
        } if current_story else None,
        'next_pending': pending_stories[0]['title'] if pending_stories else None,
        'verified_awaiting_completion': [s['id'] for s in verified_stories],
        'stories_summary': {
            'total': len(stories),
            'completed': sum(1 for s in stories if s['status'] == 'completed'),
            'verified': len(verified_stories),
            'in_progress': sum(1 for s in stories if s['status'] in ['in_progress', 'testing', 'review']),
            'pending': len(pending_stories)
        },
        'blockers': [b for b in state.get('blockers', []) if not b['resolved']],
        'checkpoint_due': should_checkpoint(),
        'recent_progress': recent_progress
    }


def get_workflow_summary() -> Dict[str, Any]:
    """Get a summary of the current workflow state."""
    state = load_state()
    if not state:
        return {'error': 'No active workflow'}

    stories = state.get('stories', [])
    completed = sum(1 for s in stories if s['status'] == 'completed')
    in_progress = sum(1 for s in stories if s['status'] == 'in_progress')
    pending = sum(1 for s in stories if s['status'] == 'pending')

    return {
        'workflowId': state.get('workflowId'),
        'goal': state.get('goal'),
        'status': state.get('status'),
        'currentPhase': state.get('currentPhase'),
        'currentAgent': state.get('currentAgent'),
        'progress': {
            'total': len(stories),
            'completed': completed,
            'in_progress': in_progress,
            'pending': pending,
            'percentage': round(completed / len(stories) * 100) if stories else 0
        },
        'checkpointDue': should_checkpoint(),
        'blockers': [b for b in state.get('blockers', []) if not b['resolved']]
    }


# CLI interface for testing
if __name__ == '__main__':
    import sys
    import argparse

    if len(sys.argv) < 2:
        print('Usage: python state.py <command> [args]')
        print('')
        print('Commands:')
        print('  init <goal> [--session ID]     Initialize or resume workflow')
        print('  status                         Show workflow summary')
        print('  recover                        Get session recovery info (for fresh sessions)')
        print('  add-story <title> [--size S|M|L|XL] [--ac "criteria"] [--security]')
        print('                                 Add a story to the workflow')
        print('  update-story <id> <status> [--agent name]')
        print('                                 Update story status (pending|in_progress|testing|')
        print('                                 review|verified|completed|blocked|skipped)')
        print('  verify <story_id> <check> [--passed] [--failed] [--details "msg"]')
        print('                                 Update verification check (testsPass|coverageMet|')
        print('                                 reviewApproved|securityCleared)')
        print('  verify-status <story_id>       Get verification status for a story')
        print('  add-blocker <desc> [--severity low|medium|high|critical]')
        print('                                 Add a blocker (pauses workflow)')
        print('  resolve-blocker <index>        Resolve blocker by index')
        print('  add-decision <title> <choice> <rationale>')
        print('                                 Record an architecture decision')
        print('  checkpoint                     Check if human review is due (exit 2 if due)')
        print('  record-review                  Record that human review occurred')
        print('  set-timeout <mins> [--story M] [--iteration M]')
        print('                                 Set timeout limits (default: story=30, iteration=10)')
        print('  check-timeout <story_id>       Check if story exceeded timeout (exit 3 if exceeded)')
        print('  progress [--lines N]           Show recent progress log entries')
        print('  complete                       Mark workflow as completed')
        print('')
        print('Exit codes: 0=success, 1=error, 2=checkpoint due, 3=blocked')
        sys.exit(1)

    command = sys.argv[1]

    if command == 'init':
        goal = sys.argv[2] if len(sys.argv) > 2 else 'Test workflow'
        session_id = None
        for i, arg in enumerate(sys.argv):
            if arg == '--session' and i + 1 < len(sys.argv):
                session_id = sys.argv[i + 1]
        state = initialize_workflow(goal, session_id)
        print(f'Initialized workflow: {state["workflowId"]}')
        if state.get('stories'):
            print(f'Resuming with {len(state["stories"])} existing stories')

    elif command == 'status':
        summary = get_workflow_summary()
        print(json.dumps(summary, indent=2))

    elif command == 'recover':
        recovery = get_session_recovery_info()
        print(json.dumps(recovery, indent=2))

    elif command == 'add-story':
        title = sys.argv[2] if len(sys.argv) > 2 else 'New Story'
        size = 'M'  # Default size
        acceptance_criteria = []
        security_sensitive = False

        # Parse optional arguments
        for i, arg in enumerate(sys.argv):
            if arg == '--size' and i + 1 < len(sys.argv):
                size = sys.argv[i + 1].upper()
            elif arg == '--ac' and i + 1 < len(sys.argv):
                acceptance_criteria.append(sys.argv[i + 1])
            elif arg == '--security':
                security_sensitive = True

        story_id = add_story(title, size, acceptance_criteria if acceptance_criteria else None, security_sensitive)
        security_flag = ' [SECURITY]' if security_sensitive else ''
        print(f'Added story: {story_id} (size: {size}){security_flag}')

    elif command == 'update-story':
        story_id = sys.argv[2] if len(sys.argv) > 2 else 'S1'
        status = sys.argv[3] if len(sys.argv) > 3 else 'completed'
        agent = None
        for i, arg in enumerate(sys.argv):
            if arg == '--agent' and i + 1 < len(sys.argv):
                agent = sys.argv[i + 1]
        if update_story_status(story_id, status, agent):
            print(f'Updated {story_id} to {status}')
        else:
            print(f'Failed to update {story_id} (invalid status or story not found)')
            sys.exit(1)

    elif command == 'verify':
        story_id = sys.argv[2] if len(sys.argv) > 2 else 'S1'
        check_name = sys.argv[3] if len(sys.argv) > 3 else 'testsPass'
        passed = True  # Default to passed
        details = None
        for i, arg in enumerate(sys.argv):
            if arg == '--failed':
                passed = False
            elif arg == '--passed':
                passed = True
            elif arg == '--details' and i + 1 < len(sys.argv):
                details = sys.argv[i + 1]
        if update_verification_check(story_id, check_name, passed, details):
            status = 'PASSED' if passed else 'FAILED'
            print(f'Verification {check_name} for {story_id}: {status}')
        else:
            print(f'Failed to update verification (invalid check or story not found)')
            sys.exit(1)

    elif command == 'verify-status':
        story_id = sys.argv[2] if len(sys.argv) > 2 else 'S1'
        result = get_verification_status(story_id)
        print(json.dumps(result, indent=2))

    elif command == 'progress':
        lines = 20
        for i, arg in enumerate(sys.argv):
            if arg == '--lines' and i + 1 < len(sys.argv):
                lines = int(sys.argv[i + 1])
        entries = get_recent_progress(lines)
        if entries:
            for entry in entries:
                print(entry)
        else:
            print('No progress entries found')

    elif command == 'add-blocker':
        description = sys.argv[2] if len(sys.argv) > 2 else 'Unknown blocker'
        severity = 'medium'
        for i, arg in enumerate(sys.argv):
            if arg == '--severity' and i + 1 < len(sys.argv):
                severity = sys.argv[i + 1]
        add_blocker(description, severity)
        print(f'Added blocker: {description} (severity: {severity})')

    elif command == 'resolve-blocker':
        index = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        resolve_blocker(index)
        print(f'Resolved blocker at index {index}')

    elif command == 'add-decision':
        title = sys.argv[2] if len(sys.argv) > 2 else 'Decision'
        choice = sys.argv[3] if len(sys.argv) > 3 else 'TBD'
        rationale = sys.argv[4] if len(sys.argv) > 4 else 'No rationale provided'
        decision_id = add_decision(title, choice, rationale)
        print(f'Added decision: {decision_id}')

    elif command == 'checkpoint':
        if should_checkpoint():
            print('CHECKPOINT_DUE: Human review recommended')
            sys.exit(2)  # Special exit code for checkpoint
        else:
            print('No checkpoint needed')

    elif command == 'record-review':
        record_human_review()
        print('Recorded human review checkpoint')

    elif command == 'set-timeout':
        story_mins = None
        iteration_mins = None
        # Parse positional or flag arguments
        if len(sys.argv) > 2:
            story_mins = int(sys.argv[2])
        for i, arg in enumerate(sys.argv):
            if arg == '--story' and i + 1 < len(sys.argv):
                story_mins = int(sys.argv[i + 1])
            elif arg == '--iteration' and i + 1 < len(sys.argv):
                iteration_mins = int(sys.argv[i + 1])
        set_timeout(story_mins, iteration_mins)
        timeouts = get_timeout()
        print(f'Timeouts set: story={timeouts["storyMaxMinutes"]}min, iteration={timeouts["iterationMaxMinutes"]}min')

    elif command == 'check-timeout':
        story_id = sys.argv[2] if len(sys.argv) > 2 else 'S1'
        result = check_story_timeout(story_id)
        if result.get('exceeded'):
            print(f'TIMEOUT: {story_id} exceeded {result["max_minutes"]}min (elapsed: {result["elapsed_minutes"]}min)')
            sys.exit(3)  # Blocked exit code
        elif result.get('error'):
            print(f'{story_id}: {result["error"]}')
        else:
            print(f'{story_id}: {result["elapsed_minutes"]}min / {result["max_minutes"]}min')

    elif command == 'complete':
        complete_workflow()
        print('Workflow completed')

    else:
        print(f'Unknown command: {command}')
        sys.exit(1)
