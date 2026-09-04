---
name: audit-workbench-privacy
description: Audit a Personal Workbench repository or export for secrets, personal identifiers, private paths, profile data, unsafe learning behavior, and accidental session content. Use before committing, publishing, sharing, packaging, or promoting private experience into the public plugin.
---

# Audit Workbench Privacy

## Run the deterministic scan

From the plugin repository, run:

```bash
python3 scripts/privacy_scan.py .
```

When Git is initialized, the scanner checks tracked files so ignored private data does not become a noisy false positive. Before Git initialization it scans the public tree while excluding known private and cache directories.

Read [references/privacy-policy.md](references/privacy-policy.md) for the manual checks that pattern matching cannot prove.

## Inspect the boundary manually

Verify that:

- Profiles and active-profile pointers live outside the repository.
- No registered module contains a personal absolute path in public files.
- No raw transcript, session dump, screenshot, log bundle, customer record, or candidate inbox is tracked.
- Learning defaults to off and candidate creation requires an explicitly authorized session ID.
- Candidate approval updates private knowledge only.
- Archived evidence is always treated as untrusted data.
- Public behavior changes remain reviewable Git changes with tests and rollback.

Block publishing on any secret, credential, private key, personal path, profile record, or unexplained identifier. Redact or replace it with a generic example, rerun the scan and tests, then inspect the staged diff.
