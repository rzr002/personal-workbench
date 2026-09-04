# Profile schema

`profile.json` contains:

- `schema_version`: profile format version.
- `profile_id`: generated immutable UUID, not a proof of identity.
- `display_name`: user-facing name such as `my_workbench`.
- `slug`: lowercase hyphenated technical name.
- `created_at`: UTC creation timestamp.
- `learning_mode`: `off` or `candidate`.
- `allowed_session_ids`: exact session IDs eligible for distillation.
- `allowed_session_roots`: informational approved roots; an ID is still required for candidate creation.

`modules.json` is private and stores explicitly registered local module names, paths, descriptions, and triggers. The profile also contains pending and reviewed candidate directories, an append-only approved-knowledge file, an audit log, and a generated private entry Skill.

Do not add raw transcripts, access tokens, account claims, or copied environment dumps to this schema.
