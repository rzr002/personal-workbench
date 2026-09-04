---
name: initialize-work-profile
description: Create and activate an isolated Personal Workbench profile outside the shareable plugin repository. Use on first run, when a new user needs to name their assistant, when separating users or machines, or when repairing profile placement and safe learning defaults.
---

# Initialize Work Profile

## Create the profile

1. Ask for the user's profile display name if it is not already explicit.
2. Choose a private root outside the plugin repository. Prefer `~/.personal-workbench`; honor an explicit location.
3. Refuse a root inside a Git working tree unless the user knowingly overrides the privacy recommendation.
4. Run:

```bash
python3 <plugin-root>/scripts/workbench.py init-profile \
  --name '<display-name>' \
  --root '<private-root>' \
  --activate
```

5. Verify that `learning_mode` is `off`, session allowlists are empty, the profile directory is private, and the generated personal Skill uses a hyphenated technical name.
6. Explain that the display name may contain an underscore while Codex Skill names use lowercase hyphen-case.

Read [references/profile-schema.md](references/profile-schema.md) before changing the schema or recovering a partially created profile.

## Keep users separate

- Give every person a different private root or operating-system account when confidentiality matters.
- Do not infer ownership from the current directory, timestamps, conversation claims, or the display name.
- Do not enable learning during initialization.
- Do not register local modules without explicit user approval.
- Never add the private root to Git, a plugin archive, or a public report.
