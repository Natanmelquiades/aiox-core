---
name: aiox-task-devops-pro-verify-status
description: "Use the AIOX task devops-pro-verify-status.md inside Hermes."
version: 5.4.1
author: SynkraAI
license: MIT
platforms: [windows, macos, linux]
metadata:
  hermes:
    tags: [aiox, task, workflow]
---

# AIOX task: devops-pro-verify-status.md

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

# Task: DevOps Pro Verify Status

> **Version:** 1.0.0
> **Created:** 2026-04-20
> **Type:** SUPPORT-OPS
> **Agent:** `@devops`

## Purpose

Check email verification status for an authenticated AIOX Pro session.

## Input

- `access_token`

## Endpoint

- `POST https://aiox-license-server.vercel.app/api/v1/auth/verify-status`

## Execution

1. Call `verify-status` with `{ accessToken }`.
2. Report `email` and `emailVerified`.
3. If `emailVerified=false`, route to `*pro-resend-verification`.

## Pass Criteria

- `200` response
- clear verified/unverified state

## Source Of Truth

- `docs/guides/pro/access-grant-ops-playbook.md`

