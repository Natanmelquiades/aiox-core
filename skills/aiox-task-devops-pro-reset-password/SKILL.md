---
name: aiox-task-devops-pro-reset-password
description: "Use the AIOX task devops-pro-reset-password.md inside Hermes."
version: 5.4.1
author: SynkraAI
license: MIT
platforms: [windows, macos, linux]
metadata:
  hermes:
    tags: [aiox, task, workflow]
---

# AIOX task: devops-pro-reset-password.md

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

# Task: DevOps Pro Reset Password

> **Version:** 1.0.0
> **Created:** 2026-04-20
> **Type:** SUPPORT-OPS
> **Agent:** `@devops`

## Purpose

Reset an AIOX Pro password administratively, then validate login with the new password.

## Inputs

- `target_email`
- `new_password`

## Execution

1. Ensure the auth user exists for the target email.
2. Update the password in Supabase Auth.
3. Ensure the email remains confirmed.
4. Validate the new password with `login`.

## Pass Criteria

- auth user password updated successfully
- `POST /api/v1/auth/login` returns `200` and `accessToken`

## Recommended Follow-Up

- if the request was really a recovery flow for the user, also offer `*pro-request-reset {email}`

## Source Of Truth

- `docs/guides/pro/access-grant-ops-playbook.md`
- `.aiox-core/development/tasks/devops-pro-access-grant.md`

