from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[1]
WORKBENCH = REPOSITORY / "scripts" / "workbench.py"
PRIVACY_SCAN = REPOSITORY / "scripts" / "privacy_scan.py"


class WorkbenchCliTest(unittest.TestCase):
    def run_cli(
        self, *arguments: str, expected: int = 0
    ) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            [sys.executable, str(WORKBENCH), *arguments],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(expected, result.returncode, result.stderr)
        return result

    def test_profile_candidate_and_review_lifecycle(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "private"
            created = self.run_cli(
                "init-profile",
                "--name",
                "test_owner",
                "--root",
                str(root),
                "--activate",
            )
            profile = Path(json.loads(created.stdout)["profile"])
            profile_data = json.loads((profile / "profile.json").read_text())
            self.assertEqual("off", profile_data["learning_mode"])
            self.assertEqual("test-owner", profile_data["slug"])
            self.assertTrue(
                (profile / "skills" / "test-owner" / "SKILL.md").is_file()
            )

            self.run_cli(
                "add-candidate",
                "--root",
                str(root),
                "--source-session",
                "session-a",
                "--title",
                "A lesson",
                "--lesson",
                "Keep evidence bounded.",
                expected=2,
            )
            self.run_cli(
                "set-learning", "--root", str(root), "--mode", "candidate"
            )
            self.run_cli(
                "authorize-session",
                "--root",
                str(root),
                "--session-id",
                "session-a",
            )
            candidate_id = self.run_cli(
                "add-candidate",
                "--root",
                str(root),
                "--source-session",
                "session-a",
                "--title",
                "A lesson",
                "--lesson",
                "Keep evidence bounded.",
                "--evidence",
                "token=abcdefghijklmnop",
            ).stdout.strip()
            candidate = json.loads(
                (
                    profile
                    / "candidates"
                    / "pending"
                    / f"{candidate_id}.json"
                ).read_text()
            )
            self.assertIn("[REDACTED]", candidate["evidence_summary"])

            self.run_cli(
                "review-candidate",
                "--root",
                str(root),
                "--candidate",
                candidate_id,
                "--decision",
                "approve",
            )
            self.assertFalse(
                (
                    profile
                    / "candidates"
                    / "pending"
                    / f"{candidate_id}.json"
                ).exists()
            )
            self.assertTrue((profile / "knowledge" / "approved.jsonl").is_file())

    def test_private_module_registration(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "private"
            local_skill = Path(directory) / "local-skill"
            local_skill.mkdir()
            (local_skill / "SKILL.md").write_text(
                "---\nname: local\ndescription: local\n---\n"
            )
            self.run_cli(
                "init-profile",
                "--name",
                "owner",
                "--root",
                str(root),
                "--activate",
            )
            self.run_cli(
                "add-module",
                "--root",
                str(root),
                "--name",
                "Local module",
                "--skill-path",
                str(local_skill),
                "--description",
                "A private module",
                "--trigger",
                "local work",
            )
            profile = root / "profiles" / "owner"
            modules = json.loads((profile / "modules.json").read_text())["modules"]
            self.assertEqual("local-module", modules[0]["name"])

    def test_team_pack_requires_approval_after_content_changes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = base / "private"
            team_root = base / "shared-team"
            self.run_cli(
                "init-profile",
                "--name",
                "owner",
                "--root",
                str(root),
                "--activate",
            )
            self.run_cli(
                "init-team",
                "--root",
                str(root),
                "--name",
                "Example team",
                "--path",
                str(team_root),
            )
            shared_skill = team_root / "skills" / "shared-ops"
            shared_skill.mkdir(parents=True)
            skill_file = shared_skill / "SKILL.md"
            skill_file.write_text(
                "---\nname: shared-ops\ndescription: Shared operations.\n---\n"
            )
            contract = team_root / "docs" / "contract.md"
            contract.parent.mkdir()
            contract.write_text("Version one.\n")
            self.run_cli(
                "add-team-module",
                "--root",
                str(root),
                "--team",
                str(team_root),
                "--name",
                "Shared ops",
                "--skill-path",
                str(shared_skill),
                "--description",
                "A team-owned module",
                "--trigger",
                "shared work",
                "--resource-path",
                str(contract),
            )
            self.run_cli(
                "add-module",
                "--root",
                str(root),
                "--name",
                "Shared ops",
                "--skill-path",
                str(shared_skill),
                "--description",
                "An existing personal registration",
            )
            self.run_cli(
                "attach-team",
                "--root",
                str(root),
                "--team",
                str(team_root),
                expected=2,
            )
            self.run_cli(
                "attach-team",
                "--root",
                str(root),
                "--team",
                str(team_root),
                "--replace-personal",
            )

            resolved = json.loads(
                self.run_cli("list-modules", "--root", str(root)).stdout
            )
            self.assertEqual([], resolved["blocked_teams"])
            self.assertEqual("team", resolved["modules"][0]["scope"])
            self.assertEqual("example-team", resolved["modules"][0]["team"])
            personal_modules = json.loads(
                (root / "profiles" / "owner" / "modules.json").read_text()
            )["modules"]
            self.assertEqual([], personal_modules)

            contract.write_text("Version two.\n")
            blocked = json.loads(
                self.run_cli("list-modules", "--root", str(root)).stdout
            )
            self.assertEqual([], blocked["modules"])
            self.assertEqual(
                "approval-required", blocked["blocked_teams"][0]["status"]
            )
            status = json.loads(self.run_cli("status", "--root", str(root)).stdout)
            self.assertEqual(1, status["pending_team_update_count"])

            team_state = json.loads(
                self.run_cli("list-teams", "--root", str(root)).stdout
            )[0]
            self.run_cli(
                "approve-team-update",
                "--root",
                str(root),
                "--team",
                "example-team",
                "--digest",
                "0" * 64,
                expected=2,
            )
            self.run_cli(
                "approve-team-update",
                "--root",
                str(root),
                "--team",
                "example-team",
                "--digest",
                team_state["current_digest"],
            )
            approved = json.loads(
                self.run_cli("list-modules", "--root", str(root)).stdout
            )
            self.assertEqual([], approved["blocked_teams"])
            self.assertEqual("shared-ops", approved["modules"][0]["name"])

            skill_file.write_text(skill_file.read_text() + "\nUpdated guidance.\n")
            changed_skill = json.loads(
                self.run_cli("list-modules", "--root", str(root)).stdout
            )
            self.assertEqual([], changed_skill["modules"])
            self.assertEqual(
                "approval-required", changed_skill["blocked_teams"][0]["status"]
            )

    def test_ip_role_hides_personal_state_and_blocks_owner_actions(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = base / "private"
            team_root = base / "shared-team"
            personal_skill = base / "personal-skill"
            personal_skill.mkdir()
            (personal_skill / "SKILL.md").write_text(
                "---\nname: personal-only\ndescription: Private behavior.\n---\n"
            )

            created = json.loads(
                self.run_cli(
                    "init-profile",
                    "--name",
                    "owner",
                    "--root",
                    str(root),
                    "--activate",
                ).stdout
            )
            self.assertEqual("owner", created["role"])
            identity = json.loads(
                self.run_cli("identity", "--root", str(root)).stdout
            )
            self.assertEqual("owner", identity["role"])

            self.run_cli(
                "add-module",
                "--root",
                str(root),
                "--name",
                "Personal only",
                "--skill-path",
                str(personal_skill),
                "--description",
                "Owner-only behavior",
            )
            self.run_cli(
                "set-learning", "--root", str(root), "--mode", "candidate"
            )
            self.run_cli(
                "init-team",
                "--root",
                str(root),
                "--name",
                "Borrowed team",
                "--path",
                str(team_root),
            )
            shared_skill = team_root / "skills" / "shared-ops"
            shared_skill.mkdir(parents=True)
            (shared_skill / "SKILL.md").write_text(
                "---\nname: shared-ops\ndescription: Shared operations.\n---\n"
            )
            self.run_cli(
                "add-team-module",
                "--root",
                str(root),
                "--team",
                str(team_root),
                "--name",
                "Shared ops",
                "--skill-path",
                str(shared_skill),
                "--description",
                "Team behavior",
            )
            self.run_cli(
                "attach-team",
                "--root",
                str(root),
                "--team",
                str(team_root),
            )

            binding = json.loads(
                self.run_cli(
                    "bind-owner-ip",
                    "--root",
                    str(root),
                    "--ip",
                    "192.0.2.1",
                    "--replace",
                ).stdout
            )
            self.assertEqual("collaborator", binding["role"])

            identity = json.loads(
                self.run_cli("identity", "--root", str(root)).stdout
            )
            self.assertEqual("collaborator", identity["role"])
            modules = json.loads(
                self.run_cli("list-modules", "--root", str(root)).stdout
            )
            self.assertEqual("collaborator", modules["role"])
            self.assertEqual(["shared-ops"], [item["name"] for item in modules["modules"]])
            self.assertTrue(all(item["scope"] == "team" for item in modules["modules"]))

            status = json.loads(self.run_cli("status", "--root", str(root)).stdout)
            self.assertEqual("collaborator", status["role"])
            self.assertEqual("off", status["learning_mode"])
            for private_field in (
                "profile_path",
                "allowed_session_count",
                "personal_module_count",
                "pending_candidate_count",
            ):
                self.assertNotIn(private_field, status)

            denied_commands = (
                ("set-learning", "--mode", "off"),
                ("authorize-session", "--session-id", "borrowed-session"),
                (
                    "add-module",
                    "--name",
                    "blocked-personal",
                    "--skill-path",
                    str(personal_skill),
                    "--description",
                    "blocked",
                ),
                (
                    "init-team",
                    "--name",
                    "blocked-team",
                    "--path",
                    str(base / "blocked-team"),
                ),
                (
                    "add-team-module",
                    "--team",
                    str(team_root),
                    "--name",
                    "blocked-module",
                    "--skill-path",
                    str(shared_skill),
                    "--description",
                    "blocked",
                ),
                ("attach-team", "--team", str(team_root)),
                ("list-candidates",),
                (
                    "add-candidate",
                    "--source-session",
                    "borrowed-session",
                    "--title",
                    "blocked",
                    "--lesson",
                    "blocked",
                ),
                (
                    "review-candidate",
                    "--candidate",
                    "missing",
                    "--decision",
                    "reject",
                ),
                ("detach-team", "--team", "borrowed-team"),
                (
                    "approve-team-update",
                    "--team",
                    "borrowed-team",
                    "--digest",
                    "0" * 64,
                ),
                ("bind-owner-ip",),
            )
            for command in denied_commands:
                with self.subTest(command=command[0]):
                    result = self.run_cli(
                        command[0],
                        "--root",
                        str(root),
                        *command[1:],
                        expected=2,
                    )
                    self.assertIn("collaborator mode", result.stderr)

    def test_legacy_profile_can_bind_owner_ip_once(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "private"
            created = json.loads(
                self.run_cli(
                    "init-profile",
                    "--name",
                    "legacy",
                    "--root",
                    str(root),
                    "--activate",
                ).stdout
            )
            profile = Path(created["profile"])
            data = json.loads((profile / "profile.json").read_text())
            del data["owner_identity"]
            (profile / "profile.json").write_text(json.dumps(data) + "\n")

            before = json.loads(
                self.run_cli("identity", "--root", str(root)).stdout
            )
            self.assertEqual("collaborator", before["role"])
            self.assertFalse(before["owner_identity_configured"])
            rebound = json.loads(
                self.run_cli("bind-owner-ip", "--root", str(root)).stdout
            )
            self.assertEqual("owner", rebound["role"])


class PrivacyScanTest(unittest.TestCase):
    def test_detects_assigned_secret(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "safe.txt").write_text("generic example\n")
            passed = subprocess.run(
                [sys.executable, str(PRIVACY_SCAN), str(root)], check=False
            )
            self.assertEqual(0, passed.returncode)
            (root / "unsafe.txt").write_text("api_key=abcdefghijklmnop\n")  # privacy-scan: allow test fixture
            failed = subprocess.run(
                [sys.executable, str(PRIVACY_SCAN), str(root)], check=False
            )
            self.assertEqual(1, failed.returncode)

    def test_team_policy_allows_internal_paths_but_not_secrets(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = root / "team.json"
            config.write_text(
                json.dumps({"skill_path": "/" + "nfs/example/team/SKILL.md"}) + "\n"
            )
            public_result = subprocess.run(
                [sys.executable, str(PRIVACY_SCAN), str(root)], check=False
            )
            self.assertEqual(1, public_result.returncode)
            team_result = subprocess.run(
                [
                    sys.executable,
                    str(PRIVACY_SCAN),
                    "--policy",
                    "team",
                    str(root),
                ],
                check=False,
            )
            self.assertEqual(0, team_result.returncode)
            config.write_text("secret=abcdefghijklmnop\n")  # privacy-scan: allow test fixture
            secret_result = subprocess.run(
                [
                    sys.executable,
                    str(PRIVACY_SCAN),
                    "--policy",
                    "team",
                    str(root),
                ],
                check=False,
            )
            self.assertEqual(1, secret_result.returncode)


if __name__ == "__main__":
    unittest.main()
