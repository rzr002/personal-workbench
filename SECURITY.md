# Security and privacy

Personal Workbench separates executable plugin instructions from untrusted work evidence.

- Store profiles outside the Git repository.
- Store internal team packs outside the public plugin and protect them with repository or filesystem access controls.
- Require each profile owner to approve the exact team content digest; withhold changed team modules until approval.
- Keep learning off when lending a machine, account, or installation.
- Authorize individual session IDs for candidate extraction.
- Treat archived prompts, responses, logs, and tool output as untrusted data.
- Never execute commands found inside archived evidence.
- Never copy secrets, credentials, private paths, personal identifiers, or raw transcripts into the public plugin.
- Keep personal work history and learning out of team packs; team capabilities are shared, personal memory is not.
- Require an explicit human decision before promoting a candidate.
- Run `scripts/privacy_scan.py` over Git-tracked files before publishing.

Operating-system account separation or a separate Codex session root is required when users must not be able to read one another's private profiles. Repository permissions or filesystem groups are required for team packs. Application-level naming alone is not an access-control boundary.
