---
name: aiox-task-yolo-toggle
description: "Use the AIOX task yolo-toggle.md inside Hermes."
version: 5.4.1
author: SynkraAI
license: MIT
platforms: [windows, macos, linux]
metadata:
  hermes:
    tags: [aiox, task, workflow]
---

# AIOX task: yolo-toggle.md

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

# yolo-toggle

**Task ID:** yolo-toggle
**Version:** 1.0.0
**Created:** 2026-02-06
**Agent:** Any agent (universal command)

---

## Purpose

Toggle the permission mode through the cycle: `ask` -> `auto` -> `explore` -> `ask`.
This task is invoked by the `*yolo` command available in all 12 agents.

---

## Task Definition (AIOX Task Format V1.0)

```yaml
task: yoloToggle()
responsável: Any Agent
responsavel_type: Agente
atomic_layer: Atom

**Entrada:**
- campo: projectRoot
  tipo: string
  origem: Context (process.cwd())
  obrigatório: false
  validação: Valid directory path

**Saída:**
- campo: newMode
  tipo: object
  destino: .aiox/config.yaml
  persistido: true
```

---

## Process

### Step 1: Load Current Mode

Read the current permission mode from `.aiox/config.yaml` under `permissions.mode`.
If the file or field does not exist, default to `ask`.

### Step 2: Cycle to Next Mode

Follow the cycle order defined in `PermissionMode.MODE_CYCLE`:

```
ask  ->  auto  ->  explore  ->  ask  (repeat)
```

### Step 3: Save New Mode

Update `.aiox/config.yaml` with the new `permissions.mode` value.
The `PermissionMode._saveToConfig()` method handles this, including creating the `.aiox/` directory if needed.

### Step 4: Display Confirmation

Show the user the new mode with its badge:

```
Permission mode changed: [icon ModeName]

  explore: Read-only mode - safe exploration (writes blocked)
  ask:     Confirm before changes - balanced approach (default)
  auto:    Full autonomy - trust mode (all operations allowed)

Current: [icon ModeName]
```

---

## Implementation

```javascript
const { cycleMode } = require('./.aiox-core/core/permissions');

async function yoloToggle() {
  const result = await cycleMode();
  console.log(result.message);
  return result;
}
```

---

## Error Handling

**Strategy:** graceful-fallback

- If `.aiox/config.yaml` cannot be read, start from default `ask` mode
- If write fails, display error and keep mode in memory only

---

## Metadata

```yaml
story: ACT-4
version: 1.0.0
dependencies:
  - .aiox-core/core/permissions/permission-mode.js
  - .aiox-core/core/permissions/index.js
tags:
  - permissions
  - mode-toggle
  - universal-command
updated_at: 2026-02-06
```

