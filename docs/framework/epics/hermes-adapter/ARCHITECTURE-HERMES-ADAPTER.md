# Hermes AIOX MVP — Arquitetura e Operação

## Objetivo

Entregar um braço Hermes-native do AIOX que seja instalável por terceiros, produza primeiro valor rapidamente e não dependa da execução de hooks de Codex/Claude/Gemini.

## Princípios

1. `.aiox-core/` é o source root upstream e não é editado pelo adapter Hermes.
2. `skills/`, `roles/` e `skill-bundles/` são projeções Hermes.
3. O entrypoint determinístico usa Python stdlib para reduzir dependências.
4. O runtime Node do AIOX é opcional e fica fora do gate principal.
5. Estado de projeto fica em `.aiox/hermes/` e é idempotente.
6. Nenhum update upstream altera a projeção sem relatório e aprovação.
7. A camada Hermes não cria `.claude`, `.codex`, `.gemini` ou hooks de IDE.

## Fluxo de uso

```text
intenção natural
  -> scripts/aiox_hermes.py route
  -> role/skill recomendada
  -> workflow AIOX
  -> docs/prd ou docs/architecture
  -> docs/stories
  -> desenvolvimento
  -> QA/evidências
  -> próximo handoff
```

## Comandos MVP

```bash
python scripts/aiox_hermes.py help
python scripts/aiox_hermes.py status
python scripts/aiox_hermes.py doctor
python scripts/aiox_hermes.py route --text "quero criar uma feature"
python scripts/aiox_hermes.py bootstrap --path .
python scripts/aiox_hermes.py state start --story story-0.1 --role dev --workflow story-development-cycle --step implementation --next "executar QA"
python scripts/aiox_hermes.py state show
python scripts/aiox_hermes.py state clear
python scripts/aiox_hermes.py manifest --check
python scripts/aiox_hermes.py sync-check --offline
```

## Distribuição

O perfil `aiox-master` é a experiência recomendada. O instalador padrão não cria uma frota de 12 Bots nem sobrescreve `SOUL.md`, `config.yaml`, memória ou sessões existentes. `--all` fica disponível para usuários que realmente desejarem perfis por role.

## Gates

- Manifesto sem entradas órfãs.
- Todas as skills declaradas existem.
- Todos os sources AIOX declarados existem.
- Estado criado sem destruir arquivos existentes.
- Sync offline não escreve arquivos.
- Testes unitários e smoke passam.
