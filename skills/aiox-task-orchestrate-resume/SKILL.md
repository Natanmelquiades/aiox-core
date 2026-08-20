---
name: aiox-task-orchestrate-resume
description: "Use the AIOX task orchestrate-resume.md inside Hermes."
version: 5.4.1
author: SynkraAI
license: MIT
platforms: [windows, macos, linux]
metadata:
  hermes:
    tags: [aiox, task, workflow]
---

# AIOX task: orchestrate-resume.md

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
title: Orchestrate Resume
description: Resume orchestrator execution from saved state
agent: aiox-master
version: 1.0.0
story: '0.9'
epic: '0'
---

# \*orchestrate-resume Command

Resumes orchestrator execution from the last saved state.

## Usage

```
*orchestrate-resume {story-id}
```

## Examples

```bash
# Resume STORY-42 from where it stopped
*orchestrate-resume STORY-42
```

## Output

```
🔄 Resuming orchestrator for STORY-42...

Loading state from: .aiox/master-orchestrator/STORY-42.json

Previous state:
  Status: stopped
  Last Epic: 4 (Execution Engine)
  Progress: 45%
  Stopped at: 2026-01-29 11:30:00

Resuming from Epic 4...

⏳ Continuing Epic 4: Execution Engine
...
```

## Behavior

1. Loads saved state from `.aiox/master-orchestrator/{story-id}.json`
2. Validates state is resumable (not completed, not corrupted)
3. Restores orchestrator to previous state
4. Continues execution from last completed epic
5. Updates dashboard status to "in_progress"

## Exit Codes

- 0: Success
- 1: No saved state found
- 2: State is not resumable (completed or corrupted)
- 3: Invalid arguments

