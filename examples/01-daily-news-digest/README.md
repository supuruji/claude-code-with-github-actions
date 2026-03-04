# Example 01: Daily News Digest

## Overview

Claude Code automatically visits tech news sites daily, extracts top headlines, summarizes emerging trends, and saves the result as a structured markdown file. This example demonstrates browser automation via Chrome DevTools MCP combined with Claude's analysis capabilities.

## What It Does

1. Launches a headless Chrome browser in GitHub Actions
2. Visits Hacker News and TechCrunch via Chrome DevTools MCP
3. Takes screenshots for visual reference
4. Extracts top headlines and metadata
5. Generates a curated digest with trend analysis
6. Commits the digest to the `output/` directory

## Architecture

```
Schedule (8 AM UTC daily)
    |
    v
GitHub Actions Runner
    |
    ├── Chrome (headless) + chrome-devtools MCP
    ├── sequential-thinking MCP (analysis)
    └── fetch MCP (API fallback)
    |
    v
Claude Code
    ├── Agent: news-curator.md
    └── Skill: news-digest-generator
    |
    v
output/YYYY-MM-DD-digest.md (git push)
```

## Setup

### 1. Repository Secrets

| Secret | Description |
|--------|-------------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key |

### 2. Enable the Workflow

The workflow is located at `.github/workflows/news-digest.yml`. It runs automatically on schedule, or you can trigger it manually from the Actions tab.

### 3. Output

Generated digests are saved to `output/YYYY-MM-DD-digest.md` and committed automatically.

## Customization

- **Sources**: Edit the prompt in the workflow file to add/remove news sources
- **Schedule**: Modify the cron expression in the workflow trigger
- **Format**: Update `.claude/skills/news-digest-generator/assets/template.md`
- **Dedup Logic**: Adjust `.claude/skills/news-digest-generator/scripts/check_duplicates.py`
