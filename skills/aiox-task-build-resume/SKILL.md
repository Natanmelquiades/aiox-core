---
name: aiox-task-build-resume
description: "Use the AIOX task build-resume.md inside Hermes."
version: 5.4.1
author: SynkraAI
license: MIT
platforms: [windows, macos, linux]
metadata:
  hermes:
    tags: [aiox, task, workflow]
---

# AIOX task: build-resume.md

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

# Task: Build Resume

> **Command:** `*build-resume {story-id}`
> **Agent:** @dev
> **Story:** 8.4 - Build Recovery & Resume
> **AC:** AC3

---

## Purpose

Resume an autonomous build from its last checkpoint after failure or interruption.

---

## Usage

```bash
*build-resume {story-id}
```

### Arguments

| Argument | Required | Description                          |
| -------- | -------- | ------------------------------------ |
| story-id | Yes      | Story identifier (e.g., "story-8.4") |

---

## Workflow

```yaml
steps:
  - name: Load Build State
    action: |
      Load build state from plan/build-state.json
      Verify state exists and is resumable
    validates:
      - State file exists
      - Status is not "completed"

  - name: Get Last Checkpoint
    action: |
      Identify last successful checkpoint
      Determine next subtask to execute
    outputs:
      - lastCheckpoint
      - nextSubtask
      - completedSubtasks

  - name: Restore Context
    action: |
      - Verify worktree still exists (if applicable)
      - Load implementation plan
      - Restore current position
    validates:
      - Worktree accessible
      - Plan file exists

  - name: Update State
    action: |
      - Set status to "in_progress"
      - Clear abandoned flags
      - Add resume notification

  - name: Display Resume Summary
    action: |
      Show:
      - Story ID
      - Last checkpoint ID
      - Completed subtasks count
      - Next subtask to execute
      - Worktree path (if any)

  - name: Continue Execution
    action: |
      Resume autonomous build loop from next subtask
      (Integrates with *build-autonomous command)
```

---

## Output Example

```
✓ Resumed build for story-8.4

  From checkpoint: cp-lxyz123-abc456
  Completed: 4 subtasks
  Next subtask: 2.3
  Worktree: .worktrees/story-8.4

Build resuming...
```

---

## Error Handling

| Error                   | Resolution                                 |
| ----------------------- | ------------------------------------------ |
| No build state found    | Run `*build {story-id}` to start new build |
| Build already completed | Cannot resume completed build              |
| Worktree missing        | Recreate worktree or start fresh           |
| Invalid checkpoint      | Try previous checkpoint or start fresh     |

---

## Integration

- **Uses:** `BuildStateManager.resumeBuild()`
- **Requires:** `plan/build-state.json`
- **Updates:** State status, notifications, attempt log

---

## Related Commands

- `*build-status {story-id}` - Check build status
- `*build {story-id}` - Start new build
- `*build-log {story-id}` - View attempt log

---

_Task file for Story 8.4 - Build Recovery & Resume_

