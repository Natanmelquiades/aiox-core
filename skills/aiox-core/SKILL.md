---
name: aiox-core
description: "Use the Synkra AIOX framework adapted for Hermes: agents, tasks, workflows and artifacts."
version: 5.4.1
author: SynkraAI + Hermes adapter
license: MIT
platforms: [windows, macos, linux]
metadata:
  hermes:
    tags: [aiox, orchestration, agile, stories, planning, development, qa]
---

# Synkra AIOX Core on Hermes

This bundle brings AIOX Core 5.4.1 into Hermes without copying IDE-specific
Claude/Codex/Gemini/Cursor hooks. In this upstream-based fork the source of
truth is the repository root and `.aiox-core/`.

## Native mapping

| AIOX | Hermes |
|---|---|
| Agent definition | role skill and optional Hermes Bot profile |
| `*command` | task/workflow skill selected by intent |
| Task markdown | individual `aiox-task-*` skill |
| Workflow YAML | `aiox-workflow-*` skill |
| Agent memory | Hermes profile memory + `SOUL.md` |
| AIOX `.aiox/` artifacts | project files, loaded through Hermes context/skills |
| IDE hooks | not copied; use Hermes hooks/tools instead |
| MCP | configure with Hermes `hermes mcp`, not `.claude/mcp.json` |

## Role roster

- `aiox-agent-aiox-master` — Orion (AIOX Master Orchestrator & Framework Developer)
- `aiox-agent-analyst` — Atlas (Business Analyst)
- `aiox-agent-architect` — Aria (Architect)
- `aiox-agent-data-engineer` — Dara (Database Architect & Operations Engineer)
- `aiox-agent-dev` — Dex (Full Stack Developer)
- `aiox-agent-devops` — Gage (GitHub Repository Manager & DevOps Specialist)
- `aiox-agent-pm` — Morgan (Product Manager)
- `aiox-agent-po` — Pax (Product Owner)
- `aiox-agent-qa` — Quinn (Test Architect & Quality Advisor)
- `aiox-agent-sm` — River (Scrum Master)
- `aiox-agent-squad-creator` — Craft (Squad Creator)
- `aiox-agent-ux-design-expert` — Uma (UX/UI Designer & Design System Architect)

## Execution policy

When the user asks for an AIOX command, identify the corresponding task or
workflow skill, load it, inspect the project, and execute its steps with Hermes
native tools. Preserve elicitation and validation gates. Never claim an AIOX hook
ran unless a real Hermes tool result proves the equivalent.

## Original source

- AIOX source: repository root (`.aiox-core/`, `bin/`, `packages/`)
- Version: 5.4.1
- License: MIT (retain copyright notices when redistributing)

## Generated task inventory

