# Example 02: Repo Health Checker

## Overview

Claude Code analyzes your repository weekly, identifies potential issues, and automatically creates a GitHub Issue with detailed findings and recommendations. This example uses only Claude Code's built-in tools -- no Chrome or MCP servers required.

## What It Does

1. Scans the repository for outdated dependencies
2. Checks for missing or incomplete documentation
3. Identifies code smells and common anti-patterns
4. Reviews test coverage gaps
5. Checks for security-related issues (exposed secrets, vulnerable patterns)
6. Creates a GitHub Issue summarizing all findings

## Architecture

```
Schedule (Monday 9 AM UTC weekly)
    |
    v
GitHub Actions Runner
    |
    └── Claude Code (built-in tools only)
        ├── Read / Grep / Glob (code analysis)
        └── Bash (dependency checks, git analysis)
    |
    v
GitHub Issue (auto-created with findings)
```

## Setup

### 1. Repository Secrets

| Secret | Description |
|--------|-------------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key |

### 2. Permissions

The workflow needs `issues: write` and `contents: read` permissions. These are configured in the workflow file.

### 3. Enable the Workflow

The workflow is at `.github/workflows/repo-health.yml`. Runs weekly on Mondays, or trigger manually from the Actions tab.

## Checks Performed

| Category | What It Checks |
|----------|---------------|
| Dependencies | Outdated packages, known vulnerabilities, unused deps |
| Documentation | Missing README sections, outdated API docs, missing JSDoc/docstrings |
| Code Quality | Long functions, deep nesting, TODO/FIXME counts, dead code |
| Testing | Missing test files, low coverage areas, skipped tests |
| Security | Hardcoded secrets, unsafe patterns, missing .gitignore entries |
| Repository | Branch hygiene, large files, missing CI configs |

## Customization

- **Check Categories**: Modify the prompt in the workflow to add/remove check categories
- **Severity Threshold**: Adjust the agent instructions to filter by severity
- **Schedule**: Change the cron expression for different frequencies
- **Output**: Switch from GitHub Issues to markdown files by modifying the final step
