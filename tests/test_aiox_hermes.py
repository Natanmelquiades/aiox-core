import json
import tempfile
import unittest
from pathlib import Path

from scripts import aiox_hermes
from scripts import install_hermes_aiox_profiles as installer


class AioxHermesEntrypointTests(unittest.TestCase):
    def test_manifest_is_complete(self):
        errors, warnings, summary = aiox_hermes.validate_manifest()
        self.assertEqual(errors, [], msg=f"manifest errors: {errors}")
        self.assertEqual(summary["manifest_roles"], 12)
        self.assertEqual(summary["manifest_tasks"], 219)
        self.assertEqual(summary["manifest_workflows"], 15)
        self.assertGreaterEqual(summary["adapter_skill_dirs"], 248)
        self.assertEqual(
            any("node_modules" in warning for warning in warnings),
            not aiox_hermes.SOURCE_ROOT.joinpath("node_modules").exists(),
        )

    def test_projection_manifest_has_hashes(self):
        projection = aiox_hermes.build_projection_manifest()
        self.assertEqual(projection["schemaVersion"], 1)
        self.assertEqual(len(projection["entries"]), 246)
        self.assertTrue(projection["generation"])
        self.assertTrue(all(entry["status"] == "active" for entry in projection["entries"]))
        self.assertTrue(all(entry["sourceHash"] and entry["outputHash"] for entry in projection["entries"]))

    def test_route_feature_to_dev(self):
        result = aiox_hermes.route_intent("quero implementar uma feature")
        self.assertEqual(result["role"], "dev")
        self.assertEqual(result["target"], "aiox-task-dev-develop-story")

    def test_route_new_feature_to_pm(self):
        result = aiox_hermes.route_intent("quero criar uma feature")
        self.assertEqual(result["role"], "pm")
        self.assertEqual(result["target"], "aiox-agent-pm")

    def test_route_status_to_master(self):
        result = aiox_hermes.route_intent("onde paramos no projeto?")
        self.assertEqual(result["role"], "aiox-master")
        self.assertEqual(result["target"], "aiox_hermes status")

    def test_bootstrap_is_idempotent(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            first = aiox_hermes.bootstrap_project(project)
            second = aiox_hermes.bootstrap_project(project)
            project_file = project / ".aiox" / "hermes" / "project.json"
            self.assertTrue(first["changed"])
            self.assertFalse(second["changed"])
            self.assertTrue(project_file.exists())
            payload = json.loads(project_file.read_text(encoding="utf-8"))
            self.assertEqual(payload["schemaVersion"], 1)
            self.assertEqual(payload["projectPath"], str(project.resolve()))

    def test_state_lifecycle(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            args = type(
                "StateArgs",
                (),
                {
                    "story": "story-0.1",
                    "role": "dev",
                    "workflow": "story-development-cycle",
                    "step": "implementation",
                    "next_step": "executar QA",
                },
            )()
            started = aiox_hermes.state_start(project, args)
            self.assertEqual(started["status"], "in_progress")
            state_file = project / ".aiox" / "hermes" / "active-run.json"
            self.assertTrue(state_file.exists())
            loaded = json.loads(state_file.read_text(encoding="utf-8"))
            self.assertEqual(loaded["next"], "executar QA")
            state_file.unlink()
            self.assertFalse(state_file.exists())

    def test_sync_check_offline_is_read_only(self):
        before = set(aiox_hermes.ROOT.rglob("*") )
        result = aiox_hermes.sync_check(offline=True)
        after = set(aiox_hermes.ROOT.rglob("*") )
        self.assertEqual(result["status"], "offline")
        self.assertEqual(before, after)


class ProfileInstallerTests(unittest.TestCase):
    def test_master_profile_name_is_canonical(self):
        role = next(item for item in installer.ROLES if item["id"] == "aiox-master")
        self.assertEqual(installer.role_profile_name(role), "aiox-master")
        self.assertEqual(len(installer.select_roles(None, False)), 1)
        self.assertEqual(installer.select_roles(None, False)[0]["id"], "aiox-master")

    def test_copy_tree_preserves_custom_file_without_force(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            target = root / "target"
            source.mkdir()
            target.mkdir()
            (source / "skill.md").write_text("upstream", encoding="utf-8")
            (target / "skill.md").write_text("local customization", encoding="utf-8")
            actions = []
            installer.copy_tree_non_destructive(
                source,
                target,
                dry_run=False,
                force=False,
                actions=actions,
            )
            self.assertEqual((target / "skill.md").read_text(encoding="utf-8"), "local customization")
            self.assertTrue(any("preserved-custom" in action for action in actions))

    def test_copy_tree_skips_runtime_directories(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            target = root / "target"
            (source / "node_modules" / "pkg").mkdir(parents=True)
            (source / ".git").mkdir()
            (source / ".claude" / "hooks").mkdir(parents=True)
            target.mkdir()
            (source / "node_modules" / "pkg" / "package.json").write_text("{}", encoding="utf-8")
            (source / ".claude" / "hooks" / "secret.sh").write_text("secret", encoding="utf-8")
            (source / ".env").write_text("TOKEN=secret", encoding="utf-8")
            (source / "runtime.py").write_text("print('ok')", encoding="utf-8")
            installer.copy_tree_non_destructive(source, target, dry_run=False, force=False, actions=[])
            self.assertTrue((target / "runtime.py").exists())
            self.assertFalse((target / "node_modules").exists())
            self.assertFalse((target / ".git").exists())
            self.assertFalse((target / ".claude").exists())
            self.assertFalse((target / ".env").exists())

    def test_copy_tree_updates_with_explicit_force(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            target = root / "target"
            source.mkdir()
            target.mkdir()
            (source / "skill.md").write_text("upstream", encoding="utf-8")
            (target / "skill.md").write_text("local customization", encoding="utf-8")
            installer.copy_tree_non_destructive(
                source,
                target,
                dry_run=False,
                force=True,
                actions=[],
            )
            self.assertEqual((target / "skill.md").read_text(encoding="utf-8"), "upstream")


if __name__ == "__main__":
    unittest.main(verbosity=2)
