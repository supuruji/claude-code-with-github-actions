---
# =============================================================================
# Agent Definition Template
# =============================================================================
# Place this file in your project's .claude/agents/ directory.
# Invoke with: /agent:<name> or by referencing the agent in conversation.
#
# Frontmatter fields:
#   name          - Display name of the agent (required)
#   description   - One-line summary shown in agent listings (required)
#   tools         - List of tools this agent is allowed to use
#   model         - Model override (optional, defaults to session model)
#   skills        - Skills this agent can invoke
#   permissionMode - "default" | "allowAll" | "denyAll"
# =============================================================================

name: "YOUR_AGENT_NAME"
description: "One-line description of what this agent does"

# Tools this agent is permitted to use.
# Common tools: Bash, Read, Write, Edit, Glob, Grep, WebFetch, WebSearch
# MCP tools: mcp__<server>__<tool> (e.g., mcp__fetch__fetch)
tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep

# Optional: Override the model for this agent.
# Uncomment to use a specific model regardless of session settings.
# model: "claude-sonnet-4-20250514"

# Optional: Skills this agent can invoke.
# Reference skills by their directory name under .claude/skills/
# skills:
#   - code-review
#   - test-generator

# Permission mode controls tool approval behavior.
#   "default"  - Follow normal permission rules (recommended)
#   "allowAll" - Skip all permission prompts (use with caution)
#   "denyAll"  - Deny all tool use (read-only agent)
permissionMode: "default"
---

# Role

Describe the agent's role clearly and concisely. What is this agent responsible
for? What domain expertise does it have?

Example:
> You are a code review specialist focused on identifying bugs, security
> vulnerabilities, and performance issues in TypeScript and Python codebases.

# When Invoked

Describe the situations where this agent should be used. This helps both the
user and the system understand the appropriate context for invoking this agent.

- When the user needs [specific task]
- When a PR requires [specific type of review]
- When the project needs [specific deliverable]

# Responsibilities

List the concrete tasks this agent performs. Be specific about inputs, processes,
and outputs.

1. **[Task Name]** - Description of what the agent does
   - Input: What it receives
   - Process: How it handles the task
   - Output: What it produces

2. **[Task Name]** - Description of what the agent does
   - Input: What it receives
   - Process: How it handles the task
   - Output: What it produces

3. **[Task Name]** - Description of what the agent does
   - Input: What it receives
   - Process: How it handles the task
   - Output: What it produces

# Output Format

Define the structure and format of the agent's output. Be explicit so results
are consistent across invocations.

```
## [Section Title]

### Findings
- [ ] Finding 1: Description
- [ ] Finding 2: Description

### Recommendations
1. Recommendation with rationale
2. Recommendation with rationale

### Summary
Brief summary of the overall assessment.
```

# Quality Standards

Define the quality criteria the agent must meet. These serve as a checklist
for the agent to self-validate its work.

- [ ] All output follows the defined format
- [ ] Every finding includes a rationale and severity level
- [ ] Recommendations are actionable and specific
- [ ] No false positives in automated checks
- [ ] Results are reproducible given the same inputs
