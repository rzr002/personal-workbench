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


if __name__ == "__main__":
    unittest.main()
