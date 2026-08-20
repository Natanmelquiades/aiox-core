# AIOX on Hermes Agent

Esta branch `hermes` mantém o núcleo AIOX upstream e adiciona uma projeção
nativa para o Hermes Agent.

## Estado da branch

- Base upstream: `SynkraAI/aiox-core/main`;
- Fork: `Natanmelquiades/aiox-core`;
- Remotes esperados:
  - `origin`: fork pessoal/organizacional;
  - `upstream`: `https://github.com/SynkraAI/aiox-core.git`;
- Branch `main`: espelho sincronizável do upstream;
- Branch `hermes`: integração específica do Hermes;
- AIOX version: 5.4.1;
- Adapter version: 0.3.0.

## Instalação no Hermes

A partir de uma cópia local ou de uma release do fork:

```bash
python scripts/install_hermes_aiox_profiles.py --profile aiox-master --dry-run
python scripts/install_hermes_aiox_profiles.py --profile aiox-master
```

Ou usando o instalador de perfis do Hermes:

```bash
hermes profile install https://github.com/Natanmelquiades/aiox-core --name aiox-master
hermes -p aiox-master chat
```

A instalação padrão materializa um perfil `aiox-master`. Use `--all` no
installer do adapter para materializar as demais roles.

## Entrypoint

```bash
python scripts/aiox_hermes.py help
python scripts/aiox_hermes.py doctor --json
python scripts/aiox_hermes.py manifest --check --json
python scripts/aiox_hermes.py route --text "quero criar uma feature" --json
python scripts/aiox_hermes.py bootstrap --path . --json
python scripts/aiox_hermes.py sync-check --offline --json
```

## Colaboração com o AIOX upstream

Mudanças genéricas de plataforma, workflows, contratos, validações e núcleo
podem ser propostas ao upstream por Pull Request. Mudanças específicas do
Hermes devem permanecer nesta branch ou em um repositório de distribuição
Hermes.

```bash
git fetch upstream main
git switch main
git merge --ff-only upstream/main
git push origin main

git switch hermes
# rebase/merge a base atual somente após revisar o diff
git diff main...hermes
```

Antes de qualquer PR upstream:

```bash
npm run lint
npm run typecheck
npm test
npm run build
npm run validate:manifest
npm run validate:port-denylist
```

Antes de publicar a branch Hermes:

```bash
python -m unittest discover -s tests -v
python scripts/aiox_hermes.py manifest --check
python scripts/aiox_hermes.py doctor --json
python scripts/aiox_hermes.py sync-check --offline --json
```

## Ownership

| Área | Fonte de verdade |
|---|---|
| Núcleo AIOX | upstream `.aiox-core/`, `bin/`, `packages/` |
| Adaptação Hermes | `distribution.yaml`, `roles/`, `skills/`, `skill-bundles/`, scripts Hermes |
| Projeto do usuário | `.aiox/`, `docs/stories/`, `.hermes.md`, `AGENTS.md` |
| Perfil Hermes | `$HERMES_HOME`, protegido pelo installer |
| Credenciais | `.env`/`auth.json` do Hermes; nunca versionar |

## Não portamos automaticamente

- hooks e instruções específicas de Claude/Codex/Gemini;
- `.claude`, `.codex`, `.gemini`, Cursor, Grok ou Antigravity para perfis Hermes;
- segredos, sessões, memória ou estado local;
- scripts upstream baixados durante `sync-check`.

## Licença

A distribuição segue a licença MIT do AIOX upstream e preserva os avisos de
copyright e trademark presentes no repositório original.
