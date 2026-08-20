---
name: aiox-hermes-entrypoint
description: "Use for AIOX-Hermes onboarding, routing, status, doctor, bootstrap and resumable workflows."
version: 0.2.0
author: SynkraAI + Hermes adapter
license: MIT
platforms: [windows, macos, linux]
metadata:
  hermes:
    tags: [aiox, hermes, onboarding, routing, status, doctor]
---

# AIOX-Hermes Entry Point

Use this skill as the single front door for the AIOX adapter in Hermes.
The user should be able to describe an intention in natural language without
knowing `aiox-task-*`, `aiox-workflow-*` or internal file paths.

## Canonical deterministic commands

The commands below use the adapter script from the active Hermes profile when
`HERMES_HOME` is set. From the adapter source repository, use the second form.

```bash
# Dentro de um perfil Hermes instalado:
python "${HERMES_HOME}/scripts/aiox_hermes.py" help
python "${HERMES_HOME}/scripts/aiox_hermes.py" status
python "${HERMES_HOME}/scripts/aiox_hermes.py" doctor
python "${HERMES_HOME}/scripts/aiox_hermes.py" route --text "<user intention>"

# A partir do repositório-fonte do adapter:
python scripts/aiox_hermes.py help
python scripts/aiox_hermes.py status
python scripts/aiox_hermes.py doctor
python scripts/aiox_hermes.py route --text "<user intention>"
```

## Routing contract

1. Read the current project state before proposing implementation.
2. Use `route --text` as a deterministic hint, never as a replacement for judgment.
3. Load the role skill selected by the route:
   - product/requirements → `aiox-agent-pm` or `aiox-agent-analyst`;
   - architecture → `aiox-agent-architect`;
   - story/backlog → `aiox-agent-sm` or `aiox-agent-po`;
   - implementation → `aiox-agent-dev`;
   - QA/review/security → `aiox-agent-qa`;
   - repository/release → `aiox-agent-devops`.
4. Keep the active role, workflow, artifact and next step visible in the response.
5. Use `todo` for multi-step progress and `delegate_task` only for isolated work.
6. Use `.aiox/hermes/active-run.json` for resumable story/workflow state.

## First-value recipes

- "Quero criar uma feature" → plan → story → development → QA.
- "Quero corrigir um bug" → brownfield assessment → story → development → regression QA.
- "Quero saber o status" → status → active run → next step.
- "Quero verificar a instalação" → doctor → actionable remediation.
- "Quero atualizar o AIOX" → sync-check → show provenance/diff; never apply silently.

## Safety and portability

- `*comando` names are workflow labels, not native Hermes slash commands.
- Never claim a Codex, Claude or Gemini hook ran in Hermes.
- Never create `.claude`, `.codex`, `.gemini`, Cursor settings or IDE hooks automatically.
- Do not execute scripts downloaded from upstream during a check.
- Do not modify project files until the story, scope and approval gate allow it.
- Do not mark a story complete without real validation output.
