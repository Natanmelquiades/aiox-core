# Epic HERMES-ADAPTER: AIOX on Hermes

## Metadata

| Campo | Valor |
|---|---|
| Epic ID | HERMES-ADAPTER |
| Status | In Progress |
| Priority | P0 |
| Base | `upstream/main` (`SynkraAI/aiox-core`) |
| Integration branch | `hermes` |
| Target | Hermes Agent profiles and native runtime |
| License | MIT-compatible derivative; preserve upstream notices |

## Objetivo

Transformar o AIOX em uma integração Hermes-native, mantendo o núcleo upstream
compatível, a possibilidade de Pull Requests para `SynkraAI/aiox-core` e uma
distribuição plug-and-play para perfis Hermes.

## Princípios

1. `main` permanece sincronizável com o upstream.
2. A branch `hermes` contém o adapter e a projeção Hermes.
3. Conteúdo AIOX é fonte; skills/perfis Hermes são projeções geradas.
4. Não criar `.claude`, `.codex`, `.gemini`, Cursor ou hooks de outra IDE.
5. Não sobrescrever configuração, credenciais, memória ou sessões do usuário.
6. Mudanças genéricas devem ser candidatas a PR upstream; mudanças específicas
   do Hermes permanecem no adapter.
7. Toda entrega precisa de story, acceptance criteria, testes e evidência.

## Slices

| Story | Objetivo | Status |
|---|---|---|
| HERMES-ADAPTER.1 | Fork real, overlay Hermes, distribuição e CI inicial | In Progress |
| HERMES-ADAPTER.2 | Executor de workflows, estado/sessão, worktree e checkpoints | Backlog |
| HERMES-ADAPTER.3 | Integração Kanban/MCP/cron/memória | Backlog |
| HERMES-ADAPTER.4 | Plugin desktop e UX visual | Backlog |
| HERMES-ADAPTER.5 | PR upstream do contrato platform-neutral | Backlog |

## Limites

Fora desta primeira story: mudar o núcleo AIOX upstream, publicar um PR
automaticamente, copiar artefatos de IDE, instalar dependências Node no perfil
Hermes ou criar múltiplos Bots obrigatórios.
