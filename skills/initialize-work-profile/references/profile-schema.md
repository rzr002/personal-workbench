# Profile schema

`profile.json` contains:

- `schema_version`: profile format version.
- `profile_id`: generated immutable UUID, not a proof of identity.
- `display_name`: user-facing name such as `my_workbench`.
- `slug`: lowercase hyphenated technical name.
- `created_at`: UTC creation timestamp.
- `owner_identity`: private IP identity configuration containing `type: ip`, one or more normalized IPv4 `addresses`, and binding timestamps.
- `learning_mode`: `off` or `candidate`.
- `allowed_session_ids`: exact session IDs eligible for distillation.
- `allowed_session_roots`: informational approved roots; an ID is still required for candidate creation.

`modules.json` is private and stores explicitly registered personal module names, paths, descriptions, and triggers.

`teams.json` is private and stores attached team IDs, manifest paths, and owner-approved content digests. It does not copy team modules or grant filesystem access. A missing `teams.json` is treated as an empty registry for compatibility with older profiles.

The CLI detects the current machine address locally. When it matches an `owner_identity.addresses` entry, the effective role is `owner`; otherwise it is `collaborator`. A legacy profile with no owner identity fails closed as collaborator, but permits a one-time initial binding from the machine holding the private profile. Once configured, only an existing owner machine may add or replace bindings.

Owner mode may access personal and approved team modules and may perform profile mutations. Collaborator mode receives approved team modules only, reports learning as off, omits personal status fields, and rejects personal reads, learning changes, session authorization, module registration, team attachment or approval changes, and candidate operations.

The profile also contains pending and reviewed candidate directories, an append-only approved-knowledge file, an audit log, and a generated private entry Skill.

Do not add raw transcripts, access tokens, account claims, or copied environment dumps to this schema. The IP binding is an operational machine-role gate, not cryptographic proof; filesystem permissions still protect the underlying profile from direct reads.
