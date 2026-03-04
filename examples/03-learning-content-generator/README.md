# Example 03: Learning Content Generator

## Overview

Claude Code generates vocabulary learning materials through a multi-step process: web research for current usage examples, word selection at the appropriate difficulty level, and structured content creation with practice questions. Based on a proven TOEIC/TOEFL vocabulary study pattern.

## What It Does

1. Researches current vocabulary usage through web sources
2. Selects words at the target difficulty level (avoiding duplicates)
3. Generates definitions with context-rich example sentences
4. Creates practice questions (multiple choice, fill-in-the-blank, matching)
5. Adds learning tips and mnemonic devices
6. Saves structured output and commits to the repository

## Architecture

```
Schedule (every 6 hours) or Manual Trigger
    |
    v
GitHub Actions Runner
    |
    ├── Chrome (headless) + chrome-devtools MCP
    ├── sequential-thinking MCP (content planning)
    └── fetch MCP (dictionary APIs)
    |
    v
Claude Code
    ├── Agent: content-specialist.md
    └── Skill: vocabulary-generator
    |
    v
output/YYYY-MM-DD-HH-vocabulary.md (git push)
```

## Setup

### 1. Repository Secrets

| Secret | Description |
|--------|-------------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key |

### 2. Configuration

Adjust the vocabulary level and target word count by editing the workflow prompt.

### 3. Enable the Workflow

The workflow is at `.github/workflows/learning-content.yml`. It runs every 6 hours automatically, or trigger it manually from the Actions tab.

## Output Structure

Each generated file contains:

| Section | Description |
|---------|-------------|
| Word Table | Word, part of speech, pronunciation guide, definition |
| Detailed Entries | Full definitions, etymology, example sentences |
| Practice Questions | Multiple choice, fill-in-the-blank, matching exercises |
| Learning Tips | Mnemonics, word roots, related words |
| Answer Key | Answers with explanations |

## Customization

- **Difficulty Level**: Edit `references/vocabulary-guide.md` to change level criteria
- **Word Count**: Modify the prompt parameter in the workflow
- **Question Types**: Update the skill SKILL.md to add/remove question formats
- **Schedule**: Change the cron expression (default: every 6 hours)
- **Template**: Edit `assets/template.md` for different output formats
