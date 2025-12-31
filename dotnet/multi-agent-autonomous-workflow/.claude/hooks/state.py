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


def initialize_workflow(goal: str, session_id: str = None) -> Dict[str, Any]:
    """Initialize a new workflow or return existing if active."""
    existing = load_state()
    if existing and existing.get('status') == 'in_progress':
        # Resume existing workflow
        existing['sessionId'] = session_id or existing.get('sessionId')
        save_state(existing)
        return existing

    # Create new workflow
    state = create_initial_state(goal, session_id)
    save_state(state)
    return state


def add_story(
    title: str,
    size: str = 'M',
    acceptance_criteria: List[str] = None
) -> str:
    """Add a new story to the workflow. Returns story ID."""
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
        'assignedAgent': None,
        'attempts': 0,
        'createdAt': now_iso(),
        'lastUpdated': now_iso()
    }

    state['stories'].append(story)
    save_state(state)
    return story_id


def update_story_status(
    story_id: str,
    status: str,
    agent: str = None
) -> bool:
    """Update a story's status."""
    state = load_state()
    if not state:
        return False

    for story in state['stories']:
        if story['id'] == story_id:
            story['status'] = status
            story['lastUpdated'] = now_iso()
            if agent:
                story['assignedAgent'] = agent
            if status == 'in_progress':
                story['attempts'] = story.get('attempts', 0) + 1

            # Update checkpoint counter
            if status == 'completed':
                state['checkpoints']['storiesSinceReview'] += 1

            save_state(state)
            return True

    return False


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
    """Mark the workflow as completed."""
    state = load_state()
    if not state:
        return False

    state['status'] = 'completed'
    state['completedAt'] = now_iso()
    save_state(state)
    return True


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
        print('  add-story <title> [--size S|M|L|XL] [--ac "criteria"]')
        print('                                 Add a story to the workflow')
        print('  update-story <id> <status> [--agent name]')
        print('                                 Update story status (pending|in_progress|completed|skipped)')
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

    elif command == 'add-story':
        title = sys.argv[2] if len(sys.argv) > 2 else 'New Story'
        size = 'M'  # Default size
        acceptance_criteria = []

        # Parse optional arguments
        for i, arg in enumerate(sys.argv):
            if arg == '--size' and i + 1 < len(sys.argv):
                size = sys.argv[i + 1].upper()
            elif arg == '--ac' and i + 1 < len(sys.argv):
                acceptance_criteria.append(sys.argv[i + 1])

        story_id = add_story(title, size, acceptance_criteria if acceptance_criteria else None)
        print(f'Added story: {story_id} (size: {size})')

    elif command == 'update-story':
        story_id = sys.argv[2] if len(sys.argv) > 2 else 'S1'
        status = sys.argv[3] if len(sys.argv) > 3 else 'completed'
        agent = None
        for i, arg in enumerate(sys.argv):
            if arg == '--agent' and i + 1 < len(sys.argv):
                agent = sys.argv[i + 1]
        update_story_status(story_id, status, agent)
        print(f'Updated {story_id} to {status}')

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
