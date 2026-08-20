---
name: aiox-task-orchestrate
description: "Use the AIOX task orchestrate.md inside Hermes."
version: 5.4.1
author: SynkraAI
license: MIT
platforms: [windows, macos, linux]
metadata:
  hermes:
    tags: [aiox, task, workflow]
---

# AIOX task: orchestrate.md

This is the Hermes adaptation wrapper for the original AIOX task.

## Hermes adaptation rules

- Treat AIOX `*command` names as intent labels; do not assume Hermes has that slash command.
- Use Hermes-native tools: `file`, `terminal`, `coding`, `web`, `browser`, `computer_use`, `delegation`, `todo`, `cronjob` and `clarify`.
- Preserve original project artifacts and paths unless the user explicitly asks for a migration.
- Do not install IDE-specific hooks or write `.claude`, `.codex`, `.gemini` or Cursor settings automatically.
- Follow the original elicitation, blocking, validation and completion rules.
- Verify every named acceptance criterion before reporting completion.

## Original AIOX task

The source is preserved verbatim below for fidelity and auditability.

---

---
title: Orchestrate Pipeline
description: Start full ADE pipeline for a story
agent: aiox-master
version: 1.0.0
story: '0.9'
epic: '0'
---

# \*orchestrate Command

Starts the ADE Master Orchestrator pipeline for a given story.

## Usage

```
*orchestrate {story-id} [options]
```

## Options

- `--epic N` - Start from specific epic (3, 4, 6, or 7)
- `--dry-run` - Preview pipeline without execution
- `--strict` - Enable strict gate mode (any failure = halt)

## Examples

```bash
# Full pipeline
*orchestrate STORY-42

# Start from Epic 4
*orchestrate STORY-42 --epic 4

# Preview only
*orchestrate STORY-42 --dry-run

# Strict mode
*orchestrate STORY-42 --strict
```

## Behavior

1. Validates story ID
2. Initializes MasterOrchestrator
3. Detects tech stack (pre-flight)
4. Executes epics in sequence: 3 → 4 → 6 → 7
5. Evaluates quality gates between epics
6. Handles errors with automatic recovery
7. Saves state for resume capability
8. Updates dashboard status

## Output

- Real-time progress in terminal
- Dashboard status at `.aiox/dashboard/status.json`
- State saved at `.aiox/master-orchestrator/{story-id}.json`
- Logs at `.aiox/logs/{story-id}.log`

## Exit Codes

- 0: Success
- 1: Pipeline failed
- 2: Pipeline blocked (gate failure)
- 3: Invalid arguments

