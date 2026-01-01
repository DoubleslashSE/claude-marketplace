#!/usr/bin/env python3
"""
Workflow State Management - Enhanced for Long-Running Execution

Provides utilities for managing workflow state across extended sessions:
- Load/save workflow state
- Update story status with verification tracking
- Track iterations for Stop hook integration
- Session recovery for interrupted workflows
- Git-based rollback for failed states

State file: .claude/workflow-state.json
Progress file: .claude/claude-progress.txt
Iteration file: .claude/.iteration-count

This version is optimized for the Ralph Wiggum pattern where workflows
run for hours with the Stop hook preventing premature exit.
"""

import json
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, List, Dict, Any


# Resolve paths relative to this script's location
SCRIPT_DIR = Path(__file__).parent.resolve()
CLAUDE_DIR = SCRIPT_DIR.parent  # .claude directory
PROJECT_ROOT = CLAUDE_DIR.parent  # Project root containing .claude

STATE_FILE = CLAUDE_DIR / 'workflow-state.json'
PROGRESS_FILE = CLAUDE_DIR / 'claude-progress.txt'
ITERATION_FILE = CLAUDE_DIR / '.iteration-count'


def generate_workflow_id() -> str:
    """Generate a unique workflow ID."""
    return str(uuid.uuid4())[:8]


def now_iso() -> str:
    """Get current timestamp in ISO format."""
    return datetime.now(timezone.utc).isoformat()


