# Candidate schema

Each private candidate contains:

- `candidate_id`
- `status`: initially `pending`
- `title`
- `observation`
- `lesson`
- `evidence_summary`
- `uncertainty`
- `validation_idea`
- `confidence`: `low`, `medium`, or `high`
- `source_session_id`
- `created_at`

A candidate is a proposal, not active behavior. Keep evidence summaries minimal and paraphrased. Never store raw transcript blocks merely to make a candidate look better supported.
