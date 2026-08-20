---
name: aiox-task-remove-mcp
description: "Use the AIOX task remove-mcp.md inside Hermes."
version: 5.4.1
author: SynkraAI
license: MIT
platforms: [windows, macos, linux]
metadata:
  hermes:
    tags: [aiox, task, workflow]
---

# AIOX task: remove-mcp.md

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

# remove-mcp

Remove an MCP server from Docker MCP Toolkit.

## Purpose

Disable and remove an MCP server from the toolkit configuration.

## Usage

```bash
*remove-mcp {server-name}
```

## Parameters

- `server-name` - Name of the MCP server to remove

## Steps

1. Verify server exists: `docker mcp tools ls`
2. Confirm with user before removal
3. Remove server: `docker mcp server remove {server-name}`
4. Verify removal: `docker mcp tools ls`

## Safety

- Always confirm before removing
- Check if server is in use by other configurations
- Document removal in session notes

## Related

- `*list-mcps` - List enabled MCPs
- `*add-mcp` - Add MCP server

