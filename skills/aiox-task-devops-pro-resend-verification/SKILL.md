---
name: aiox-task-devops-pro-resend-verification
description: "Use the AIOX task devops-pro-resend-verification.md inside Hermes."
version: 5.4.1
author: SynkraAI
license: MIT
platforms: [windows, macos, linux]
metadata:
  hermes:
    tags: [aiox, task, workflow]
---

# AIOX task: devops-pro-resend-verification.md

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

# Task: DevOps Pro Resend Verification

> **Version:** 1.0.0
> **Created:** 2026-04-20
> **Type:** SUPPORT-OPS
> **Agent:** `@devops`

## Purpose

Resend the email verification link for an AIOX Pro user account.

## Input

- `target_email`

## Endpoint

- `POST https://aiox-license-server.vercel.app/api/v1/auth/resend-verification`

## Execution

1. Call `resend-verification` with the target email.
2. Report status and generic delivery message.
3. If `429`, report resend rate limit and retry guidance.

## Pass Criteria

- endpoint returns success-style response without leaking account existence

## Source Of Truth

- `docs/guides/pro/access-grant-ops-playbook.md`

