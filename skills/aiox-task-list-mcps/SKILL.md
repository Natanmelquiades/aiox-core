---
name: aiox-task-list-mcps
description: "Use the AIOX task list-mcps.md inside Hermes."
version: 5.4.1
author: SynkraAI
license: MIT
platforms: [windows, macos, linux]
metadata:
  hermes:
    tags: [aiox, task, workflow]
---

# AIOX task: list-mcps.md

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

# list-mcps

List currently enabled MCP servers and their available tools.

## Purpose

Display all MCP servers configured in Docker MCP Toolkit with their status and tools.

## Usage

```bash
*list-mcps
```

## Output

Shows:
- Server name and status (enabled/disabled)
- Available tools per server
- Connection status

## Implementation

Uses Docker MCP Toolkit CLI:
```bash
docker mcp tools ls
```

## Related

- `*add-mcp` - Add new MCP server
- `*remove-mcp` - Remove MCP server
- `*search-mcp` - Search MCP catalog