def get_elapsed_time(start_iso: str) -> str:
    """Get elapsed time since start as human-readable string."""
    try:
        start = datetime.fromisoformat(start_iso.replace('Z', '+00:00'))
        elapsed = datetime.now(timezone.utc) - start
        hours = int(elapsed.total_seconds() // 3600)
        minutes = int((elapsed.total_seconds() % 3600) // 60)
        if hours > 0:
            return f"{hours}h {minutes}m"
        return f"{minutes}m"
    except:
        return "unknown"


# ============================================================================
# Iteration Tracking (For Stop Hook Integration)
# ============================================================================

def get_iteration_count() -> int:
    """Get current iteration count for Stop hook."""
    if ITERATION_FILE.exists():
        try:
            return int(ITERATION_FILE.read_text(encoding='utf-8').strip())
        except (ValueError, IOError):
            pass
    return 0


def increment_iteration() -> int:
    """Increment and save iteration count."""
    count = get_iteration_count() + 1
    try:
        ITERATION_FILE.write_text(str(count), encoding='utf-8')
    except IOError:
        pass
    return count


def reset_iterations() -> None:
    """Reset iteration count (on workflow completion)."""
    try:
        if ITERATION_FILE.exists():
            ITERATION_FILE.unlink()
    except IOError:
        pass


# ============================================================================
# State Management
# ============================================================================

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
        'totalIterations': 0,
        'stories': [],
        'decisions': [],
        'clarifications': [],  # Persisted user clarification answers
        'failures': [],  # Categorized failure log
        'checkpoints': {
            'lastHumanReview': now_iso(),
            'storiesSinceReview': 0,
            'lastProgressReport': now_iso(),
            'storiesSinceReport': 0,
            'lastTimeCheck': now_iso()
        },
        'blockers': [],
        'metrics': {
            'storiesCompleted': 0,
            'totalAttempts': 0,
            'failedVerifications': 0,
            'failuresByCategory': {
                'code': 0,
                'test': 0,
                'infra': 0,
                'external': 0,
                'timeout': 0
            }
        },
        'timeouts': {
            'storyMaxMinutes': 30,
            'iterationMaxMinutes': 10,
            'questionTimeoutMinutes': 5
        },
        'alerts': []  # Time-based and iteration alerts
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
    state['totalIterations'] = get_iteration_count()
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    try:
        STATE_FILE.write_text(json.dumps(state, indent=2), encoding='utf-8')
        return True
    except IOError:
        return False


def log_progress(message: str, story_id: str = None, agent: str = None) -> None:
    """Log progress to claude-progress.txt for session recovery."""
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
        pass


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


# ============================================================================
# Clarification Persistence
# ============================================================================

def add_clarification(
    question: str,
    answer: str,
    phase: str,
    category: str = 'general'
) -> None:
    """
    Persist a user's clarification answer for session recovery.

    Categories: scope, priority, technical, integration, data, error_handling
    """
    state = load_state()
    if not state:
        return

    state.setdefault('clarifications', []).append({
        'question': question,
        'answer': answer,
        'phase': phase,
        'category': category,
        'timestamp': now_iso()
    })
    save_state(state)
    log_progress(f"CLARIFICATION [{category}]: {question[:50]}... -> {answer[:50]}...")


def get_clarifications(phase: str = None, category: str = None) -> List[Dict[str, Any]]:
    """Get stored clarifications, optionally filtered by phase or category."""
    state = load_state()
    if not state:
        return []

    clarifications = state.get('clarifications', [])

    if phase:
        clarifications = [c for c in clarifications if c.get('phase') == phase]
    if category:
        clarifications = [c for c in clarifications if c.get('category') == category]

    return clarifications


def get_clarification_summary() -> str:
    """Get a summary of all clarifications for context."""
    state = load_state()
    if not state:
        return "No clarifications recorded."

    clarifications = state.get('clarifications', [])
    if not clarifications:
        return "No clarifications recorded."

    lines = ["## User Clarifications", ""]
    for c in clarifications:
        lines.append(f"**{c.get('category', 'general').title()}:** {c['question']}")
        lines.append(f"  → {c['answer']}")
        lines.append("")

    return '\n'.join(lines)


# ============================================================================
# Failure Categorization
# ============================================================================

# Failure categories with detection patterns
FAILURE_CATEGORIES = {
    'code': {
        'description': 'Bug in implementation',
        'patterns': ['error:', 'exception:', 'failed assertion', 'null reference', 'undefined'],
        'retryable': True
    },
    'test': {
        'description': 'Test itself is incorrect',
        'patterns': ['expected:', 'actual:', 'assertion failed', 'test setup failed'],
        'retryable': True
    },
    'infra': {
        'description': 'Infrastructure issue (DB, network, filesystem)',
        'patterns': ['connection refused', 'timeout', 'database', 'network', 'permission denied', 'disk full'],
        'retryable': True,
        'backoff': True
    },
    'external': {
        'description': 'External service unavailable',
        'patterns': ['api key', 'authentication', 'rate limit', '401', '403', '503', 'service unavailable'],
        'retryable': False,
        'escalate': True
    },
    'timeout': {
        'description': 'Operation timed out',
        'patterns': ['timed out', 'deadline exceeded', 'operation timeout'],
        'retryable': True,
        'backoff': True
    }
}


def categorize_failure(error_message: str) -> str:
    """
    Categorize a failure based on error message patterns.
    Returns the category name.
    """
    error_lower = error_message.lower()

    for category, config in FAILURE_CATEGORIES.items():
        for pattern in config['patterns']:
            if pattern.lower() in error_lower:
                return category

    return 'code'  # Default to code issue


def add_failure(
    story_id: str,
    error_message: str,
    category: str = None,
    context: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Record a categorized failure for analysis and retry decisions.

    Returns the failure record with retry recommendations.
    """
    state = load_state()
    if not state:
        return {}

    # Auto-categorize if not specified
    if not category:
        category = categorize_failure(error_message)

    category_config = FAILURE_CATEGORIES.get(category, FAILURE_CATEGORIES['code'])

    failure = {
        'id': f"F{len(state.get('failures', [])) + 1}",
        'storyId': story_id,
        'category': category,
        'message': error_message[:500],  # Truncate long messages
        'context': context or {},
        'timestamp': now_iso(),
        'iteration': get_iteration_count(),
        'retryable': category_config.get('retryable', True),
        'needsBackoff': category_config.get('backoff', False),
        'shouldEscalate': category_config.get('escalate', False)
    }

    state.setdefault('failures', []).append(failure)

    # Update metrics
    metrics = state.setdefault('metrics', {})
    by_category = metrics.setdefault('failuresByCategory', {})
    by_category[category] = by_category.get(category, 0) + 1

    save_state(state)
    log_progress(f"FAILURE [{category.upper()}]: {error_message[:100]}...", story_id=story_id)

    return failure


def get_story_failures(story_id: str) -> List[Dict[str, Any]]:
    """Get all failures for a specific story."""
    state = load_state()
    if not state:
        return []

    return [f for f in state.get('failures', []) if f.get('storyId') == story_id]


def get_retry_recommendation(story_id: str) -> Dict[str, Any]:
    """
    Analyze failures and recommend retry strategy.

    Returns:
        - should_retry: bool
        - reason: str
        - backoff_seconds: int (if applicable)
        - escalate: bool
    """
    failures = get_story_failures(story_id)

    if not failures:
        return {'should_retry': True, 'reason': 'No failures recorded'}

    recent = failures[-3:]  # Look at last 3 failures

    # Check for escalation triggers
    external_failures = [f for f in recent if f.get('category') == 'external']
    if len(external_failures) >= 2:
        return {
            'should_retry': False,
            'reason': 'External service failures - manual intervention needed',
            'escalate': True
        }

    # Check for infrastructure issues needing backoff
    infra_failures = [f for f in recent if f.get('needsBackoff')]
    if infra_failures:
        return {
            'should_retry': True,
            'reason': 'Infrastructure issue - retry with backoff',
            'backoff_seconds': 30 * len(infra_failures)  # Progressive backoff
        }

    # Check for repeated same error
    if len(recent) >= 3:
        messages = [f.get('message', '')[:50] for f in recent]
        if len(set(messages)) == 1:
            return {
                'should_retry': False,
                'reason': 'Same error repeated 3 times - needs different approach',
                'escalate': True
            }

    return {'should_retry': True, 'reason': 'Standard retry'}


# ============================================================================
# Elapsed Time Tracking & Alerts
# ============================================================================

def get_elapsed_minutes() -> float:
    """Get elapsed minutes since workflow start."""
    state = load_state()
    if not state:
        return 0

    try:
        started = datetime.fromisoformat(state['startedAt'].replace('Z', '+00:00'))
        elapsed = (datetime.now(timezone.utc) - started).total_seconds() / 60
        return round(elapsed, 1)
    except:
        return 0


def check_time_alerts() -> List[Dict[str, Any]]:
    """
    Check for time-based conditions and return alerts.

    Alerts:
    - Progress report due (every 30 min)
    - Long-running story warning (> story timeout)
    - Extended workflow warning (> 2 hours)
    - Checkpoint due (every 5 stories)
    """
    state = load_state()
    if not state:
        return []

    alerts = []
    elapsed = get_elapsed_minutes()

    # Check for progress report due
    last_report = state.get('checkpoints', {}).get('lastProgressReport')
    if last_report:
        try:
            last = datetime.fromisoformat(last_report.replace('Z', '+00:00'))
            mins_since_report = (datetime.now(timezone.utc) - last).total_seconds() / 60
            if mins_since_report >= 30:
                alerts.append({
                    'type': 'progress_report_due',
                    'severity': 'info',
                    'message': f'Progress report due (last: {int(mins_since_report)}m ago)'
                })
        except:
            pass

    # Check for extended workflow
    if elapsed >= 120:  # 2 hours
        alerts.append({
            'type': 'extended_workflow',
            'severity': 'warning',
            'message': f'Workflow running for {int(elapsed)}m - consider context management'
        })
    elif elapsed >= 240:  # 4 hours
        alerts.append({
            'type': 'very_long_workflow',
            'severity': 'critical',
            'message': f'Workflow running for {int(elapsed)}m - aggressive context trimming recommended'
        })

    # Check for story timeout
    current = get_next_story_internal(state)
    if current and current.get('status') == 'in_progress':
        story_timeout = state.get('timeouts', {}).get('storyMaxMinutes', 30)
        try:
            started = datetime.fromisoformat(current['lastUpdated'].replace('Z', '+00:00'))
            story_mins = (datetime.now(timezone.utc) - started).total_seconds() / 60
            if story_mins > story_timeout:
                alerts.append({
                    'type': 'story_timeout',
                    'severity': 'warning',
                    'storyId': current['id'],
                    'message': f"Story {current['id']} exceeded {story_timeout}m timeout ({int(story_mins)}m elapsed)"
                })
        except:
            pass

    # Check iteration count warnings
    iterations = get_iteration_count()
    if iterations >= 50:
        alerts.append({
            'type': 'high_iterations',
            'severity': 'warning',
            'message': f'High iteration count: {iterations} - verify progress is being made'
        })

    # Store alerts in state
    state['alerts'] = alerts
    save_state(state)

    return alerts


def get_next_story_internal(state: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Internal helper to get next story from provided state."""
    stories = state.get('stories', [])
    for s in stories:
        if s['status'] in ['in_progress', 'testing', 'review']:
            return s
    for s in stories:
        if s['status'] == 'pending':
            return s
    return None


# ============================================================================
# TDD Phase Tracking
# ============================================================================

TDD_PHASES = ['red', 'green', 'refactor', 'verify']


def update_tdd_phase(story_id: str, phase: str) -> bool:
    """
    Track TDD phase for a story.
    Phases: red (write failing test), green (make it pass), refactor, verify
    """
    if phase not in TDD_PHASES:
        return False

    state = load_state()
    if not state:
        return False

    for story in state['stories']:
        if story['id'] == story_id:
            story['tddPhase'] = phase
            story['tddPhaseStarted'] = now_iso()
            story.setdefault('tddHistory', []).append({
                'phase': phase,
                'timestamp': now_iso(),
                'iteration': get_iteration_count()
            })
            save_state(state)
            log_progress(f"TDD Phase: {phase.upper()}", story_id=story_id)
            return True

    return False


def get_tdd_phase(story_id: str) -> Optional[str]:
    """Get current TDD phase for a story."""
    state = load_state()
    if not state:
        return None

    for story in state['stories']:
        if story['id'] == story_id:
            return story.get('tddPhase')

    return None


def validate_tdd_progression(story_id: str, next_phase: str) -> Dict[str, Any]:
    """
    Validate TDD phase progression.
    Ensures red->green->refactor->verify order.
    """
    current = get_tdd_phase(story_id)

    if current is None and next_phase == 'red':
        return {'valid': True}

    expected_order = {'red': 'green', 'green': 'refactor', 'refactor': 'verify', 'verify': 'red'}

    if current and expected_order.get(current) == next_phase:
        return {'valid': True}

    # Allow skipping refactor if minor changes
    if current == 'green' and next_phase == 'verify':
        return {'valid': True, 'warning': 'Skipped refactor phase'}

    return {
        'valid': False,
        'error': f"Invalid TDD progression: {current or 'none'} -> {next_phase}",
        'expected': expected_order.get(current, 'red')
    }


# ============================================================================
# Workflow Lifecycle
# ============================================================================

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
    reset_iterations()  # Reset iteration count for new workflow
    state = create_initial_state(goal, session_id)
    save_state(state)
    log_progress(f"STARTED workflow {state['workflowId']} - Goal: {goal}")
    return state


def complete_workflow() -> bool:
    """Mark the workflow as completed and archive progress file."""
    state = load_state()
    if not state:
        return False

    state['status'] = 'completed'
    state['completedAt'] = now_iso()
    state['totalIterations'] = get_iteration_count()
    save_state(state)

    # Log completion
    stories = state.get('stories', [])
    completed = sum(1 for s in stories if s['status'] == 'completed')
    elapsed = get_elapsed_time(state.get('startedAt', now_iso()))
    log_progress(f"WORKFLOW COMPLETED - {completed}/{len(stories)} stories in {elapsed}")

    # Reset iteration counter
    reset_iterations()

    # Archive progress file
    try:
        if PROGRESS_FILE.exists():
            archive = CLAUDE_DIR / 'claude-progress.old'
            PROGRESS_FILE.rename(archive)
    except IOError:
        pass

    return True


# ============================================================================
# Story Management
# ============================================================================

def add_story(
    title: str,
    size: str = 'M',
    acceptance_criteria: List[str] = None,
    security_sensitive: bool = False
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
        'securitySensitive': security_sensitive,
        'assignedAgent': None,
        'attempts': 0,
        'iterations': [],  # Track each attempt
        'verificationChecks': {
            'testsPass': False,
            'coverageMet': False,
            'reviewApproved': False,
            'securityCleared': not security_sensitive
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
    """Update a story's status with iteration tracking."""
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
                # Track iteration details
                story.setdefault('iterations', []).append({
                    'attempt': story['attempts'],
                    'startedAt': now_iso(),
                    'globalIteration': get_iteration_count()
                })
                state['metrics']['totalAttempts'] = state['metrics'].get('totalAttempts', 0) + 1

            if status == 'completed':
                checks = story.get('verificationChecks', {})
                if not all([checks.get('testsPass'), checks.get('coverageMet'), checks.get('reviewApproved')]):
                    story['status'] = 'verified'
                    log_progress(f"Status: {old_status} -> verified (awaiting all checks)", story_id=story_id, agent=agent)
                else:
                    story['completedAt'] = now_iso()
                    state['checkpoints']['storiesSinceReview'] += 1
                    state['checkpoints']['storiesSinceReport'] += 1
                    state['metrics']['storiesCompleted'] = state['metrics'].get('storiesCompleted', 0) + 1
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
    """Update a verification check for a story."""
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

            if not passed:
                state['metrics']['failedVerifications'] = state['metrics'].get('failedVerifications', 0) + 1

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


def get_incomplete_stories() -> List[Dict[str, Any]]:
    """Get all stories that are not completed."""
    state = load_state()
    if not state:
        return []
    return [s for s in state.get('stories', []) if s['status'] not in ['completed', 'skipped']]


def get_next_story() -> Optional[Dict[str, Any]]:
    """Get the next story to work on (priority: in_progress > testing > review > pending)."""
    state = load_state()
    if not state:
        return None

    stories = state.get('stories', [])

    # First: any in progress
    for s in stories:
        if s['status'] in ['in_progress', 'testing', 'review']:
            return s

    # Then: first pending
    for s in stories:
        if s['status'] == 'pending':
            return s

    return None


# ============================================================================
# Progress Reporting
# ============================================================================

def should_generate_progress_report() -> bool:
    """Check if a progress report should be generated."""
    state = load_state()
    if not state:
        return False

    checkpoints = state.get('checkpoints', {})

    # Every 3 stories
    if checkpoints.get('storiesSinceReport', 0) >= 3:
        return True

    # Every 30 minutes
    last_report = checkpoints.get('lastProgressReport')
    if last_report:
        try:
            last = datetime.fromisoformat(last_report.replace('Z', '+00:00'))
            elapsed = (datetime.now(timezone.utc) - last).total_seconds() / 60
            if elapsed >= 30:
                return True
        except:
            pass

    return False


def record_progress_report() -> None:
    """Record that a progress report was generated."""
    state = load_state()
    if not state:
        return

    state['checkpoints']['lastProgressReport'] = now_iso()
    state['checkpoints']['storiesSinceReport'] = 0
    save_state(state)


def get_workflow_summary() -> Dict[str, Any]:
    """Get a summary of the current workflow state."""
    state = load_state()
    if not state:
        return {'error': 'No active workflow'}

    stories = state.get('stories', [])
    completed = sum(1 for s in stories if s['status'] == 'completed')
    in_progress = sum(1 for s in stories if s['status'] in ['in_progress', 'testing', 'review'])
    pending = sum(1 for s in stories if s['status'] == 'pending')
    blocked = sum(1 for s in stories if s['status'] == 'blocked')

    current = get_next_story()

    return {
        'workflowId': state.get('workflowId'),
        'goal': state.get('goal'),
        'status': state.get('status'),
        'currentPhase': state.get('currentPhase'),
        'currentAgent': state.get('currentAgent'),
        'elapsed': get_elapsed_time(state.get('startedAt', now_iso())),
        'iterations': get_iteration_count(),
        'currentStory': {
            'id': current['id'],
            'title': current['title'],
            'status': current['status'],
            'attempts': current.get('attempts', 0)
        } if current else None,
        'progress': {
            'total': len(stories),
            'completed': completed,
            'in_progress': in_progress,
            'pending': pending,
            'blocked': blocked,
            'percentage': round(completed / len(stories) * 100) if stories else 0
        },
        'metrics': state.get('metrics', {}),
        'checkpointDue': should_checkpoint(),
        'progressReportDue': should_generate_progress_report(),
        'blockers': [b for b in state.get('blockers', []) if not b['resolved']]
    }


# ============================================================================
# Blocker Management
# ============================================================================

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

    if not any(b for b in state['blockers'] if not b['resolved']):
        state['status'] = 'in_progress'

    save_state(state)
    return True


# ============================================================================
# Checkpoints
# ============================================================================

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


# ============================================================================
# Git Integration
# ============================================================================

def _run_git_command(args: List[str], cwd: Path = None) -> Optional[str]:
    """Run a git command and return output, or None on failure."""
    try:
        result = subprocess.run(
            ['git'] + args,
            cwd=cwd or PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return None
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return None


def mark_working_state() -> Optional[str]:
    """Mark current commit as a known working state."""
    result = _run_git_command(['rev-parse', 'HEAD'])
    if not result:
        return None

    commit_sha = result.strip()
    state = load_state()
    if state:
        state['lastWorkingCommit'] = commit_sha
        state['lastWorkingAt'] = now_iso()
        save_state(state)
        log_progress(f"Marked working state: {commit_sha[:8]}")

    return commit_sha


def rollback_to_checkpoint() -> bool:
    """Revert to last known working commit."""
    state = load_state()
    if not state:
        return False

    last_good = state.get('lastWorkingCommit')
    if not last_good:
        return False

    _run_git_command(['stash', 'push', '-m', 'Pre-rollback stash'])
    result = _run_git_command(['reset', '--hard', last_good])
    if result is not None:
        log_progress(f"Rolled back to checkpoint: {last_good[:8]}")
        return True

    return False


# ============================================================================
# Session Recovery
# ============================================================================

def get_session_recovery_info() -> Dict[str, Any]:
    """Get comprehensive session recovery information."""
    state = load_state()
    recent_progress = get_recent_progress(15)

    if not state:
        return {
            'has_active_workflow': False,
            'recent_progress': recent_progress
        }

    stories = state.get('stories', [])
    current_story = get_next_story()

    return {
        'has_active_workflow': True,
        'workflow_id': state.get('workflowId'),
        'goal': state.get('goal'),
        'status': state.get('status'),
        'elapsed': get_elapsed_time(state.get('startedAt', now_iso())),
        'iterations': get_iteration_count(),
        'current_phase': state.get('currentPhase'),
        'current_story': {
            'id': current_story['id'],
            'title': current_story['title'],
            'status': current_story['status'],
            'attempts': current_story.get('attempts', 0),
            'verification': current_story.get('verificationChecks', {})
        } if current_story else None,
        'stories_summary': {
            'total': len(stories),
            'completed': sum(1 for s in stories if s['status'] == 'completed'),
            'in_progress': sum(1 for s in stories if s['status'] in ['in_progress', 'testing', 'review']),
            'pending': sum(1 for s in stories if s['status'] == 'pending')
        },
        'blockers': [b for b in state.get('blockers', []) if not b['resolved']],
        'recent_progress': recent_progress
    }


def get_compact_context() -> str:
    """Return minimal context summary for recovery."""
    state = load_state()
    if not state:
        return "No active workflow"

    stories = state.get('stories', [])
    completed = [s for s in stories if s['status'] == 'completed']
    current = get_next_story()
    blockers = [b for b in state.get('blockers', []) if not b.get('resolved')]

    lines = [
        f"=== Workflow {state.get('workflowId')} ===",
        f"Goal: {state.get('goal')}",
        f"Phase: {state.get('currentPhase')}",
        f"Elapsed: {get_elapsed_time(state.get('startedAt', now_iso()))}",
        f"Iterations: {get_iteration_count()}",
        f"Progress: {len(completed)}/{len(stories)} ({round(len(completed)/len(stories)*100) if stories else 0}%)",
        "",
    ]

    if current:
        lines.append(f"CURRENT: [{current['id']}] {current['title']}")
        lines.append(f"  Status: {current['status']}, Attempts: {current.get('attempts', 0)}")
        checks = current.get('verificationChecks', {})
        checks_str = ', '.join(f"{k}={'Y' if v else 'N'}" for k, v in checks.items())
        lines.append(f"  Checks: {checks_str}")
        lines.append("")

    if blockers:
        lines.append("BLOCKERS:")
        for b in blockers:
            lines.append(f"  - [{b.get('severity')}] {b['description']}")

    return '\n'.join(lines)


def trim_progress_file(max_lines: int = 100) -> bool:
    """Keep only recent progress entries."""
    if not PROGRESS_FILE.exists():
        return True

    try:
        lines = PROGRESS_FILE.read_text(encoding='utf-8').splitlines()
        if len(lines) > max_lines:
            trimmed = lines[-max_lines:]
            PROGRESS_FILE.write_text('\n'.join(trimmed) + '\n', encoding='utf-8')
            log_progress(f"Trimmed progress file to {max_lines} lines")
        return True
    except IOError:
        return False


# ============================================================================
# CLI Interface
# ============================================================================

if __name__ == '__main__':
    import sys
    import argparse

    if len(sys.argv) < 2:
        print('Usage: python state.py <command> [args]')
        print('')
        print('Workflow Lifecycle:')
        print('  init <goal> [--session ID]     Initialize or resume workflow')
        print('  status                         Show workflow summary')
        print('  recover                        Get session recovery info')
        print('  complete                       Mark workflow as completed')
        print('')
        print('Story Management:')
        print('  add-story <title> [--size S|M|L|XL] [--security]')
        print('  update-story <id> <status> [--agent name]')
        print('  verify <story_id> <check> [--passed|--failed] [--details "msg"]')
        print('  verify-status <story_id>       Get verification status')
        print('')
        print('TDD Tracking:')
        print('  tdd-phase <story_id> <phase>   Set TDD phase (red|green|refactor|verify)')
        print('  tdd-status <story_id>          Get current TDD phase')
        print('  tdd-validate <story_id> <next> Validate TDD phase transition')
        print('')
        print('Clarifications:')
        print('  add-clarification <question> <answer> --phase <phase> [--category <cat>]')
        print('  get-clarifications [--phase <phase>] [--category <cat>]')
        print('  clarification-summary          Get formatted summary of all clarifications')
        print('')
        print('Failure Tracking:')
        print('  add-failure <story_id> <error> [--category code|test|infra|external|timeout]')
        print('  get-failures <story_id>        Get all failures for a story')
        print('  retry-recommendation <story_id> Get retry strategy recommendation')
        print('')
        print('Time & Alerts:')
        print('  elapsed                        Show elapsed time in minutes')
        print('  check-alerts                   Check for time-based alerts')
        print('')
        print('Progress & Context:')
        print('  progress [--lines N]           Show recent progress entries')
        print('  compact-context                Get minimal context summary')
        print('  trim-progress [--lines N]      Trim progress file')
        print('')
        print('Blockers:')
        print('  add-blocker <desc> [--severity low|medium|high|critical]')
        print('  resolve-blocker <index>        Resolve blocker by index')
        print('')
        print('Git Recovery:')
        print('  mark-working-state             Mark current commit as working')
        print('  rollback-to-checkpoint         Revert to last working commit')
        print('')
        print('Iteration Tracking:')
        print('  iteration                      Show current iteration count')
        print('')
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

    elif command == 'complete':
        complete_workflow()
        print('Workflow completed')

    elif command == 'add-story':
        title = sys.argv[2] if len(sys.argv) > 2 else 'New Story'
        size = 'M'
        security_sensitive = False
        for i, arg in enumerate(sys.argv):
            if arg == '--size' and i + 1 < len(sys.argv):
                size = sys.argv[i + 1].upper()
            elif arg == '--security':
                security_sensitive = True
        story_id = add_story(title, size, None, security_sensitive)
        print(f'Added story: {story_id} (size: {size})')

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
            print(f'Failed to update {story_id}')
            sys.exit(1)

    elif command == 'verify':
        story_id = sys.argv[2] if len(sys.argv) > 2 else 'S1'
        check_name = sys.argv[3] if len(sys.argv) > 3 else 'testsPass'
        passed = True
        details = None
        for i, arg in enumerate(sys.argv):
            if arg == '--failed':
                passed = False
            elif arg == '--passed':
                passed = True
            elif arg == '--details' and i + 1 < len(sys.argv):
                details = sys.argv[i + 1]
        if update_verification_check(story_id, check_name, passed, details):
            print(f'Verification {check_name} for {story_id}: {"PASSED" if passed else "FAILED"}')
        else:
            print(f'Failed to update verification')
            sys.exit(1)

    elif command == 'verify-status':
        story_id = sys.argv[2] if len(sys.argv) > 2 else 'S1'
        state = load_state()
        if state:
            for s in state.get('stories', []):
                if s['id'] == story_id:
                    print(json.dumps(s.get('verificationChecks', {}), indent=2))
                    break

    elif command == 'progress':
        lines = 20
        for i, arg in enumerate(sys.argv):
            if arg == '--lines' and i + 1 < len(sys.argv):
                lines = int(sys.argv[i + 1])
        entries = get_recent_progress(lines)
        for entry in entries:
            print(entry)

    elif command == 'compact-context':
        print(get_compact_context())

    elif command == 'trim-progress':
        max_lines = 100
        for i, arg in enumerate(sys.argv):
            if arg == '--lines' and i + 1 < len(sys.argv):
                max_lines = int(sys.argv[i + 1])
        trim_progress_file(max_lines)
        print(f'Progress file trimmed to {max_lines} lines')

    elif command == 'add-blocker':
        description = sys.argv[2] if len(sys.argv) > 2 else 'Unknown blocker'
        severity = 'medium'
        for i, arg in enumerate(sys.argv):
            if arg == '--severity' and i + 1 < len(sys.argv):
                severity = sys.argv[i + 1]
        add_blocker(description, severity)
        print(f'Added blocker: {description}')

    elif command == 'resolve-blocker':
        index = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        resolve_blocker(index)
        print(f'Resolved blocker at index {index}')

    elif command == 'mark-working-state':
        commit = mark_working_state()
        if commit:
            print(f'Marked working state: {commit[:8]}')
        else:
            print('Failed to mark working state')
            sys.exit(1)

    elif command == 'rollback-to-checkpoint':
        if rollback_to_checkpoint():
            print('Rolled back to last checkpoint')
        else:
            print('Failed to rollback')
            sys.exit(1)

    elif command == 'iteration':
        print(f'Current iteration: {get_iteration_count()}')

    # TDD Tracking commands
    elif command == 'tdd-phase':
        story_id = sys.argv[2] if len(sys.argv) > 2 else 'S1'
        phase = sys.argv[3] if len(sys.argv) > 3 else 'red'
        if update_tdd_phase(story_id, phase):
            print(f'TDD phase for {story_id}: {phase.upper()}')
        else:
            print(f'Failed to set TDD phase (invalid phase or story)')
            sys.exit(1)

    elif command == 'tdd-status':
        story_id = sys.argv[2] if len(sys.argv) > 2 else 'S1'
        phase = get_tdd_phase(story_id)
        print(f'TDD phase for {story_id}: {phase or "not started"}')

    elif command == 'tdd-validate':
        story_id = sys.argv[2] if len(sys.argv) > 2 else 'S1'
        next_phase = sys.argv[3] if len(sys.argv) > 3 else 'green'
        result = validate_tdd_progression(story_id, next_phase)
        print(json.dumps(result, indent=2))
        if not result.get('valid'):
            sys.exit(1)

    # Clarification commands
    elif command == 'add-clarification':
        question = sys.argv[2] if len(sys.argv) > 2 else 'Question'
        answer = sys.argv[3] if len(sys.argv) > 3 else 'Answer'
        phase = 'general'
        category = 'general'
        for i, arg in enumerate(sys.argv):
            if arg == '--phase' and i + 1 < len(sys.argv):
                phase = sys.argv[i + 1]
            elif arg == '--category' and i + 1 < len(sys.argv):
                category = sys.argv[i + 1]
        add_clarification(question, answer, phase, category)
        print(f'Added clarification: {question[:30]}...')

    elif command == 'get-clarifications':
        phase = None
        category = None
        for i, arg in enumerate(sys.argv):
            if arg == '--phase' and i + 1 < len(sys.argv):
                phase = sys.argv[i + 1]
            elif arg == '--category' and i + 1 < len(sys.argv):
                category = sys.argv[i + 1]
        clarifications = get_clarifications(phase, category)
        print(json.dumps(clarifications, indent=2))

    elif command == 'clarification-summary':
        print(get_clarification_summary())

    # Failure tracking commands
    elif command == 'add-failure':
        story_id = sys.argv[2] if len(sys.argv) > 2 else 'S1'
        error = sys.argv[3] if len(sys.argv) > 3 else 'Unknown error'
        category = None
        for i, arg in enumerate(sys.argv):
            if arg == '--category' and i + 1 < len(sys.argv):
                category = sys.argv[i + 1]
        failure = add_failure(story_id, error, category)
        print(f'Added failure: {failure.get("id")} [{failure.get("category")}]')

    elif command == 'get-failures':
        story_id = sys.argv[2] if len(sys.argv) > 2 else 'S1'
        failures = get_story_failures(story_id)
        print(json.dumps(failures, indent=2))

    elif command == 'retry-recommendation':
        story_id = sys.argv[2] if len(sys.argv) > 2 else 'S1'
        recommendation = get_retry_recommendation(story_id)
        print(json.dumps(recommendation, indent=2))
        if recommendation.get('escalate'):
            sys.exit(2)  # Special exit code for escalation

    # Time & Alert commands
    elif command == 'elapsed':
        print(f'Elapsed: {get_elapsed_minutes()} minutes')

    elif command == 'check-alerts':
        alerts = check_time_alerts()
        if alerts:
            print('ALERTS:')
            for alert in alerts:
                print(f"  [{alert['severity'].upper()}] {alert['type']}: {alert['message']}")
            # Exit with warning code if critical alerts
            if any(a['severity'] == 'critical' for a in alerts):
                sys.exit(3)
        else:
            print('No alerts')

    else:
        print(f'Unknown command: {command}')
        sys.exit(1)
