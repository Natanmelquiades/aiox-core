---
name: aiox-task-cleanup-worktrees
description: "Use the AIOX task cleanup-worktrees.md inside Hermes."
version: 5.4.1
author: SynkraAI
license: MIT
platforms: [windows, macos, linux]
metadata:
  hermes:
    tags: [aiox, task, workflow]
---

# AIOX task: cleanup-worktrees.md

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

# cleanup-worktrees

Remove all stale git worktrees older than specified threshold.

## Purpose

Clean up abandoned worktrees to maintain repository hygiene.

## Usage

```bash
*cleanup-worktrees [--days=30]
```

## Parameters

- `--days` - Age threshold in days (default: 30)

## Steps

1. List all worktrees: `git worktree list`
2. Identify stale worktrees (no commits > threshold)
3. Present list for user confirmation
4. For each approved worktree:
   - Remove worktree: `git worktree remove {path}`
   - Delete branch if merged: `git branch -d {branch}`
5. Report cleanup summary

## Safety Checks

- Never remove worktree with uncommitted changes
- Always confirm with user before deletion
- Keep worktrees with recent activity

## Related

- `*list-worktrees` - List all worktrees
- `*remove-worktree` - Remove single worktree
- `*create-worktree` - Create new worktree

