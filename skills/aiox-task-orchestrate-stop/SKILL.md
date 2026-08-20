---
name: aiox-task-orchestrate-stop
description: "Use the AIOX task orchestrate-stop.md inside Hermes."
version: 5.4.1
author: SynkraAI
license: MIT
platforms: [windows, macos, linux]
metadata:
  hermes:
    tags: [aiox, task, workflow]
---

# AIOX task: orchestrate-stop.md

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
title: Orchestrate Stop
description: Stop orchestrator execution for a story
agent: aiox-master
version: 1.0.0
story: '0.9'
epic: '0'
---

# \*orchestrate-stop Command

Stops the orchestrator execution for a story.

## Usage

```
*orchestrate-stop {story-id}
```

## Examples

```bash
# Stop STORY-42 execution
*orchestrate-stop STORY-42
```

## Output

```
🛑 Stopping orchestrator for STORY-42...

Current state: in_progress
Current epic: 4

Saving state for resume...
State saved at: .aiox/master-orchestrator/STORY-42.json

✅ Orchestrator stopped successfully.
   Run *orchestrate-resume STORY-42 to continue.
```

## Behavior

1. Locates running orchestrator for story
2. Gracefully stops current epic execution
3. Saves current state for resume
4. Updates dashboard status to "stopped"
5. Sends notification

## Exit Codes

- 0: Success
- 1: Story not found or not running
- 3: Invalid arguments

