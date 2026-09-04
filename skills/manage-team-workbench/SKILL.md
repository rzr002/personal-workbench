---
name: manage-team-workbench
description: Create, populate, attach, inspect, and owner-approve updates to internal Personal Workbench team packs. Use when coworkers borrowing a named workbench need shared operational Skills, internal paths, service endpoints, schemas, or SOPs without gaining access to the owner's personal modules or learning records.
---

# Manage Team Workbench

Keep team knowledge outside the public plugin and personal profiles. A team pack may reference internal Skills and documentation, but it must never contain credentials, session archives, candidates, or personal preferences.

Run `workbench.py identity` first. Creating or changing a team pack, attaching or detaching it, and approving a new digest require role `owner`. In collaborator mode, only inspect and use the already approved team modules returned by `list-modules`.

Read [references/team-pack-schema.md](references/team-pack-schema.md) before creating or changing a team pack.

## Create a team pack

Choose an access-controlled shared directory or internal repository outside the public plugin:

```bash
python3 <plugin-root>/scripts/workbench.py init-team \
  --root '<private-root>' \
  --name '<team display name>' \
  --path '<internal-team-directory>'
```

Register only modules the whole authorized team may use:

```bash
python3 <plugin-root>/scripts/workbench.py add-team-module \
  --root '<private-root>' \
  --team '<internal-team-directory>' \
  --name '<module name>' \
  --skill-path '<path-to-SKILL.md-or-directory>' \
  --description '<team-facing purpose>' \
  --trigger '<example request>' \
  --resource-path '<external-authoritative-document>'
```

Prefer paths relative to the team manifest when the Skill lives in the same internal repository. Declare every behavior-defining file or directory outside the Skill folder with repeatable `--resource-path` options so changes also require approval. Never move internal paths or endpoints into the public plugin merely to make onboarding easier.

## Attach a team to an owner's workbench

Confirm that the user is authorized to access the team material, then attach the current content snapshot:

```bash
python3 <plugin-root>/scripts/workbench.py attach-team \
  --team '<internal-team-directory>'
```

The attachment is controlled by the workbench owner. Once approved, team modules become available to both owner and collaborator roles, while personal modules, learning candidates, and approved lessons remain owner-only.

When migrating existing personal registrations, use `--replace-personal` only after checking that the same module names point to the same Skill files. The command rejects a path mismatch instead of silently substituting different instructions.

## Review team updates

Run `list-teams` before routing. A changed manifest, Skill, script, or reference produces `approval-required`; do not load modules from that team.

```bash
python3 <plugin-root>/scripts/workbench.py list-teams
```

Show the user what changed using the internal repository's trusted diff or release notes. After explicit approval, bind the exact displayed digest:

```bash
python3 <plugin-root>/scripts/workbench.py approve-team-update \
  --team '<team slug>' \
  --digest '<current digest from list-teams>'
```

Only an owner IP may execute approval. Never treat continued use, a collaborator's request, or a matching team name as the workbench owner's approval.

Detach a team only when the profile owner explicitly asks:

```bash
python3 <plugin-root>/scripts/workbench.py detach-team --team '<team slug>'
```

Detaching removes only the private reference and approval; it does not delete or modify the shared team pack.

## Enforce boundaries

- Use filesystem groups, repository permissions, or separate operating-system accounts for real access control.
- Keep secrets in credential stores or environment configuration, not team manifests or Skills.
- Keep work history, candidate lessons, and approved personal knowledge in the owner's private profile.
- Collaborators may inspect and use the role-filtered approved team modules, but may not attach, detach, or approve team content through the borrowed profile.
- Run `python3 <plugin-root>/scripts/privacy_scan.py --policy team <team-directory>` before sharing a pack internally.
- Run the stricter public policy before publishing anything outside the team.
