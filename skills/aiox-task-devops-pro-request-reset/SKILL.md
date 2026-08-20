---
name: aiox-task-devops-pro-request-reset
description: "Use the AIOX task devops-pro-request-reset.md inside Hermes."
version: 5.4.1
author: SynkraAI
license: MIT
platforms: [windows, macos, linux]
metadata:
  hermes:
    tags: [aiox, task, workflow]
---

# AIOX task: devops-pro-request-reset.md

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

# Task: DevOps Pro Request Reset

> **Version:** 1.0.0
> **Created:** 2026-04-20
> **Type:** SUPPORT-OPS
> **Agent:** `@devops`

## Purpose

Trigger the user-facing password reset email flow for an AIOX Pro account.

## Input

- `target_email`

## Endpoint

- `POST https://aiox-license-server.vercel.app/api/v1/auth/request-reset`

## Execution

1. Call `request-reset` with the target email.
2. Report the HTTP status.
3. Treat the generic success message as expected anti-enumeration behavior.
4. If the endpoint returns `429`, report the rate limit window.

## Pass Criteria

- request returns `200` with the generic message
- or a clear `429` with retry guidance

## Source Of Truth

- `docs/guides/pro/access-grant-ops-playbook.md`

