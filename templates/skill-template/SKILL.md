---
# =============================================================================
# Skill Definition Template
# =============================================================================
# Place this file as SKILL.md inside a directory under .claude/skills/.
# The directory name becomes the skill identifier.
#
# Directory structure:
#   .claude/skills/<skill-name>/
#   ├── SKILL.md          # This file (required)
#   ├── assets/           # Static assets (templates, configs, etc.)
#   ├── references/       # Reference documents and examples
#   └── scripts/          # Helper scripts the skill can invoke
#
# Frontmatter fields:
#   name        - Display name of the skill (required)
#   description - One-line summary shown in skill listings (required)
#   version     - Semantic version of this skill definition
#   tags        - Searchable tags for discovery
#   author      - Who created/maintains this skill
# =============================================================================

name: "YOUR_SKILL_NAME"
description: "One-line description of what this skill does"
version: "1.0.0"
tags:
  - tag1
  - tag2
  - tag3
# author: "your-name"
---

# Overview

Provide a clear, concise description of what this skill does. Include the
problem it solves and the value it provides.

Example:
> This skill generates comprehensive test suites for TypeScript modules. It
> analyzes the module's exports, identifies edge cases, and produces tests
> using the project's existing test framework.

# When to Use

Describe the specific situations where this skill should be invoked. Be precise
so that both agents and users know when this skill is appropriate.

- **Use when:** [specific trigger condition]
- **Use when:** [specific trigger condition]
- **Do not use when:** [condition where this skill is inappropriate]

# Workflow

Define the step-by-step process this skill follows. Each step should be
discrete and verifiable.

## Step 1: [Name]

Description of what happens in this step.

- **Input:** What this step receives
- **Action:** What this step does
- **Output:** What this step produces
- **Validation:** How to verify this step succeeded

## Step 2: [Name]

Description of what happens in this step.

- **Input:** What this step receives
- **Action:** What this step does
- **Output:** What this step produces
- **Validation:** How to verify this step succeeded

## Step 3: [Name]

Description of what happens in this step.

- **Input:** What this step receives
- **Action:** What this step does
- **Output:** What this step produces
- **Validation:** How to verify this step succeeded

# Quality Standards

Define measurable quality criteria for the skill's output.

| Criterion | Requirement | How to Verify |
|-----------|------------|---------------|
| Completeness | All required sections are present | Checklist review |
| Accuracy | Output is factually correct | Cross-reference with source |
| Format | Follows the defined output structure | Schema validation |
| Idempotency | Running twice produces same result | Re-run comparison |

# Resources

List assets, references, and scripts that support this skill.

## Assets (`assets/`)

Files in the assets directory that this skill uses:

| File | Purpose |
|------|---------|
| `template.txt` | Output template |
| `config.json` | Default configuration |

## References (`references/`)

Reference documents for context and examples:

| File | Purpose |
|------|---------|
| `example-output.md` | Example of expected output |
| `style-guide.md` | Style guidelines to follow |

## Scripts (`scripts/`)

Helper scripts that can be invoked during the workflow:

| Script | Purpose | Usage |
|--------|---------|-------|
| `validate.sh` | Validates skill output | `bash scripts/validate.sh <output-file>` |
| `setup.sh` | Prepares the environment | `bash scripts/setup.sh` |
