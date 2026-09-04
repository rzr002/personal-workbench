# Team pack schema

A team pack is an access-controlled directory outside the public Personal Workbench repository. Its `team.json` contains:

- `schema_version`: team manifest format version.
- `team_id`: immutable generated UUID; it identifies the pack but does not grant access.
- `display_name` and `slug`: human and technical names.
- `created_at` and `updated_at`: UTC timestamps.
- `modules`: shared module names, paths, descriptions, triggers, declared external resource paths, and registration timestamps.

Module paths may be relative to `team.json` or absolute. Prefer relative paths when a Skill is stored in the same internal repository so the pack remains portable.

Each owner's profile stores team attachments in `teams.json`. An attachment records the manifest path and the exact approved content digest. The digest covers the manifest, every file beneath each registered Skill directory, and every explicitly declared external resource, excluding Git and cache metadata. When any covered content changes, that team's modules are withheld until the workbench owner approves the new digest. Collaborators borrowing the workbench inherit the owner's approved team snapshot but cannot approve or change it.

Declare external documents or support directories that materially define Skill behavior. The digest does not represent remote service state, database contents, files that were not declared, or authorization to access the underlying systems.

Team packs may contain internal paths, service locations, data contracts, and operational procedures intended for all authorized members. They must not contain passwords, tokens, private keys, raw conversations, session identifiers, customer records, personal preferences, candidate lessons, or approved personal knowledge.

Repository access and operating-system permissions remain the authority for who may read or edit a team pack. Personal Workbench verifies content approval, not organizational membership.
