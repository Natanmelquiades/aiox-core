#!/usr/bin/env python3
"""Hermes-native entrypoint for the Synkra AIOX adapter.

This module intentionally uses only the Python standard library so the adapter
can be used as a plug-and-play Hermes distribution without requiring the
upstream AIOX Node runtime to be installed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
_SNAPSHOT_ROOT = ROOT / "references" / "aiox-source"
SOURCE_ROOT = _SNAPSHOT_ROOT if (_SNAPSHOT_ROOT / "package.json").exists() else ROOT
AIOX_ROOT = SOURCE_ROOT / ".aiox-core"
SKILLS_ROOT = ROOT / "skills"
MANIFEST_PATH = ROOT / "adapter-manifest.json"
DISTRIBUTION_PATH = ROOT / "distribution.yaml"
PROJECTION_MANIFEST_PATH = ROOT / "projection-manifest.json"
UPSTREAM_REPOSITORY = "https://github.com/SynkraAI/aiox-core"
UPSTREAM_API = "https://api.github.com/repos/SynkraAI/aiox-core/commits/main"
UPSTREAM_PACKAGE = "https://raw.githubusercontent.com/SynkraAI/aiox-core/main/package.json"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def rel(path: Path, base: Path = ROOT) -> str:
    return path.resolve().relative_to(base.resolve()).as_posix()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json_atomic(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def read_distribution_value(name: str) -> str | None:
    if not DISTRIBUTION_PATH.exists():
        return None
    pattern = re.compile(rf"^{re.escape(name)}:\s*['\"]?([^'\"#\s]+)", re.MULTILINE)
    match = pattern.search(DISTRIBUTION_PATH.read_text(encoding="utf-8"))
    return match.group(1) if match else None


def iter_files(path: Path, suffixes: Iterable[str] | None = None) -> list[Path]:
    if not path.exists():
        return []
    allowed = set(suffixes) if suffixes else None
    return sorted(
        item for item in path.rglob("*")
        if item.is_file() and (allowed is None or item.suffix in allowed)
    )


def source_counts() -> dict[str, int]:
    agents_dir = AIOX_ROOT / "development" / "agents"
    tasks_dir = AIOX_ROOT / "development" / "tasks"
    workflows_dir = AIOX_ROOT / "development" / "workflows"
    return {
        "source_agents": len(list(agents_dir.glob("*.md"))) if agents_dir.exists() else 0,
        "source_tasks": len(iter_files(tasks_dir)),
        "source_workflows": len(iter_files(workflows_dir)),
    }


def projection_counts() -> dict[str, int]:
    dirs = [item for item in SKILLS_ROOT.iterdir() if item.is_dir()] if SKILLS_ROOT.exists() else []
    return {
        "adapter_skill_dirs": len(dirs),
        "agent_skills": sum(item.name.startswith("aiox-agent-") for item in dirs),
        "task_skills": sum(item.name.startswith("aiox-task-") for item in dirs),
        "workflow_skills": sum(item.name.startswith("aiox-workflow-") for item in dirs),
    }


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_projection_manifest() -> dict[str, Any]:
    manifest = load_json(MANIFEST_PATH)
    entries: list[dict[str, Any]] = []

    def add_entry(source_id: str, source_path: Path, target_id: str, target_path: Path, kind: str) -> None:
        entries.append(
            {
                "sourceId": source_id,
                "sourcePath": rel(source_path),
                "sourceKind": kind,
                "targetId": target_id,
                "targetPath": rel(target_path),
                "ownership": "upstream-transformed",
                "transform": f"{kind}-to-hermes-skill-v1",
                "sourceHash": sha256_file(source_path) if source_path.exists() else None,
                "outputHash": sha256_file(target_path) if target_path.exists() else None,
                "status": "active" if source_path.exists() and target_path.exists() else "missing",
            }
        )

    for item in manifest.get("roles", []):
        add_entry(
            f"aiox-agent:{item.get('id', '')}",
            ROOT / "roles" / item.get("file", ""),
            item.get("skill", ""),
            SKILLS_ROOT / item.get("skill", "") / "SKILL.md",
            "agent",
        )
    for item in manifest.get("tasks", []):
        add_entry(
            f"aiox-task:{item.get('source', '')}",
            AIOX_ROOT / "development" / "tasks" / item.get("source", ""),
            item.get("skill", ""),
            SKILLS_ROOT / item.get("skill", "") / "SKILL.md",
            "task",
        )
    for item in manifest.get("workflows", []):
        add_entry(
            f"aiox-workflow:{item.get('source', '')}",
            AIOX_ROOT / "development" / "workflows" / item.get("source", ""),
            item.get("skill", ""),
            SKILLS_ROOT / item.get("skill", "") / "SKILL.md",
            "workflow",
        )

    entries.sort(key=lambda item: item["sourceId"])
    digest_input = json.dumps(entries, ensure_ascii=False, sort_keys=True).encode("utf-8")
    generation = hashlib.sha256(digest_input).hexdigest()[:16]
    return {
        "schemaVersion": 1,
        "generation": generation,
        "adapter": adapter_metadata(),
        "entries": entries,
    }


def validate_manifest() -> tuple[list[str], list[str], dict[str, Any]]:
    errors: list[str] = []
    warnings: list[str] = []
    summary: dict[str, Any] = {}

    if not MANIFEST_PATH.exists():
        return [f"Manifest not found: {MANIFEST_PATH}"], warnings, summary
    try:
        manifest = load_json(MANIFEST_PATH)
    except (OSError, json.JSONDecodeError) as exc:
        return [f"Manifest cannot be parsed: {exc}"], warnings, summary

    roles = manifest.get("roles", [])
    tasks = manifest.get("tasks", [])
    workflows = manifest.get("workflows", [])
    summary.update(
        {
            "aiox_version": manifest.get("aiox_version"),
            "manifest_roles": len(roles),
            "manifest_tasks": len(tasks),
            "manifest_workflows": len(workflows),
            **source_counts(),
            **projection_counts(),
        }
    )

    expected = source_counts()
    if len(roles) != expected["source_agents"]:
        errors.append(f"Role count mismatch: manifest={len(roles)} source={expected['source_agents']}")
    if len(tasks) != expected["source_tasks"]:
        errors.append(f"Task count mismatch: manifest={len(tasks)} source={expected['source_tasks']}")
    if len(workflows) != expected["source_workflows"]:
        errors.append(
            f"Workflow count mismatch: manifest={len(workflows)} source={expected['source_workflows']}"
        )

    seen_targets: set[str] = set()
    for entry in roles:
        skill = entry.get("skill", "")
        role_file = entry.get("file", "")
        target = SKILLS_ROOT / skill / "SKILL.md"
        source_role = ROOT / "roles" / role_file
        if skill in seen_targets:
            errors.append(f"Duplicate role skill: {skill}")
        seen_targets.add(skill)
        if not target.exists():
            errors.append(f"Missing role skill: {rel(target)}")
        if not source_role.exists():
            errors.append(f"Missing role file: {rel(source_role)}")

    for entry in tasks:
        skill = entry.get("skill", "")
        source_file = entry.get("source", "")
        target = SKILLS_ROOT / skill / "SKILL.md"
        source_task = AIOX_ROOT / "development" / "tasks" / source_file
        if skill in seen_targets:
            errors.append(f"Duplicate task skill: {skill}")
        seen_targets.add(skill)
        if not target.exists():
            errors.append(f"Missing task skill: {rel(target)}")
        elif "## Original AIOX task" not in target.read_text(encoding="utf-8"):
            errors.append(f"Task wrapper missing original section: {rel(target)}")
        if not source_task.exists():
            errors.append(f"Missing source task: {rel(source_task)}")

    for entry in workflows:
        skill = entry.get("skill", "")
        source_file = entry.get("source", "")
        target = SKILLS_ROOT / skill / "SKILL.md"
        source_workflow = AIOX_ROOT / "development" / "workflows" / source_file
        if skill in seen_targets:
            errors.append(f"Duplicate workflow skill: {skill}")
        seen_targets.add(skill)
        if not target.exists():
            errors.append(f"Missing workflow skill: {rel(target)}")
        elif "## Original workflow" not in target.read_text(encoding="utf-8"):
            errors.append(f"Workflow wrapper missing original section: {rel(target)}")
        if not source_workflow.exists():
            errors.append(f"Missing source workflow: {rel(source_workflow)}")

    if not (SOURCE_ROOT / "package.json").exists():
        errors.append("Upstream package.json is missing")
    if not (AIOX_ROOT / "constitution.md").exists():
        warnings.append("AIOX constitution is missing from the source root")
    if not (SOURCE_ROOT / "node_modules").exists():
        warnings.append("Upstream node_modules is absent; Node runtime validation is optional")
    if not shutil.which("hermes") and not shutil.which("hermes.exe"):
        warnings.append("Hermes CLI was not found on PATH")

    return errors, warnings, summary


def run_command(args: list[str], cwd: Path = ROOT) -> tuple[int, str]:
    try:
        result = subprocess.run(
            args,
            cwd=str(cwd),
            text=True,
            capture_output=True,
            check=False,
        )
    except OSError as exc:
        return 127, str(exc)
    output = (result.stdout + result.stderr).strip()
    return result.returncode, output


def git_status(path: Path) -> dict[str, Any]:
    code, output = run_command(["git", "status", "--short", "--branch"], cwd=path)
    if code != 0:
        return {"is_git": False, "error": output}
    lines = output.splitlines()
    changes = [line for line in lines if line and not line.startswith("##")]
    branch = next((line[2:] for line in lines if line.startswith("## ")), "unknown")
    return {"is_git": True, "branch": branch, "changed_entries": len(changes), "raw": output}


def project_status(path: Path) -> dict[str, Any]:
    path = path.resolve()
    artifacts = {
        "docs/stories": (path / "docs" / "stories").exists(),
        "docs/prd": (path / "docs" / "prd").exists(),
        "docs/architecture": (path / "docs" / "architecture").exists(),
        ".aiox": (path / ".aiox").exists(),
        ".aiox/hermes": (path / ".aiox" / "hermes").exists(),
    }
    state_path = path / ".aiox" / "hermes" / "active-run.json"
    state = load_json(state_path) if state_path.exists() else None
    return {
        "path": str(path),
        "project_name": path.name,
        "git": git_status(path),
        "artifacts": artifacts,
        "active_run": state,
    }


def route_intent(text: str) -> dict[str, Any]:
    normalized = text.lower().strip()
    routes = [
        (("doctor", "diagnóstico", "diagnostico", "saúde", "saude"), "aiox-master", "aiox_hermes doctor", "Executar diagnóstico do adapter Hermes-AIOX"),
        (("status", "situação", "situacao", "onde paramos", "progresso"), "aiox-master", "aiox_hermes status", "Mostrar projeto, story e próximo passo"),
        (("qa", "teste", "testes", "qualidade", "review", "revisão", "revisao", "segurança", "seguranca"), "qa", "aiox-task-qa-gate", "Executar validação e produzir evidências"),
        (("story", "história", "historia", "backlog", "sprint", "critério", "criterio"), "sm", "aiox-task-create-next-story", "Criar ou validar uma story AIOX"),
        (("prd", "produto", "priorização", "priorizacao", "roadmap", "requisito", "quero criar uma feature", "criar uma feature", "criar funcionalidade", "nova feature", "planejar"), "pm", "aiox-agent-pm", "Elicitar requisitos e estruturar produto"),
        (("arquitetura", "arquitetar", "api", "infraestrutura", "infra", "sistema"), "architect", "aiox-agent-architect", "Desenhar a solução técnica"),
        (("ux", "interface", "design", "wireframe", "usabilidade"), "ux-design-expert", "aiox-agent-ux-design-expert", "Projetar experiência e interface"),
        (("banco", "database", "sql", "supabase", "migração", "migracao"), "data-engineer", "aiox-agent-data-engineer", "Modelar e validar dados"),
        (("push", "release", "deploy", "ci/cd", "github", "pull request", "pr"), "devops", "aiox-agent-devops", "Executar operação de repositório sob autoridade DevOps"),
        (("pesquisa", "mercado", "brainstorm", "ideia", "competitivo"), "analyst", "aiox-agent-analyst", "Pesquisar e estruturar descoberta"),
        (("implementar", "desenvolver", "bug", "código", "codigo", "build", "corrigir"), "dev", "aiox-task-dev-develop-story", "Implementar somente a story aprovada"),
    ]
    for keywords, role, target, next_action in routes:
        if any(keyword in normalized for keyword in keywords):
            return {
                "input": text,
                "role": role,
                "target": target,
                "next_action": next_action,
                "matched": True,
            }
    return {
        "input": text,
        "role": "aiox-master",
        "target": "aiox-hermes-entrypoint",
        "next_action": "Usar *help e escolher uma receita de trabalho",
        "matched": False,
    }


def adapter_metadata() -> dict[str, Any]:
    return {
        "adapter_version": read_distribution_value("version") or "unknown",
        "aiox_version": read_distribution_value("aiox_version") or (load_json(MANIFEST_PATH).get("aiox_version") if MANIFEST_PATH.exists() else "unknown"),
        "upstream_repository": read_distribution_value("upstream_repository") or UPSTREAM_REPOSITORY,
        "upstream_ref": read_distribution_value("upstream_ref") or "main",
        "upstream_commit": read_distribution_value("upstream_commit") or "unknown",
        "hermes_min_version": read_distribution_value("hermes_requires") or "unknown",
    }


def bootstrap_project(path: Path, force: bool = False, dry_run: bool = False) -> dict[str, Any]:
    path = path.resolve()
    state_dir = path / ".aiox" / "hermes"
    project_file = state_dir / "project.json"
    metadata = adapter_metadata()
    payload = {
        "schemaVersion": 1,
        "projectPath": str(path),
        "initializedAt": now_iso(),
        "adapter": metadata,
        "artifacts": ["docs/stories", "docs/prd", "docs/architecture", ".aiox"],
    }
    actions = [str(state_dir), str(project_file)]
    if project_file.exists() and not force:
        return {"changed": False, "reason": "project_already_bootstrapped", "path": str(project_file), "actions": actions}
    if not dry_run:
        state_dir.mkdir(parents=True, exist_ok=True)
        write_json_atomic(project_file, payload)
    return {"changed": True, "dry_run": dry_run, "path": str(project_file), "actions": actions}


def state_path(path: Path) -> Path:
    return path.resolve() / ".aiox" / "hermes" / "active-run.json"


def state_start(path: Path, args: argparse.Namespace) -> dict[str, Any]:
    destination = state_path(path)
    payload = {
        "schemaVersion": 1,
        "story": args.story,
        "role": args.role,
        "workflow": args.workflow,
        "step": args.step,
        "next": args.next_step,
        "status": "in_progress",
        "updatedAt": now_iso(),
    }
    write_json_atomic(destination, payload)
    return payload


def fetch_upstream() -> tuple[str | None, str | None, str | None]:
    headers = {"User-Agent": "hermes-aiox-adapter"}
    try:
        request = urllib.request.Request(UPSTREAM_API, headers=headers)
        with urllib.request.urlopen(request, timeout=15) as response:
            commit_payload = json.load(response)
        commit = commit_payload.get("sha")
        message = (commit_payload.get("commit", {}).get("message") or "").splitlines()[0]
        package_request = urllib.request.Request(UPSTREAM_PACKAGE, headers=headers)
        with urllib.request.urlopen(package_request, timeout=15) as response:
            package = json.load(response)
        return commit, package.get("version"), message
    except (OSError, urllib.error.URLError, json.JSONDecodeError) as exc:
        return None, None, str(exc)


def sync_check(offline: bool = False) -> dict[str, Any]:
    local = adapter_metadata()
    result: dict[str, Any] = {"local": local, "network": "skipped" if offline else "checked"}
    if offline:
        result["status"] = "offline"
        return result
    commit, version, message = fetch_upstream()
    if not commit:
        result["status"] = "unavailable"
        result["error"] = message
        return result
    result["upstream"] = {"commit": commit, "version": version, "message": message}
    if version and str(local.get("aiox_version")) != str(version):
        result["status"] = "update_available"
    elif local.get("upstream_commit") == "unknown":
        result["status"] = "provenance_missing"
    elif local.get("upstream_commit") == commit or (
        local.get("upstream_commit") != "unknown"
        and (commit.startswith(str(local["upstream_commit"])) or str(local["upstream_commit"]).startswith(commit))
    ):
        result["status"] = "up_to_date"
    else:
        result["status"] = "update_available"
    return result


def print_payload(payload: Any, as_json: bool = False) -> None:
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    if isinstance(payload, str):
        print(payload)
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))


def command_help(_: argparse.Namespace) -> int:
    print(
        "Hermes AIOX Adapter — entrypoint plug-and-play\n\n"
        "Uso:\n"
        "  python scripts/aiox_hermes.py help\n"
        "  python scripts/aiox_hermes.py status\n"
        "  python scripts/aiox_hermes.py doctor\n"
        "  python scripts/aiox_hermes.py route --text 'quero criar uma feature'\n"
        "  python scripts/aiox_hermes.py bootstrap --path .\n"
        "  python scripts/aiox_hermes.py state start --story story-0.1 --role dev --workflow story-development-cycle --step implementation --next 'executar QA'\n"
        "  python scripts/aiox_hermes.py state show\n"
        "  python scripts/aiox_hermes.py state clear\n"
        "  python scripts/aiox_hermes.py manifest --check\n"
        "  python scripts/aiox_hermes.py manifest --write\n"
        "  python scripts/aiox_hermes.py sync-check --offline\n\n"
        "Receitas Hermes:\n"
        "  *plan -> PM/Analyst/Architect\n"
        "  *story -> SM/PO\n"
        "  *develop -> Dev\n"
        "  *qa -> QA\n"
        "  *resume -> status + próximo passo\n"
    )
    return 0


def command_status(args: argparse.Namespace) -> int:
    payload = project_status(Path(args.path))
    payload["adapter"] = adapter_metadata()
    print_payload(payload, args.json)
    return 0


def command_doctor(args: argparse.Namespace) -> int:
    errors, warnings, summary = validate_manifest()
    payload = {"ok": not errors, "errors": errors, "warnings": warnings, "summary": summary}
    print_payload(payload, args.json)
    return 0 if not errors else 1


def command_manifest(args: argparse.Namespace) -> int:
    errors, warnings, summary = validate_manifest()
    payload = {"valid": not errors, "errors": errors, "warnings": warnings, "summary": summary}
    if args.write and not errors:
        projection = build_projection_manifest()
        write_json_atomic(PROJECTION_MANIFEST_PATH, projection)
        payload["projection_manifest"] = {
            "path": str(PROJECTION_MANIFEST_PATH),
            "generation": projection["generation"],
            "entries": len(projection["entries"]),
        }
    print_payload(payload, args.json)
    return 0 if not errors else 1


def command_route(args: argparse.Namespace) -> int:
    print_payload(route_intent(args.text), args.json)
    return 0


def command_bootstrap(args: argparse.Namespace) -> int:
    payload = bootstrap_project(Path(args.path), force=args.force, dry_run=args.dry_run)
    print_payload(payload, args.json)
    return 0


def command_state(args: argparse.Namespace) -> int:
    path = Path(args.path)
    destination = state_path(path)
    if args.state_action == "start":
        payload = state_start(path, args)
    elif args.state_action == "show":
        if not destination.exists():
            payload = {"active": False, "path": str(destination)}
        else:
            payload = {"active": True, "path": str(destination), "run": load_json(destination)}
    elif args.state_action == "clear":
        existed = destination.exists()
        if existed:
            destination.unlink()
        payload = {"cleared": existed, "path": str(destination)}
    else:
        raise ValueError(f"Unknown state action: {args.state_action}")
    print_payload(payload, args.json)
    return 0


def command_sync_check(args: argparse.Namespace) -> int:
    payload = sync_check(offline=args.offline)
    print_payload(payload, args.json)
    return 0 if payload.get("status") not in {"unavailable"} else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Hermes-native AIOX plug-and-play entrypoint")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("help", help="Mostrar onboarding e receitas principais").set_defaults(func=command_help)

    status = sub.add_parser("status", help="Mostrar projeto, Git, artefatos e run ativo")
    status.add_argument("--path", default=".")
    status.add_argument("--json", action="store_true")
    status.set_defaults(func=command_status)

    doctor = sub.add_parser("doctor", help="Validar integridade do adapter e dependências")
    doctor.add_argument("--json", action="store_true")
    doctor.set_defaults(func=command_doctor)

    manifest = sub.add_parser("manifest", help="Verificar paridade do manifesto")
    manifest.add_argument("--check", action="store_true", help="Falha se houver erro")
    manifest.add_argument("--write", action="store_true", help="Gerar projection-manifest.json com hashes")
    manifest.add_argument("--json", action="store_true")
    manifest.set_defaults(func=command_manifest)

    route = sub.add_parser("route", help="Roteiar uma intenção para role/skill")
    route.add_argument("--text", required=True)
    route.add_argument("--json", action="store_true")
    route.set_defaults(func=command_route)

    bootstrap = sub.add_parser("bootstrap", help="Inicializar estado Hermes-AIOX em um projeto")
    bootstrap.add_argument("--path", default=".")
    bootstrap.add_argument("--force", action="store_true")
    bootstrap.add_argument("--dry-run", action="store_true")
    bootstrap.add_argument("--json", action="store_true")
    bootstrap.set_defaults(func=command_bootstrap)

    state = sub.add_parser("state", help="Gerenciar o run ativo AIOX-Hermes")
    state.add_argument("state_action", choices=["start", "show", "clear"])
    state.add_argument("--path", default=".")
    state.add_argument("--story")
    state.add_argument("--role")
    state.add_argument("--workflow")
    state.add_argument("--step")
    state.add_argument("--next", dest="next_step")
    state.add_argument("--json", action="store_true")
    state.set_defaults(func=command_state)

    sync = sub.add_parser("sync-check", help="Consultar proveniência e atualizações upstream")
    sync.add_argument("--offline", action="store_true")
    sync.add_argument("--json", action="store_true")
    sync.set_defaults(func=command_sync_check)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "state" and args.state_action == "start":
        missing = [name for name in ("story", "role", "workflow", "step", "next_step") if not getattr(args, name)]
        if missing:
            parser.error(f"state start requer: {', '.join(missing)}")
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
