#!/usr/bin/env python3
"""
Platform Configuration Manager - Dynamic Discovery

Provides utilities for:
- Dynamic platform discovery from Workflows/platforms/
- Platform matching based on codebase markers
- Accessing platform-specific commands and conventions

This version supports fully dynamic platform detection without
hardcoding any platform names or configurations.
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# Search paths for platforms directory
SCRIPT_DIR = Path(__file__).parent.resolve()
CLAUDE_DIR = SCRIPT_DIR.parent
PROJECT_ROOT = CLAUDE_DIR.parent

# Potential locations for platforms
PLATFORM_SEARCH_PATHS = [
    PROJECT_ROOT / 'Workflows' / 'platforms',
    PROJECT_ROOT.parent / 'Workflows' / 'platforms',
    Path(os.environ.get('WORKFLOW_PLATFORMS_PATH', '')) if os.environ.get('WORKFLOW_PLATFORMS_PATH') else None,
    Path('/workflows/platforms') if Path('/workflows/platforms').exists() else None,
]

# Cached platform config
_cached_platform: Optional[Dict[str, Any]] = None
_platform_config_path: Optional[Path] = None


def find_platforms_directory() -> Optional[Path]:
    """Find the platforms directory."""
    for path in PLATFORM_SEARCH_PATHS:
        if path and path.exists() and path.is_dir():
            return path
    return None


def discover_platforms() -> List[Dict[str, Any]]:
    """
    Dynamically discover all available platforms.

    Scans Workflows/platforms/ for subdirectories containing platform.json.
    Returns list of platform configs with metadata.
    """
    platforms_dir = find_platforms_directory()
    if not platforms_dir:
        return []

    platforms = []
    for subdir in platforms_dir.iterdir():
        if subdir.is_dir():
            config_file = subdir / 'platform.json'
            if config_file.exists():
                try:
                    config = json.loads(config_file.read_text(encoding='utf-8'))
                    config['_path'] = str(subdir)
                    config['_config_file'] = str(config_file)
                    platforms.append(config)
                except (json.JSONDecodeError, IOError):
                    pass

    return platforms


def check_marker(marker: str, project_root: Path) -> bool:
    """Check if a marker file/pattern exists in the project."""
    # Handle glob patterns
    if '*' in marker:
        matches = list(project_root.glob(marker))
        return len(matches) > 0

    # Handle exact file path
    return (project_root / marker).exists()


def match_platform_to_codebase(
    codebase_root: Path = None,
    platforms: List[Dict[str, Any]] = None
) -> Tuple[Optional[Dict[str, Any]], str]:
    """
    Match available platforms to the current codebase.

    Returns (matched_platform, reason) tuple.
    Uses markers and matchMode from each platform's config.
    """
    root = codebase_root or PROJECT_ROOT
    available = platforms or discover_platforms()

    if not available:
        return None, "No platforms found in search paths"

    candidates = []

    for platform in available:
        markers = platform.get('markers', [])
        match_mode = platform.get('matchMode', 'any')  # 'any' or 'all'
        priority = platform.get('priority', 50)

        if not markers:
            continue

        matches = [check_marker(m, root) for m in markers]

        if match_mode == 'all':
            matched = all(matches)
        else:  # 'any'
            matched = any(matches)

        if matched:
            matched_markers = [m for m, found in zip(markers, matches) if found]
            candidates.append({
                'platform': platform,
                'priority': priority,
                'matched_markers': matched_markers
            })

    if not candidates:
        return None, "No platform markers matched in codebase"

    # Sort by priority (highest first)
    candidates.sort(key=lambda x: x['priority'], reverse=True)
    best = candidates[0]

    return best['platform'], f"Matched markers: {', '.join(best['matched_markers'])}"


def load_platform(config_path: Path = None) -> Dict[str, Any]:
    """Load platform configuration from file or auto-detect."""
    global _cached_platform, _platform_config_path

    # Check cache
    if _cached_platform and (config_path is None or config_path == _platform_config_path):
        return _cached_platform

    # Explicit path provided
    if config_path and config_path.exists():
        try:
            _cached_platform = json.loads(config_path.read_text(encoding='utf-8'))
            _platform_config_path = config_path
            return _cached_platform
        except (json.JSONDecodeError, IOError):
            pass

    # Check for platform.json in standard locations
    for path in [CLAUDE_DIR / 'platform.json', PROJECT_ROOT / 'platform.json']:
        if path.exists():
            try:
                _cached_platform = json.loads(path.read_text(encoding='utf-8'))
                _platform_config_path = path
                return _cached_platform
            except (json.JSONDecodeError, IOError):
                pass

    # Auto-detect from available platforms
    platform, reason = match_platform_to_codebase()
    if platform:
        _cached_platform = platform
        return platform

    # Return default if nothing found
    return get_default_platform()


def get_default_platform() -> Dict[str, Any]:
    """Get default platform config when no platform is detected."""
    return {
        'name': 'generic',
        'displayName': 'Generic Project',
        'version': '1.0.0',
        'commands': {
            'build': 'echo "No build command configured - please set up platform.json"',
            'test': 'echo "No test command configured - please set up platform.json"'
        },
        'conventions': {
            'testNaming': '{Method}_{Scenario}_{Expected}',
            'commitFormat': 'type: description'
        },
        'qualityGates': {
            'coverageThresholds': {'S': 70, 'M': 80, 'L': 85, 'XL': 90},
            'requiredChecks': ['build', 'test']
        }
    }


def get_command(name: str, platform: Dict[str, Any] = None) -> Optional[str]:
    """Get a command by name from platform config."""
    p = platform or load_platform()
    return p.get('commands', {}).get(name)


def get_convention(name: str, platform: Dict[str, Any] = None) -> Optional[str]:
    """Get a convention by name."""
    p = platform or load_platform()
    return p.get('conventions', {}).get(name)


def get_quality_gate(name: str, platform: Dict[str, Any] = None) -> Any:
    """Get a quality gate value."""
    p = platform or load_platform()
    return p.get('qualityGates', {}).get(name)


def get_pattern(name: str, platform: Dict[str, Any] = None) -> Optional[str]:
    """Get a file pattern by name."""
    p = platform or load_platform()
    return p.get('patterns', {}).get(name)


def get_coverage_threshold(size: str, platform: Dict[str, Any] = None) -> int:
    """Get coverage threshold for story size."""
    p = platform or load_platform()
    thresholds = p.get('qualityGates', {}).get('coverageThresholds', {})
    return thresholds.get(size.upper(), 80)


def substitute_placeholders(template: str, **kwargs) -> str:
    """Substitute placeholders in a template string."""
    result = template
    for key, value in kwargs.items():
        result = result.replace(f'{{{key}}}', str(value))
    return result


def run_command(name: str, platform: Dict[str, Any] = None, **kwargs) -> subprocess.CompletedProcess:
    """Run a platform command with optional placeholder substitution."""
    cmd = get_command(name, platform)
    if not cmd:
        raise ValueError(f"Unknown command: {name}")

    cmd = substitute_placeholders(cmd, **kwargs)
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=PROJECT_ROOT)


def list_commands(platform: Dict[str, Any] = None) -> List[str]:
    """List all available commands."""
    p = platform or load_platform()
    return list(p.get('commands', {}).keys())


def list_conventions(platform: Dict[str, Any] = None) -> List[str]:
    """List all available conventions."""
    p = platform or load_platform()
    return list(p.get('conventions', {}).keys())


def get_platform_info() -> Dict[str, Any]:
    """Get comprehensive platform information."""
    platforms_dir = find_platforms_directory()
    available = discover_platforms()
    current, match_reason = match_platform_to_codebase()

    return {
        'platforms_directory': str(platforms_dir) if platforms_dir else None,
        'available_platforms': [
            {
                'name': p.get('name'),
                'displayName': p.get('displayName'),
                'markers': p.get('markers', []),
                'priority': p.get('priority', 50)
            }
            for p in available
        ],
        'detected_platform': current.get('name') if current else None,
        'match_reason': match_reason,
        'commands': list_commands(current) if current else [],
        'conventions': list_conventions(current) if current else []
    }


# CLI interface
if __name__ == '__main__':
    import argparse

    if len(sys.argv) < 2:
        print('Usage: python platform.py <command> [args]')
        print('')
        print('Discovery:')
        print('  discover                    List all available platforms')
        print('  detect                      Detect platform for current codebase')
        print('  info                        Show comprehensive platform info')
        print('')
        print('Commands:')
        print('  get-command <name>          Get a command template')
        print('  run <name>                  Run a platform command')
        print('  list-commands               List all available commands')
        print('')
        print('Conventions:')
        print('  get-convention <name>       Get a convention value')
        print('  get-threshold <size>        Get coverage threshold (S/M/L/XL)')
        print('  get-pattern <name>          Get a file pattern')
        print('  list-conventions            List all conventions')
        print('')
        sys.exit(1)

    command = sys.argv[1]

    if command == 'discover':
        platforms = discover_platforms()
        if platforms:
            print(f'Found {len(platforms)} platforms:\n')
            for p in platforms:
                print(f"  {p.get('name')}: {p.get('displayName', 'No description')}")
                print(f"    Markers: {', '.join(p.get('markers', []))}")
                print(f"    Priority: {p.get('priority', 50)}")
                print()
        else:
            print('No platforms found in search paths')

    elif command == 'detect':
        platform, reason = match_platform_to_codebase()
        if platform:
            print(f"Detected: {platform.get('name')} ({platform.get('displayName')})")
            print(f"Reason: {reason}")
        else:
            print(f"No platform detected: {reason}")

    elif command == 'info':
        info = get_platform_info()
        print(json.dumps(info, indent=2))

    elif command == 'get-command':
        name = sys.argv[2] if len(sys.argv) > 2 else 'build'
        cmd = get_command(name)
        if cmd:
            print(cmd)
        else:
            print(f"Command not found: {name}", file=sys.stderr)
            sys.exit(1)

    elif command == 'run':
        name = sys.argv[2] if len(sys.argv) > 2 else 'build'
        try:
            result = run_command(name)
            print(result.stdout, end='')
            if result.stderr:
                print(result.stderr, file=sys.stderr, end='')
            sys.exit(result.returncode)
        except ValueError as e:
            print(str(e), file=sys.stderr)
            sys.exit(1)

    elif command == 'list-commands':
        for cmd in list_commands():
            print(cmd)

    elif command == 'get-convention':
        name = sys.argv[2] if len(sys.argv) > 2 else 'testNaming'
        conv = get_convention(name)
        if conv:
            print(conv)
        else:
            print(f"Convention not found: {name}", file=sys.stderr)
            sys.exit(1)

    elif command == 'get-threshold':
        size = sys.argv[2] if len(sys.argv) > 2 else 'M'
        print(get_coverage_threshold(size))

    elif command == 'get-pattern':
        name = sys.argv[2] if len(sys.argv) > 2 else 'entity'
        pattern = get_pattern(name)
        if pattern:
            print(pattern)
        else:
            print(f"Pattern not found: {name}", file=sys.stderr)
            sys.exit(1)

    elif command == 'list-conventions':
        for conv in list_conventions():
            print(conv)

    else:
        print(f'Unknown command: {command}')
        sys.exit(1)
