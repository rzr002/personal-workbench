---
name: review-experience-candidates
description: Review pending Personal Workbench learning candidates and record explicit approve, revise, or reject decisions in the private profile. Use when a user asks what the workbench learned, wants to curate its memory, correct a proposed lesson, or promote a validated candidate without modifying the public plugin.
---

# Review Experience Candidates

## Review deliberately

1. Run `workbench.py identity` and stop unless the role is `owner`.
2. List pending candidates with `python3 <plugin-root>/scripts/workbench.py list-candidates`.
3. Present the observation, proposed lesson, uncertainty, evidence summary, and validation idea separately. Do not hide weak evidence behind confident wording.
4. Ask the profile owner for an explicit decision on each candidate: approve, revise, reject, or defer.
5. For approve or reject, run:

```bash
python3 <plugin-root>/scripts/workbench.py review-candidate \
  --candidate '<candidate-id>' \
  --decision '<approve|reject>'
```

Use `--lesson '<revised lesson>'` when the owner revises an approved lesson.

Read [references/promotion-policy.md](references/promotion-policy.md) before approving a candidate that affects safety, destructive operations, external communication, or shared behavior.

## Preserve provenance

- Keep the original candidate, review decision, timestamp, and any revised lesson.
- Approved lessons enter only the private approved-knowledge log.
- Reject project-specific claims that are framed as universal rules.
- Require a separate code change, tests, version bump, and privacy audit before moving a private lesson into the public plugin.
- Never interpret silence or continued use as approval.
