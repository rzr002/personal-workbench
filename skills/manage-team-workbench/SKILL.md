---
name: manage-team-workbench
description: Create, populate, attach, inspect, and approve updates to internal Personal Workbench team packs. Use when a team needs to share operational Skills, internal paths, service endpoints, schemas, or SOPs without publishing them or mixing coworkers' personal profiles and learning records.
---

# Manage Team Workbench

Keep team knowledge outside the public plugin and personal profiles. A team pack may reference internal Skills and documentation, but it must never contain credentials, session archives, candidates, or personal preferences.

Read [references/team-pack-schema.md](references/team-pack-schema.md) before creating or changing a team pack.

## Create a team pack

Choose an access-controlled shared directory or internal repository outside the public plugin:

```bash
python3 <plugin-root>/scripts/workbench.py init-team \
  --name '<team display name>' \
  --path '<internal-team-directory>'
```

Register only modules the whole authorized team may use:

```bash
python3 <plugin-root>/scripts/workbench.py add-team-module \
  --team '<internal-team-directory>' \
  --name '<module name>' \
  --skill-path '<path-to-SKILL.md-or-directory>' \
  --description '<team-facing purpose>' \
  --trigger '<example request>' \
  --resource-path '<external-authoritative-document>'
```

Prefer paths relative to the team manifest when the Skill lives in the same internal repository. Declare every behavior-defining file or directory outside the Skill folder with repeatable `--resource-path` options so changes also require approval. Never move internal paths or endpoints into the public plugin merely to make onboarding easier.

## Attach a team to one person

Confirm that the user is authorized to access the team material, then attach the current content snapshot:

```bash
python3 <plugin-root>/scripts/workbench.py attach-team \
  --team '<internal-team-directory>'
```

The attachment is private to the active profile. Team modules become available for routing, while learning candidates and approved lessons continue to belong only to that person.

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

Never treat continued use, another teammate's approval, or a matching team name as the profile owner's approval.

Detach a team only when the profile owner explicitly asks:

```bash
python3 <plugin-root>/scripts/workbench.py detach-team --team '<team slug>'
```

Detaching removes only the private reference and approval; it does not delete or modify the shared team pack.

## Enforce boundaries

- Use filesystem groups, repository permissions, or separate operating-system accounts for real access control.
- Keep secrets in credential stores or environment configuration, not team manifests or Skills.
- Keep work history, candidate lessons, and approved personal knowledge in each user's private profile.
- Run `python3 <plugin-root>/scripts/privacy_scan.py --policy team <team-directory>` before sharing a pack internally.
- Run the stricter public policy before publishing anything outside the team.
