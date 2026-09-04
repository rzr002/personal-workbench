#!/usr/bin/env python3
"""Scan a Personal Workbench public tree for likely privacy leaks."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path


EXCLUDED_PARTS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".personal-workbench",
    ".personal-workbench-private",
    "profiles",
    "sessions",
    "candidates",
}

PATTERNS = (
    (
        "private-key",
        "critical",
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    ),
    (
        "bearer-token",
        "critical",
        re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._~+/=-]{16,}"),
    ),
    (
        "assigned-secret",
        "critical",
        re.compile(
            r"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)"
            r"\s*[:=]\s*['\"]?[A-Za-z0-9._~+/=-]{12,}"
        ),
    ),
    (
        "absolute-user-path",
        "high",
        re.compile(r"/(?:home|Users|nfs)/[A-Za-z0-9._/-]+"),
    ),
    (
        "email",
        "medium",
        re.compile(
            r"\b[A-Za-z0-9._%+-]+@(?!example\.com\b)[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
        ),
    ),
    ("phone", "medium", re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)")),
    (
        "profile-record",
        "high",
        re.compile(r'"(?:profile_id|allowed_session_ids|source_session_id)"\s*:'),
    ),
)


def git_files(root: Path) -> list[Path] | None:
    result = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "--show-toplevel"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    if Path(result.stdout.strip()).resolve() != root:
        return None
    listed = subprocess.run(
        [
            "git",
            "-C",
            str(root),
            "ls-files",
            "-z",
            "--cached",
            "--others",
            "--exclude-standard",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if listed.returncode != 0:
        raise RuntimeError(listed.stderr.decode("utf-8", errors="replace"))
    return [
        root / value.decode("utf-8")
        for value in listed.stdout.split(b"\0")
        if value
    ]


def public_files(root: Path) -> list[Path]:
    tracked = git_files(root)
    if tracked is not None:
        return tracked
    result = []
    for directory, names, files in os.walk(root):
        names[:] = [name for name in names if name not in EXCLUDED_PARTS]
        base = Path(directory)
        result.extend(base / filename for filename in files)
    return result


def scan(root: Path, policy: str = "public") -> list[tuple[str, str, Path, int]]:
    findings = []
    for path in public_files(root):
        if any(part in EXCLUDED_PARTS for part in path.relative_to(root).parts):
            continue
        try:
            raw = path.read_bytes()
        except OSError:
            continue
        if b"\0" in raw:
            continue
        text = raw.decode("utf-8", errors="replace")
        for line_number, line in enumerate(text.splitlines(), 1):
            if "privacy-scan: allow" in line:
                continue
            for name, severity, pattern in PATTERNS:
                if policy == "team" and name == "absolute-user-path":
                    continue
                if pattern.search(line):
                    findings.append(
                        (severity, name, path.relative_to(root), line_number)
                    )
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument(
        "--policy",
        choices=("public", "team"),
        default="public",
        help="public blocks internal paths; team allows paths but still blocks secrets and personal records",
    )
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()
    findings = scan(root, policy=args.policy)
    for severity, name, path, line in findings:
        print(f"{severity}: {name}: {path}:{line}")
    if findings:
        print(
            f"privacy scan failed with {len(findings)} finding(s)", file=sys.stderr
        )
        return 1
    print("privacy scan passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
