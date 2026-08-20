---
name: aiox-task-ids-health
description: "Use the AIOX task ids-health.md inside Hermes."
version: 5.4.1
author: SynkraAI
license: MIT
platforms: [windows, macos, linux]
metadata:
  hermes:
    tags: [aiox, task, workflow]
---

# AIOX task: ids-health.md

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

# IDS Registry Health Check Task

## Purpose

Run a self-healing health check on the IDS entity registry to detect and auto-fix data integrity issues.

---

## Pre-Conditions

- Entity registry exists at `.aiox-core/data/entity-registry.yaml`
- IDS modules are installed (IDS-1, IDS-3, IDS-4a)

---

## Execution

### Step 1: Run Health Check

```bash
node bin/aiox-ids.js ids:health
```

Review the output for any detected issues.

### Step 2: Auto-Heal (Optional)

If auto-fixable issues are detected, run with `--fix`:

```bash
node bin/aiox-ids.js ids:health --fix
```

This will:
- Create a backup of the registry before changes
- Auto-fix issues: checksum mismatches, orphaned references, missing keywords, stale timestamps
- Skip non-auto-healable issues (missing files) and emit warnings
- Log all healing actions to `.aiox-core/data/registry-healing-log.jsonl`

### Step 3: JSON Output (Machine-Readable)

```bash
node bin/aiox-ids.js ids:health --json
node bin/aiox-ids.js ids:health --fix --json
```

### Step 4: Review Warnings

If critical issues are found (missing files), the command exits with code 1.
Review the warnings and take manual action as suggested.

---

## Post-Conditions

- Registry integrity issues are detected and reported
- Auto-healable issues are fixed (with --fix)
- Non-auto-healable issues generate warnings with suggested actions
- Healing actions are logged for audit trail
- Registry backup is created before any modifications

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | No critical issues |
| 1 | Critical issues found (e.g., missing files) |

---

## Programmatic Usage

```javascript
const { RegistryHealer } = require('.aiox-core/core/ids/registry-healer');

const healer = new RegistryHealer();
const healthResult = healer.runHealthCheck();

if (healthResult.summary.total > 0) {
  const healResult = healer.heal(healthResult.issues, { autoOnly: true });
  console.log(`Healed: ${healResult.healed.length}, Skipped: ${healResult.skipped.length}`);
}
```

---

*Story IDS-4a | Self-Healing Data Integrity*