- `aiox-task-add-mcp` ← `add-mcp.md`
- `aiox-task-advanced-elicitation` ← `advanced-elicitation.md`
- `aiox-task-analyst-facilitate-brainstorming` ← `analyst-facilitate-brainstorming.md`
- `aiox-task-analyze-brownfield` ← `analyze-brownfield.md`
- `aiox-task-analyze-cross-artifact` ← `analyze-cross-artifact.md`
- `aiox-task-analyze-framework` ← `analyze-framework.md`
- `aiox-task-analyze-performance` ← `analyze-performance.md`
- `aiox-task-analyze-project-structure` ← `analyze-project-structure.md`
- `aiox-task-apply-qa-fixes` ← `apply-qa-fixes.md`
- `aiox-task-architect-analyze-impact` ← `architect-analyze-impact.md`
- `aiox-task-audit-codebase` ← `audit-codebase.md`
- `aiox-task-audit-tailwind-config` ← `audit-tailwind-config.md`
- `aiox-task-audit-utilities` ← `audit-utilities.md`
- `aiox-task-blocks-agent-prompt-template` ← `blocks/agent-prompt-template.md`
- `aiox-task-blocks-context-loading` ← `blocks/context-loading.md`
- `aiox-task-blocks-execution-pattern` ← `blocks/execution-pattern.md`
- `aiox-task-blocks-finalization` ← `blocks/finalization.md`
- `aiox-task-blocks-readme` ← `blocks/README.md`
- `aiox-task-bootstrap-shadcn-library` ← `bootstrap-shadcn-library.md`
- `aiox-task-brownfield-create-epic` ← `brownfield-create-epic.md`
- `aiox-task-brownfield-create-story` ← `brownfield-create-story.md`
- `aiox-task-build-autonomous` ← `build-autonomous.md`
- `aiox-task-build-component` ← `build-component.md`
- `aiox-task-build-resume` ← `build-resume.md`
- `aiox-task-build-status` ← `build-status.md`
- `aiox-task-build` ← `build.md`
- `aiox-task-calculate-roi` ← `calculate-roi.md`
- `aiox-task-check-docs-links` ← `check-docs-links.md`
- `aiox-task-ci-cd-configuration` ← `ci-cd-configuration.md`
- `aiox-task-cleanup-utilities` ← `cleanup-utilities.md`
- `aiox-task-cleanup-worktrees` ← `cleanup-worktrees.md`
- `aiox-task-collaborative-edit` ← `collaborative-edit.md`
- `aiox-task-compose-molecule` ← `compose-molecule.md`
- `aiox-task-consolidate-patterns` ← `consolidate-patterns.md`
- `aiox-task-correct-course` ← `correct-course.md`
- `aiox-task-create-agent` ← `create-agent.md`
- `aiox-task-create-brownfield-story` ← `create-brownfield-story.md`
- `aiox-task-create-deep-research-prompt` ← `create-deep-research-prompt.md`
- `aiox-task-create-doc` ← `create-doc.md`
- `aiox-task-create-next-story` ← `create-next-story.md`
- `aiox-task-create-service` ← `create-service.md`
- `aiox-task-create-suite` ← `create-suite.md`
- `aiox-task-create-task` ← `create-task.md`
- `aiox-task-create-workflow` ← `create-workflow.md`
- `aiox-task-create-worktree` ← `create-worktree.md`
- `aiox-task-db-analyze-hotpaths` ← `db-analyze-hotpaths.md`
- `aiox-task-db-apply-migration` ← `db-apply-migration.md`
- `aiox-task-db-bootstrap` ← `db-bootstrap.md`
- `aiox-task-db-domain-modeling` ← `db-domain-modeling.md`
- `aiox-task-db-dry-run` ← `db-dry-run.md`
- `aiox-task-db-env-check` ← `db-env-check.md`
- `aiox-task-db-explain` ← `db-explain.md`
- `aiox-task-db-impersonate` ← `db-impersonate.md`
- `aiox-task-db-load-csv` ← `db-load-csv.md`
- `aiox-task-db-policy-apply` ← `db-policy-apply.md`
- `aiox-task-db-rls-audit` ← `db-rls-audit.md`
- `aiox-task-db-rollback` ← `db-rollback.md`
- `aiox-task-db-run-sql` ← `db-run-sql.md`
- `aiox-task-db-schema-audit` ← `db-schema-audit.md`
- `aiox-task-db-seed` ← `db-seed.md`
- `aiox-task-db-smoke-test` ← `db-smoke-test.md`
- `aiox-task-db-snapshot` ← `db-snapshot.md`
- `aiox-task-db-squad-integration` ← `db-squad-integration.md`
- `aiox-task-db-supabase-setup` ← `db-supabase-setup.md`
- `aiox-task-db-verify-order` ← `db-verify-order.md`
- `aiox-task-delegate-to-external-executor` ← `delegate-to-external-executor.md`
- `aiox-task-deprecate-component` ← `deprecate-component.md`
- `aiox-task-dev-apply-qa-fixes` ← `dev-apply-qa-fixes.md`
- `aiox-task-dev-backlog-debt` ← `dev-backlog-debt.md`
- `aiox-task-dev-develop-story` ← `dev-develop-story.md`
- `aiox-task-dev-improve-code-quality` ← `dev-improve-code-quality.md`
- `aiox-task-dev-optimize-performance` ← `dev-optimize-performance.md`
- `aiox-task-dev-suggest-refactoring` ← `dev-suggest-refactoring.md`
- `aiox-task-dev-validate-next-story` ← `dev-validate-next-story.md`
- `aiox-task-devops-pro-access-grant` ← `devops-pro-access-grant.md`
- `aiox-task-devops-pro-activate` ← `devops-pro-activate.md`
- `aiox-task-devops-pro-check-access` ← `devops-pro-check-access.md`
- `aiox-task-devops-pro-request-reset` ← `devops-pro-request-reset.md`
- `aiox-task-devops-pro-resend-verification` ← `devops-pro-resend-verification.md`
- `aiox-task-devops-pro-reset-password` ← `devops-pro-reset-password.md`
- `aiox-task-devops-pro-validate-login` ← `devops-pro-validate-login.md`
- `aiox-task-devops-pro-verify-status` ← `devops-pro-verify-status.md`
- `aiox-task-document-gotchas` ← `document-gotchas.md`
- `aiox-task-document-project` ← `document-project.md`
- `aiox-task-environment-bootstrap` ← `environment-bootstrap.md`
- `aiox-task-execute-checklist` ← `execute-checklist.md`
- `aiox-task-execute-epic-plan` ← `execute-epic-plan.md`
- `aiox-task-export-design-tokens-dtcg` ← `export-design-tokens-dtcg.md`
- `aiox-task-extend-pattern` ← `extend-pattern.md`
- `aiox-task-extract-patterns` ← `extract-patterns.md`
- `aiox-task-extract-tokens` ← `extract-tokens.md`
- `aiox-task-facilitate-brainstorming-session` ← `facilitate-brainstorming-session.md`
- `aiox-task-fast-path-gate` ← `fast-path-gate.md`
- `aiox-task-generate-ai-frontend-prompt` ← `generate-ai-frontend-prompt.md`
- `aiox-task-generate-documentation` ← `generate-documentation.md`
- `aiox-task-generate-migration-strategy` ← `generate-migration-strategy.md`
- `aiox-task-generate-shock-report` ← `generate-shock-report.md`
- `aiox-task-github-devops-github-pr-automation` ← `github-devops-github-pr-automation.md`
- `aiox-task-github-devops-pre-push-quality-gate` ← `github-devops-pre-push-quality-gate.md`
- `aiox-task-github-devops-repository-cleanup` ← `github-devops-repository-cleanup.md`
- `aiox-task-github-devops-version-management` ← `github-devops-version-management.md`
- `aiox-task-github-issue-triage` ← `github-issue-triage.md`
- `aiox-task-gotcha` ← `gotcha.md`
- `aiox-task-gotchas` ← `gotchas.md`
- `aiox-task-health-check` ← `health-check.yaml`
- `aiox-task-ids-governor` ← `ids-governor.md`
- `aiox-task-ids-health` ← `ids-health.md`
- `aiox-task-ids-query` ← `ids-query.md`
- `aiox-task-improve-self` ← `improve-self.md`
- `aiox-task-index-docs` ← `index-docs.md`
- `aiox-task-init-project-status` ← `init-project-status.md`
- `aiox-task-integrate-squad` ← `integrate-squad.md`
- `aiox-task-kb-mode-interaction` ← `kb-mode-interaction.md`
- `aiox-task-learn-patterns` ← `learn-patterns.md`
- `aiox-task-list-mcps` ← `list-mcps.md`
- `aiox-task-list-worktrees` ← `list-worktrees.md`
- `aiox-task-mcp-workflow` ← `mcp-workflow.md`
- `aiox-task-merge-worktree` ← `merge-worktree.md`
- `aiox-task-modify-agent` ← `modify-agent.md`
- `aiox-task-modify-task` ← `modify-task.md`
- `aiox-task-modify-workflow` ← `modify-workflow.md`
- `aiox-task-next` ← `next.md`
- `aiox-task-orchestrate-resume` ← `orchestrate-resume.md`
- `aiox-task-orchestrate-status` ← `orchestrate-status.md`
- `aiox-task-orchestrate-stop` ← `orchestrate-stop.md`
- `aiox-task-orchestrate` ← `orchestrate.md`
- `aiox-task-patterns` ← `patterns.md`
- `aiox-task-plan-create-context` ← `plan-create-context.md`
- `aiox-task-plan-create-implementation` ← `plan-create-implementation.md`
- `aiox-task-plan-execute-subtask` ← `plan-execute-subtask.md`
- `aiox-task-po-backlog-add` ← `po-backlog-add.md`
- `aiox-task-po-close-story` ← `po-close-story.md`
- `aiox-task-po-manage-story-backlog` ← `po-manage-story-backlog.md`
- `aiox-task-po-pull-story-from-clickup` ← `po-pull-story-from-clickup.md`
- `aiox-task-po-pull-story` ← `po-pull-story.md`
- `aiox-task-po-stories-index` ← `po-stories-index.md`
- `aiox-task-po-sync-story-to-clickup` ← `po-sync-story-to-clickup.md`
- `aiox-task-po-sync-story` ← `po-sync-story.md`
- `aiox-task-pr-automation` ← `pr-automation.md`
- `aiox-task-project-status` ← `project-status.md`
- `aiox-task-propose-modification` ← `propose-modification.md`
- `aiox-task-publish-npm` ← `publish-npm.md`
- `aiox-task-qa-after-creation` ← `qa-after-creation.md`
- `aiox-task-qa-backlog-add-followup` ← `qa-backlog-add-followup.md`
- `aiox-task-qa-browser-console-check` ← `qa-browser-console-check.md`
- `aiox-task-qa-create-fix-request` ← `qa-create-fix-request.md`
- `aiox-task-qa-evidence-requirements` ← `qa-evidence-requirements.md`
- `aiox-task-qa-false-positive-detection` ← `qa-false-positive-detection.md`
- `aiox-task-qa-fix-issues` ← `qa-fix-issues.md`
- `aiox-task-qa-gate` ← `qa-gate.md`
- `aiox-task-qa-generate-tests` ← `qa-generate-tests.md`
- `aiox-task-qa-library-validation` ← `qa-library-validation.md`
- `aiox-task-qa-migration-validation` ← `qa-migration-validation.md`
- `aiox-task-qa-nfr-assess` ← `qa-nfr-assess.md`
- `aiox-task-qa-review-build` ← `qa-review-build.md`
- `aiox-task-qa-review-proposal` ← `qa-review-proposal.md`
- `aiox-task-qa-review-story` ← `qa-review-story.md`
- `aiox-task-qa-risk-profile` ← `qa-risk-profile.md`
- `aiox-task-qa-run-tests` ← `qa-run-tests.md`
- `aiox-task-qa-security-checklist` ← `qa-security-checklist.md`
- `aiox-task-qa-test-design` ← `qa-test-design.md`
- `aiox-task-qa-trace-requirements` ← `qa-trace-requirements.md`
- `aiox-task-release-management` ← `release-management.md`
- `aiox-task-remove-mcp` ← `remove-mcp.md`
- `aiox-task-remove-worktree` ← `remove-worktree.md`
- `aiox-task-resolve-github-issue` ← `resolve-github-issue.md`
- `aiox-task-review-contributor-pr` ← `review-contributor-pr.md`
- `aiox-task-run-design-system-pipeline` ← `run-design-system-pipeline.md`
- `aiox-task-run-workflow-engine` ← `run-workflow-engine.md`
- `aiox-task-run-workflow` ← `run-workflow.md`
- `aiox-task-search-mcp` ← `search-mcp.md`
- `aiox-task-security-audit` ← `security-audit.md`
- `aiox-task-security-scan` ← `security-scan.md`
- `aiox-task-session-resume` ← `session-resume.md`
- `aiox-task-setup-database` ← `setup-database.md`
- `aiox-task-setup-design-system` ← `setup-design-system.md`
- `aiox-task-setup-github` ← `setup-github.md`
- `aiox-task-setup-llm-routing` ← `setup-llm-routing.md`
- `aiox-task-setup-mcp-docker` ← `setup-mcp-docker.md`
- `aiox-task-setup-project-docs` ← `setup-project-docs.md`
- `aiox-task-shard-doc` ← `shard-doc.md`
- `aiox-task-sm-create-next-story` ← `sm-create-next-story.md`
- `aiox-task-spec-assess-complexity` ← `spec-assess-complexity.md`
- `aiox-task-spec-critique` ← `spec-critique.md`
- `aiox-task-spec-gather-requirements` ← `spec-gather-requirements.md`
- `aiox-task-spec-research-dependencies` ← `spec-research-dependencies.md`
- `aiox-task-spec-write-spec` ← `spec-write-spec.md`
- `aiox-task-squad-creator-analyze` ← `squad-creator-analyze.md`
- `aiox-task-squad-creator-create` ← `squad-creator-create.md`
- `aiox-task-squad-creator-design` ← `squad-creator-design.md`
- `aiox-task-squad-creator-download` ← `squad-creator-download.md`
- `aiox-task-squad-creator-extend` ← `squad-creator-extend.md`
- `aiox-task-squad-creator-list` ← `squad-creator-list.md`
- `aiox-task-squad-creator-migrate` ← `squad-creator-migrate.md`
- `aiox-task-squad-creator-publish` ← `squad-creator-publish.md`
- `aiox-task-squad-creator-sync-ide-command` ← `squad-creator-sync-ide-command.md`
- `aiox-task-squad-creator-sync-synkra` ← `squad-creator-sync-synkra.md`
- `aiox-task-squad-creator-validate` ← `squad-creator-validate.md`
- `aiox-task-story-checkpoint` ← `story-checkpoint.md`
- `aiox-task-sync-documentation` ← `sync-documentation.md`
- `aiox-task-sync-registry-intel` ← `sync-registry-intel.md`
- `aiox-task-tailwind-upgrade` ← `tailwind-upgrade.md`
- `aiox-task-test-as-user` ← `test-as-user.md`
- `aiox-task-test-validation-task` ← `test-validation-task.md`
- `aiox-task-triage-github-issues` ← `triage-github-issues.md`
- `aiox-task-undo-last` ← `undo-last.md`
- `aiox-task-update-aiox` ← `update-aiox.md`
- `aiox-task-update-manifest` ← `update-manifest.md`
- `aiox-task-update-source-tree` ← `update-source-tree.md`
- `aiox-task-ux-create-wireframe` ← `ux-create-wireframe.md`
- `aiox-task-ux-ds-scan-artifact` ← `ux-ds-scan-artifact.md`
- `aiox-task-ux-user-research` ← `ux-user-research.md`
- `aiox-task-validate-agents` ← `validate-agents.md`
- `aiox-task-validate-next-story` ← `validate-next-story.md`
- `aiox-task-validate-tech-preset` ← `validate-tech-preset.md`
- `aiox-task-validate-workflow` ← `validate-workflow.md`
- `aiox-task-verify-subtask` ← `verify-subtask.md`
- `aiox-task-waves` ← `waves.md`
- `aiox-task-yolo-toggle` ← `yolo-toggle.md`

## Generated workflow inventory

- `aiox-workflow-auto-worktree` ← `auto-worktree.yaml`
- `aiox-workflow-brownfield-discovery` ← `brownfield-discovery.yaml`
- `aiox-workflow-brownfield-fullstack` ← `brownfield-fullstack.yaml`
- `aiox-workflow-brownfield-service` ← `brownfield-service.yaml`
- `aiox-workflow-brownfield-ui` ← `brownfield-ui.yaml`
- `aiox-workflow-design-system-build-quality` ← `design-system-build-quality.yaml`
- `aiox-workflow-development-cycle` ← `development-cycle.yaml`
- `aiox-workflow-epic-orchestration` ← `epic-orchestration.yaml`
- `aiox-workflow-greenfield-fullstack` ← `greenfield-fullstack.yaml`
- `aiox-workflow-greenfield-service` ← `greenfield-service.yaml`
- `aiox-workflow-greenfield-ui` ← `greenfield-ui.yaml`
- `aiox-workflow-qa-loop` ← `qa-loop.yaml`
- `aiox-workflow-readme` ← `README.md`
- `aiox-workflow-spec-pipeline` ← `spec-pipeline.yaml`
- `aiox-workflow-story-development-cycle` ← `story-development-cycle.yaml`
