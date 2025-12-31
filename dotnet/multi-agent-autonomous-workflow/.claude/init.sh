#!/bin/bash
#
# Environment Initialization Script
# Per Anthropic best practices: "Creates init.sh script for development server startup...
# eliminates setup guesswork"
#
# Run this at the start of each session to ensure consistent environment state.
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=============================================="
echo "  Multi-Agent Workflow Environment Setup"
echo "=============================================="
echo ""

# Get script directory (works even when called from different locations)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"
echo "Working directory: $(pwd)"
echo ""

# 1. Check prerequisites
echo "=== Checking Prerequisites ==="

check_command() {
    if command -v "$1" >/dev/null 2>&1; then
        echo -e "${GREEN}[OK]${NC} $1 found: $(command -v "$1")"
        return 0
    else
        echo -e "${RED}[MISSING]${NC} $1 not found"
        return 1
    fi
}

PREREQS_OK=true

check_command "dotnet" || PREREQS_OK=false
check_command "python" || PREREQS_OK=false
check_command "git" || PREREQS_OK=false

if [ "$PREREQS_OK" = false ]; then
    echo ""
    echo -e "${RED}ERROR: Missing prerequisites. Please install missing tools.${NC}"
    exit 1
fi

echo ""
echo ".NET SDK Version: $(dotnet --version)"
echo "Python Version: $(python --version 2>&1)"
echo "Git Version: $(git --version)"
echo ""

# 2. Check git status
echo "=== Git Status ==="
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "not a git repo")
echo "Current branch: $BRANCH"

if git diff --quiet 2>/dev/null; then
    echo -e "${GREEN}[CLEAN]${NC} No uncommitted changes"
else
    echo -e "${YELLOW}[MODIFIED]${NC} Uncommitted changes present"
    git status --short
fi
echo ""

# 3. Check workflow state
echo "=== Workflow State ==="
if [ -f ".claude/workflow-state.json" ]; then
    echo -e "${GREEN}[ACTIVE]${NC} Workflow state found"
    python .claude/hooks/state.py status 2>/dev/null || echo "Could not read state"
else
    echo -e "${YELLOW}[NONE]${NC} No active workflow"
fi
echo ""

# 4. Restore dependencies
echo "=== Restoring Dependencies ==="
if [ -f "*.sln" ] || find . -maxdepth 2 -name "*.sln" -quit 2>/dev/null; then
    echo "Restoring NuGet packages..."
    dotnet restore --verbosity quiet && echo -e "${GREEN}[OK]${NC} Dependencies restored" || {
        echo -e "${RED}[FAIL]${NC} Failed to restore dependencies"
        exit 1
    }
else
    echo -e "${YELLOW}[SKIP]${NC} No .sln file found - skipping restore"
fi
echo ""

# 5. Build solution
echo "=== Building Solution ==="
if [ -f "*.sln" ] || find . -maxdepth 2 -name "*.sln" -quit 2>/dev/null; then
    dotnet build --no-restore --verbosity quiet && echo -e "${GREEN}[OK]${NC} Build succeeded" || {
        echo -e "${RED}[FAIL]${NC} Build failed"
        echo "Run 'dotnet build' for full output"
        exit 1
    }
else
    echo -e "${YELLOW}[SKIP]${NC} No .sln file found - skipping build"
fi
echo ""

# 6. Run tests (optional - comment out for faster startup)
echo "=== Running Tests ==="
if [ -f "*.sln" ] || find . -maxdepth 2 -name "*.sln" -quit 2>/dev/null; then
    TEST_RESULT=$(dotnet test --no-build --verbosity quiet 2>&1) && {
        echo -e "${GREEN}[PASS]${NC} All tests passing"
    } || {
        echo -e "${YELLOW}[WARN]${NC} Some tests failing"
        echo "Run 'dotnet test' for details"
    }
else
    echo -e "${YELLOW}[SKIP]${NC} No .sln file found - skipping tests"
fi
echo ""

# 7. Display recent progress (if workflow active)
if [ -f ".claude/claude-progress.txt" ]; then
    echo "=== Recent Progress ==="
    tail -10 .claude/claude-progress.txt 2>/dev/null || echo "No progress logged yet"
    echo ""
fi

# 8. Summary
echo "=============================================="
echo -e "${GREEN}  Environment Ready${NC}"
echo "=============================================="
echo ""
echo "Next steps:"
echo "  - Start workflow:  /workflow [goal]"
echo "  - Check status:    /status"
echo "  - View state:      python .claude/hooks/state.py status"
echo "  - Session recovery: python .claude/hooks/state.py recover"
echo ""
