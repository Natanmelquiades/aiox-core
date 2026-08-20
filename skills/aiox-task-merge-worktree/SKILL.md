---
name: aiox-task-merge-worktree
description: "Use the AIOX task merge-worktree.md inside Hermes."
version: 5.4.1
author: SynkraAI
license: MIT
platforms: [windows, macos, linux]
metadata:
  hermes:
    tags: [aiox, task, workflow]
---

# AIOX task: merge-worktree.md

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

# merge-worktree

Merge a worktree branch back to its base branch.

## Purpose

Complete worktree workflow by merging changes back to base branch.

## Usage

```bash
*merge-worktree {worktree-name}
```

## Parameters

- `worktree-name` - Name of the worktree to merge

## Steps

1. Verify worktree exists: `git worktree list`
2. Run quality gates on worktree branch:
   - `npm run lint`
   - `npm test`
   - `npm run typecheck`
3. Checkout base branch: `git checkout {base-branch}`
4. Merge worktree branch: `git merge {worktree-branch}`
5. Handle conflicts if any (with user assistance)
6. Push merged changes: delegate to `*push`
7. Optionally remove worktree: `*remove-worktree`

## Safety

- Quality gates must pass before merge
- User confirms merge direction
- Conflict resolution requires user input

## Related

- `*create-worktree` - Create worktree
- `*remove-worktree` - Remove worktree
- `*push` - Push merged changes

