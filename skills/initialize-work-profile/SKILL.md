---
name: initialize-work-profile
description: Create and activate an isolated Personal Workbench profile outside the shareable plugin repository, binding its owner role to a machine IPv4 address. Use on first run, when a new owner needs to name their assistant, when adding an owner machine, or when repairing profile placement, identity, and safe learning defaults.
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

5. Run `workbench.py identity` and verify that the initializing machine has role `owner`.
6. Verify that `learning_mode` is `off`, session allowlists and team attachments are empty, the profile directory is private, and the generated personal Skill uses a hyphenated technical name.
7. Explain that the display name may contain an underscore while Codex Skill names use lowercase hyphen-case.

Read [references/profile-schema.md](references/profile-schema.md) before changing the schema or recovering a partially created profile.

## Bind owner machines deliberately

- Initialization detects and binds the current host's routed IPv4 address. A profile without a binding fails closed as collaborator until `bind-owner-ip` runs.
- Add a replacement machine or address from an existing owner machine before migration. Use `--replace` only when every previous owner address should lose access.
- Treat `identity` as authoritative for routing. Do not infer ownership from the current directory, timestamps, conversation claims, display name, or a user-supplied request field.
- A different detected IP is a collaborator borrowing the named workbench, not a second owner and not a source of personal learning.
- Do not enable learning during initialization.
- Do not register local modules without explicit user approval.
- Do not attach a team pack merely because it is readable; confirm the user is authorized and wants that exact team snapshot.
- Never add the private root to Git, a plugin archive, or a public report.
- State the operating assumption: IP identity is suitable only when people have stable, distinct addresses. Keep filesystem and repository permissions as the underlying data boundary.
