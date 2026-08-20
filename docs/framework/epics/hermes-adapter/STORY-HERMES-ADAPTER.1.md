# Story HERMES-ADAPTER.1: Upstream-based Hermes adapter

## Metadata

| Campo | Valor |
|---|---|
| Story ID | HERMES-ADAPTER.1 |
| Epic | HERMES-ADAPTER |
| Status | In Progress |
| Branch | `hermes` |
| Base | `upstream/main` |
| Owner | `@devops` / `@dev` |

## Goal

Portar o adapter AIOX-Hermes existente para uma branch baseada no histórico
real do AIOX upstream, sem substituir o núcleo, preservando a capacidade de
sincronização e preparando colaboração via fork GitHub.

## Acceptance Criteria

1. A branch `hermes` é baseada no mesmo commit de `upstream/main` e `main` permanece limpa.
2. O adapter Hermes fica em arquivos/diretórios claramente identificados e não sobrescreve o README ou o núcleo upstream sem justificativa.
3. O entrypoint e o installer funcionam quando o próprio repositório fork é a fonte AIOX; snapshots aninhados são opcionais e não obrigatórios.
4. A projeção contém 12 roles, 219 tasks e 15 workflows, com manifesto e hashes válidos.
5. A distribuição protege `SOUL.md`, `config.yaml`, `.env`, `auth.json`, estado Hermes, diretórios IDE, `.git` e `node_modules`.
6. O repositório mantém `LICENSE`, `CONTRIBUTING.md`, `AGENTS.md` e os contratos públicos upstream.
7. Existe documentação de remotes, branches, contribuição upstream e separação entre mudanças genéricas e Hermes-specific.
8. Existe CI específico do adapter Hermes sem remover ou mascarar os gates upstream.
9. `python -m unittest discover -s tests -v`, `manifest --check`, `doctor`, `sync-check --offline` e smoke de instalação em perfil isolado passam.
10. O fork remoto recebe somente commits verificados, e o SHA remoto é lido de volta após o push.

## Deliverables

| Artifact | Path |
|---|---|
| Epic | `docs/framework/epics/hermes-adapter/EPIC-HERMES-ADAPTER.md` |
| Story | `docs/framework/epics/hermes-adapter/STORY-HERMES-ADAPTER.1.md` |
| Adapter metadata | `distribution.yaml`, `adapter-manifest.json`, `projection-manifest.json` |
| Entrypoint | `scripts/aiox_hermes.py` |
| Installer | `scripts/install_hermes_aiox_profiles.py` |
| Projection | `roles/`, `skills/`, `skill-bundles/` |
| Tests | `tests/test_aiox_hermes.py` |
| Hermes docs | `docs/platforms/hermes.md` |
| CI | `.github/workflows/hermes-adapter.yml` |

## Implementation Tasks

- [ ] Port adapter projection files from the verified local checkpoint.
- [ ] Make source-root detection work from the upstream-based fork.
- [ ] Add Hermes platform documentation and collaboration contract.
- [ ] Add adapter-specific validation workflow without changing upstream gates.
- [ ] Execute focused Hermes tests and upstream validation.
- [ ] Commit the branch with conventional commits.
- [ ] Push `hermes` to the personal fork only after all gates pass.
- [ ] Verify remote branch SHA and report limitations.

## QA Plan

- Hermes unit tests and Python syntax checks.
- AIOX manifest/agent/workflow/denylist validations.
- Upstream `node bin/aiox.js validate --detailed`.
- Native profile install from the fork.
- Verify no forbidden IDE or secret artifacts enter the profile.
- Verify `origin` points to the personal fork and `upstream` points to SynkraAI.

## File List

A ser preenchido durante a implementação.

## Change Log

| Date | Event |
|---|---|
| 2026-08-20 | Story criada na branch `hermes` a partir de `upstream/main`. |
