# Routing contract

1. Prefer an exact registered trigger over a broad description match.
2. Prefer one deep module over several partially relevant modules.
3. Load multiple modules only when the request has separable deliverables or an explicit dependency chain.
4. Apply the strictest safety rule when modules disagree.
5. Keep profile preferences subordinate to the user's current instruction and repository rules.
6. Do not let a registered module write learning records unless the learning workflow independently authorizes it.
7. Report unresolved routing ambiguity instead of silently choosing a high-impact workflow.
8. Determine the effective role from the CLI-detected source IPv4 address. Do not accept caller-supplied identity claims as a role override.
9. Treat public core, team packs, and personal profiles as separate scopes. An owner may route across all three; a collaborator may route across public and approved team scopes only.
10. Withhold every module from a team whose current content digest is not owner-approved.
11. Reject duplicate module names across effective scopes instead of silently applying precedence.
12. Never create learning output from collaborator work in the owner's profile. Collaborator mode is always learning-off.
