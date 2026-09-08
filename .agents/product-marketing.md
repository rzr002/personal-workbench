# Product Marketing Context

**Document version:** v1
**Last updated:** 2026-09-08
**Basis:** Current public implementation. Audience and conversion goals are working assumptions, not customer research.

## Product overview

Personal Workbench provides one named entry point for registered Codex skills. Six bundled skills support routing, private profiles, team snapshots, candidate extraction, candidate review, and privacy checks. Python tooling manages the local state. Early release 0.3.0; consult the repository's License section for current reuse terms.

## Audience and problem

Primary audience: Codex users who already maintain multiple skills or recurring work routines. Secondary audience: people managing internal team procedures in controlled environments. They need to find relevant capabilities, keep personal and team stores separate, and review proposed learning before adoption. Customer demand and willingness to pay have not been established.

## Positioning and differentiation

- Register existing skills by reference and route to the smallest relevant module.
- Maintain separate public tooling, approved team packs, and private profiles.
- Require approval for changed team content snapshots.
- Keep learning off initially; authorized lessons enter a review inbox.
- Create a named private entry skill and make its installation steps explicit.

## Alternatives and related projects

Manually selecting skills and maintaining a large instruction file are workflow alternatives; no comparative benchmark is available. Reflect Workday provides daily or weekly recall. WorkSkill distills methods into a wiki and skill candidates. There is no automatic import or synchronization of those projects' personal data.

## Objections and boundaries

- Does profile creation install the skills? No. Users must also expose the bundled skills and generated entry skill to Codex.
- Is machine IP authentication? It is an operational role selector. Shared addresses, hosts, and direct file access can defeat its assumptions; filesystem/repository permissions remain necessary.
- Does it collect sessions automatically? No. Collection is outside the current implementation.
- Does it rewrite public skills automatically? No. Candidate approval updates private knowledge; public changes use normal review.
- Is this an enterprise access-control platform? No. Describe the exact controls and their limits.

## Voice and evidence

Direct, developer-oriented, English with a practical Chinese guide. Lead with skill routing and reviewable learning, not abstract privacy or autonomous-evolution promises. Avoid unsupported claims about secure multi-user isolation, automatic collection, performance gains, customers, or time saved. No verified customer quotes are available.

Proof sources: `scripts/workbench.py`, `tests/test_workbench.py`, `skills/use-workbench/SKILL.md`, and `SECURITY.md`. The architecture image explains the model; it is not a product screenshot.

## Goal

Primary README action: create a profile, expose its skills to Codex, and inspect available modules with learning off. Secondary action: register one existing personal skill. GitHub visits and clones do not measure successful setup; no usage telemetry is present.

## Changelog

- v1 (2026-09-08) — Capture skill-routing positioning, complete first-use steps, and the limits of role selection and learning.
