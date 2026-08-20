---
name: aiox-task-devops-pro-check-access
description: "Use the AIOX task devops-pro-check-access.md inside Hermes."
version: 5.4.1
author: SynkraAI
license: MIT
platforms: [windows, macos, linux]
metadata:
  hermes:
    tags: [aiox, task, workflow]
---

# AIOX task: devops-pro-check-access.md

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

# Task: DevOps Pro Check Access

> **Version:** 1.0.0
> **Created:** 2026-04-20
> **Type:** SUPPORT-OPS
> **Agent:** `@devops`

## Purpose

Check whether an email already has AIOX Pro buyer entitlement and whether an auth account exists.

## Input

- `target_email`

## Endpoint

- `POST https://aiox-license-server.vercel.app/api/v1/auth/check-email`

## Execution

1. Call `check-email` with the target email.
2. Report `isBuyer`, `hasAccount`, and normalized `email`.
3. If `isBuyer=false`, recommend `*pro-access-grant`.
4. If `isBuyer=true` and `hasAccount=false`, recommend account creation or `*pro-access-grant`.

## Pass Criteria

- request returns `200`
- response clearly identifies buyer/account state

## Source Of Truth

- `docs/guides/pro/access-grant-ops-playbook.md`

