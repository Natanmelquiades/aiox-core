---
name: aiox-task-ids-query
description: "Use the AIOX task ids-query.md inside Hermes."
version: 5.4.1
author: SynkraAI
license: MIT
platforms: [windows, macos, linux]
metadata:
  hermes:
    tags: [aiox, task, workflow]
---

# AIOX task: ids-query.md

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

## Task Definition (AIOX Task Format V1.0)

```yaml
task: idsQuery()
responsável: Any Agent
responsavel_type: Agente
atomic_layer: Molecule

**Entrada:**
- campo: intent
  tipo: string
  origem: User Input
  obrigatório: true
  validação: Non-empty string describing what is needed

- campo: context
  tipo: object
  origem: User Input
  obrigatório: false
  validação: Optional filters (type, category)

- campo: format
  tipo: string
  origem: User Input
  obrigatório: false
  validação: "json" or "text" (default: text)

**Saída:**
- campo: analysis_result
  tipo: object
  destino: Return value
  persistido: false

- campo: decision
  tipo: string
  destino: Return value
  persistido: false
```

---

## Pre-Conditions

```yaml
pre-conditions:
  - [ ] Entity Registry exists at .aiox-core/data/entity-registry.yaml
    tipo: pre-condition
    blocker: false
    validação: |
      If missing, engine returns CREATE with empty registry rationale
    error_message: "Registry not found — CREATE decisions will be recommended"
```

---

## Purpose

Query the IDS (Incremental Development System) Entity Registry to find existing artifacts that match a given intent. Returns REUSE, ADAPT, or CREATE recommendations based on semantic matching.

**Constitution Reference:** Article IV-A — REUSE > ADAPT > CREATE

---

## Usage

### CLI Usage

```bash
# Basic query
node bin/aiox-ids.js ids:query "validate story drafts"

# With JSON output
node bin/aiox-ids.js ids:query "template rendering engine" --json

# Filter by type
node bin/aiox-ids.js ids:query "database migration" --type script

# Filter by category
node bin/aiox-ids.js ids:query "agent persona" --category agents
```

### Programmatic Usage (Agent Context)

```javascript
const path = require('path');
const { RegistryLoader } = require(path.resolve('.aiox-core/core/ids/registry-loader'));
const { IncrementalDecisionEngine } = require(path.resolve('.aiox-core/core/ids/incremental-decision-engine'));

const loader = new RegistryLoader();
loader.load();

const engine = new IncrementalDecisionEngine(loader);
const result = engine.analyze('validate story drafts before implementation');

// result.summary.decision → 'REUSE' | 'ADAPT' | 'CREATE'
// result.recommendations → ranked list with rationale
// result.justification → CREATE justification (if applicable)
```

---

## Decision Interpretation

| Decision | Meaning | Action |
|----------|---------|--------|
| **REUSE** | >=90% relevance match | Use the existing artifact directly |
| **ADAPT** | 60-89% match + adaptable | Modify existing artifact (changes <30%) |
| **CREATE** | No suitable match | Create new artifact with justification |

---

## Output Structure

```yaml
intent: "validate story drafts"
recommendations:
  - entityId: "validate-story"
    decision: "REUSE"
    confidence: "high"
    relevanceScore: 0.95
    rationale: "Strong match..."
summary:
  totalEntities: 474
  matchesFound: 3
  decision: "REUSE"
  confidence: "high"
rationale: "Found 3 matches above threshold..."
```

---

## Related Commands

- `aiox ids:create-review` — Review CREATE decisions for 30-day assessment
- `*develop` — Development workflow (uses IDS recommendations at G4 gate)

---

## Metadata

```yaml
story: IDS-2
version: 1.0.0
dependencies:
  - registry-loader.js (IDS-1)
  - incremental-decision-engine.js (IDS-2)
tags:
  - ids
  - registry
  - decision-engine
updated_at: 2026-02-08
```

