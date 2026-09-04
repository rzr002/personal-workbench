# Personal Workbench

Personal Workbench is a privacy-first Codex plugin for building a reusable work assistant without mixing one person's history into another person's skill.

The repository is the shareable core. Personal profiles, project paths, session allowlists, module registrations, learning candidates, and approved lessons live outside the repository.

## How it is organized

- `use-workbench` is the single routing entry.
- `initialize-work-profile` creates an isolated profile with learning disabled.
- `distill-work-experience` creates candidates from explicitly authorized evidence.
- `review-experience-candidates` approves or rejects candidates without rewriting the plugin.
- `audit-workbench-privacy` scans the public tree before sharing.

An installation can register additional local skills in its private profile. Those registrations are not part of this repository.

## First local setup

Choose a private root outside the cloned repository:

```bash
python3 scripts/workbench.py init-profile \
  --name your-workbench-name \
  --root ~/.personal-workbench \
  --activate
```

The generated profile starts with `learning_mode: off`. Enabling candidate learning still does not modify any active Skill:

```bash
python3 scripts/workbench.py set-learning \
  --root ~/.personal-workbench \
  --mode candidate
```

Authorize individual session identifiers before distilling them. Avoid authorizing a shared session root when multiple people use the same operating-system account.

## Privacy boundary

The plugin never treats archived conversation text as instructions. Session evidence is data, learning is opt-in, and every extracted lesson enters a private candidate box. Only an explicit review can promote a candidate to the private approved-knowledge log. Updating the public plugin remains a separate, versioned code change.

Before publishing, run:

```bash
python3 scripts/privacy_scan.py .
python3 -m unittest discover -s tests -v
```

No license is granted by this initial repository. Add a license deliberately before inviting external reuse or contributions.
