---
name: aiox-task-devops-pro-activate
description: "Use the AIOX task devops-pro-activate.md inside Hermes."
version: 5.4.1
author: SynkraAI
license: MIT
platforms: [windows, macos, linux]
metadata:
  hermes:
    tags: [aiox, task, workflow]
---

# AIOX task: devops-pro-activate.md

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

# Task: DevOps Pro Activate

> **Version:** 1.0.0
> **Created:** 2026-04-20
> **Type:** SUPPORT-OPS
> **Agent:** `@devops`

## Purpose

Call the live `activate-pro` endpoint directly to validate or restore AIOX Pro activation for a session.

## Inputs

- `access_token`
- `machine_id` (optional, default: `ops-validation-machine`)
- `version` (optional, default: current installer version)

## Endpoint

- `POST https://aiox-license-server.vercel.app/api/v1/auth/activate-pro`

## Execution

1. Build the request body with:
   - `accessToken`
   - `machineId`
   - `version`
   - `aioxCoreVersion`
2. Call `activate-pro`.
3. Report:
   - HTTP status
   - `activated`
   - whether activation was new or restored
4. Never paste the full `licenseKey` into logs or tickets.

## Pass Criteria

- `201` on first activation or `200` on idempotent restore

## Source Of Truth

- `docs/guides/pro/access-grant-ops-playbook.md`

