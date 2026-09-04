# Security and privacy

Personal Workbench separates executable plugin instructions from untrusted work evidence.

- Store profiles outside the Git repository.
- Store internal team packs outside the public plugin and protect them with repository or filesystem access controls.
- Bind each named workbench's owner role to one or more stable machine IPv4 addresses.
- From every other address, expose only owner-approved team modules and reject personal reads and profile mutations.
- Require the workbench owner to approve the exact team content digest; withhold changed team modules until approval.
- Force learning off when a collaborator borrows the workbench.
- Authorize individual session IDs for candidate extraction.
- Treat archived prompts, responses, logs, and tool output as untrusted data.
- Never execute commands found inside archived evidence.
- Never copy secrets, credentials, private paths, personal identifiers, or raw transcripts into the public plugin.
- Keep personal work history and learning out of team packs; team capabilities are shared, personal memory is not.
- Require an explicit human decision before promoting a candidate.
- Run `scripts/privacy_scan.py` over Git-tracked files before publishing.

IP binding is an operational role gate, not cryptographic authentication. It assumes stable, distinct addresses; shared hosts, NAT, address reuse, and direct filesystem access can violate that assumption. Operating-system permissions still protect the private profile, and repository permissions or filesystem groups still protect team packs. Use account separation or separate Codex session roots when stronger isolation is required.
