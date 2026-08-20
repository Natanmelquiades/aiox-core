#!/usr/bin/env python3
"""Materialize the Hermes AIOX adapter as one or more Hermes profiles.

The default is deliberately safe and small: create/update only ``aiox-master``.
Use ``--all`` when a user explicitly wants one profile per AIOX role.
Existing SOUL.md, config.yaml and skill files are preserved unless an explicit
force flag is provided. The operation never creates IDE-specific directories.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

ADAPTER = Path(__file__).resolve().parents[1]
_NESTED_SOURCE = ADAPTER / "references" / "aiox-source"
SOURCE_ROOT = _NESTED_SOURCE if (_NESTED_SOURCE / "package.json").exists() else ADAPTER
MANIFEST_PATH = ADAPTER / "adapter-manifest.json"
MANIFEST = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
ROLES = MANIFEST["roles"]
SKIP_DIR_NAMES = {
    "node_modules",
    ".git",
    ".claude",
    ".codex",
    ".gemini",
    ".cursor",
    ".grok",
    ".antigravity",
    "coverage",
    ".cache",
    "__pycache__",
    ".env",
    "auth.json",
    "state.db",
    "state.db-shm",
    "state.db-wal",
    "hermes_state.db",
    "hermes_state.db-shm",
    "hermes_state.db-wal",
}


def hermes_command() -> str:
    for name in ("hermes.exe", "hermes"):
        found = shutil.which(name)
        if found:
            return found
    raise SystemExit("Hermes CLI not found on PATH. Install Hermes or pass --dry-run.")


def hermes_home() -> Path:
    configured = os.environ.get("HERMES_HOME")
    if configured:
        return Path(configured)
    local_app_data = os.environ.get("LOCALAPPDATA")
    return Path(local_app_data) / "hermes" if local_app_data else Path.home() / ".hermes"


def run(command: list[str]) -> None:
    result = subprocess.run(command, text=True, capture_output=True, check=False)
    if result.returncode:
        raise SystemExit(
            f"Command failed ({result.returncode}): {' '.join(command)}\n"
            f"{result.stdout}\n{result.stderr}"
        )


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def role_profile_name(role: dict[str, Any]) -> str:
    role_id = role["id"]
    return role_id if role_id.startswith("aiox-") else f"aiox-{role_id}"


def select_roles(profile: str | None, all_roles: bool) -> list[dict[str, Any]]:
    if all_roles:
        return list(ROLES)
    target = profile or "aiox-master"
    if not target.startswith("aiox-"):
        target = f"aiox-{target}"
    selected = [role for role in ROLES if role_profile_name(role) == target]
    if not selected:
        available = ", ".join(role_profile_name(role) for role in ROLES)
        raise SystemExit(f"Unknown profile {target!r}. Available: {available}")
    return selected


def copy_file(
    source: Path,
    target: Path,
    *,
    dry_run: bool,
    force: bool,
    actions: list[str],
) -> None:
    if not source.exists():
        raise SystemExit(f"Source file not found: {source}")
    if target.exists() and not force:
        actions.append(f"preserved {target}")
        return
    actions.append(f"copy {source} -> {target}")
    if not dry_run:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def copy_tree_non_destructive(
    source: Path,
    target: Path,
    *,
    dry_run: bool,
    force: bool,
    actions: list[str],
) -> None:
    if not source.exists():
        raise SystemExit(f"Source directory not found: {source}")
    for source_file in sorted(item for item in source.rglob("*") if item.is_file()):
        relative = source_file.relative_to(source)
        if any(part in SKIP_DIR_NAMES for part in relative.parts):
            continue
        target_file = target / relative
        if target_file.exists() and not force:
            if file_hash(source_file) == file_hash(target_file):
                actions.append(f"unchanged {target_file}")
            else:
                actions.append(f"preserved-custom {target_file}")
            continue
        actions.append(f"copy {source_file} -> {target_file}")
        if not dry_run:
            target_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_file, target_file)


def materialize_role(
    role: dict[str, Any],
    home: Path,
    *,
    hermes: str | None = None,
    dry_run: bool = False,
    force_skills: bool = False,
    force_profile: bool = False,
    copy_source: bool = True,
    create_profile: bool = True,
) -> dict[str, Any]:
    name = role_profile_name(role)
    profile_dir = home / "profiles" / name
    actions: list[str] = []
    if not profile_dir.exists():
        actions.append(f"create profile {name}")
        if create_profile and not dry_run:
            if not hermes:
                hermes = hermes_command()
            description = f"AIOX {role['title']} — {role['when']}"
            run([hermes, "profile", "create", name, "--no-alias", "--no-skills", "--description", description])
        if not dry_run:
            profile_dir.mkdir(parents=True, exist_ok=True)
    else:
        actions.append(f"reuse profile {name}")

    config_source = ADAPTER / "config.yaml"
    soul_source = ADAPTER / "roles" / role["file"]
    copy_file(config_source, profile_dir / "config.yaml", dry_run=dry_run, force=force_profile, actions=actions)
    copy_file(soul_source, profile_dir / "SOUL.md", dry_run=dry_run, force=force_profile, actions=actions)
    copy_file(
        ADAPTER / "adapter-manifest.json",
        profile_dir / "adapter-manifest.json",
        dry_run=dry_run,
        force=force_skills,
        actions=actions,
    )
    copy_file(
        ADAPTER / "distribution.yaml",
        profile_dir / "distribution.yaml",
        dry_run=dry_run,
        force=force_skills,
        actions=actions,
    )
    copy_tree_non_destructive(
        ADAPTER / "roles",
        profile_dir / "roles",
        dry_run=dry_run,
        force=force_skills,
        actions=actions,
    )
    copy_tree_non_destructive(
        ADAPTER / "skill-bundles",
        profile_dir / "skill-bundles",
        dry_run=dry_run,
        force=force_skills,
        actions=actions,
    )

    skills_source = ADAPTER / "skills"
    copy_tree_non_destructive(
        skills_source,
        profile_dir / "skills",
        dry_run=dry_run,
        force=force_skills,
        actions=actions,
    )

    entrypoint_source = ADAPTER / "scripts" / "aiox_hermes.py"
    copy_file(
        entrypoint_source,
        profile_dir / "scripts" / "aiox_hermes.py",
        dry_run=dry_run,
        force=force_skills,
        actions=actions,
    )

    if name == "aiox-master" and copy_source:
        if SOURCE_ROOT == _NESTED_SOURCE:
            copy_tree_non_destructive(
                SOURCE_ROOT,
                profile_dir / "references" / "aiox-source",
                dry_run=dry_run,
                force=force_skills,
                actions=actions,
            )
        else:
            source_paths = [
                ".aiox-core",
                "bin",
                "packages",
                "scripts",
                "package.json",
                "package-lock.json",
                "LICENSE",
                "CONTRIBUTING.md",
                "AGENTS.md",
            ]
            for relative in source_paths:
                source = SOURCE_ROOT / relative
                target = profile_dir / relative
                if source.is_dir():
                    copy_tree_non_destructive(
                        source,
                        target,
                        dry_run=dry_run,
                        force=force_skills,
                        actions=actions,
                    )
                elif source.is_file():
                    copy_file(
                        source,
                        target,
                        dry_run=dry_run,
                        force=force_skills,
                        actions=actions,
                    )

    return {"profile": name, "path": str(profile_dir), "actions": actions}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Install the AIOX adapter into Hermes profiles")
    parser.add_argument("--profile", help="Profile to materialize; defaults to aiox-master")
    parser.add_argument("--all", action="store_true", help="Materialize all role profiles")
    parser.add_argument("--dry-run", action="store_true", help="Show actions without writing")
    parser.add_argument("--force-skills", action="store_true", help="Overwrite adapter-owned skills and snapshot files")
    parser.add_argument("--force-profile", action="store_true", help="Overwrite SOUL.md and config.yaml")
    parser.add_argument("--no-source", action="store_true", help="Do not materialize the upstream snapshot")
    parser.add_argument("--home", type=Path, help="Override Hermes home (mainly for tests)")
    args = parser.parse_args(argv)

    home = (args.home or hermes_home()).resolve()
    hermes = None if args.dry_run else hermes_command()
    roles = select_roles(args.profile, args.all)
    print(f"Hermes home: {home}")
    print(f"Profiles selected: {', '.join(role_profile_name(role) for role in roles)}")
    for role in roles:
        result = materialize_role(
            role,
            home,
            hermes=hermes,
            dry_run=args.dry_run,
            force_skills=args.force_skills,
            force_profile=args.force_profile,
            copy_source=not args.no_source,
        )
        print(f"{result['profile']}: {len(result['actions'])} planned actions")
    print("Dry-run complete; no files written." if args.dry_run else "AIOX Hermes profile materialization complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
