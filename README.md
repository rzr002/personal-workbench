<p align="center">
  <img src="./assets/architecture.svg" alt="Personal Workbench architecture" width="100%" />
</p>

<h1 align="center">Personal Workbench</h1>

<p align="center">
  A privacy-first Codex plugin for public tooling, approved team capabilities, and private personal learning.
</p>

<p align="center">
  <a href="#quick-start">Quick start</a> ·
  <a href="#privacy-model">Privacy model</a> ·
  <a href="#included-skills">Included skills</a> ·
  <a href="#中文说明">中文说明</a>
</p>

---

Personal Workbench gives Codex one clear entry point for modular work skills. Generic tooling stays public, internal operational knowledge lives in access-controlled team packs, and each person's work history and learning stay in a private profile. Neither a team update nor a candidate lesson becomes active for a person without explicit approval.

## Why this exists

Useful work habits are usually scattered across prompts, local scripts, project notes, and chat history. Copying all of that into one large Skill creates three problems:

- irrelevant instructions consume context;
- personal or company details are easy to leak;
- automatic self-editing makes behavior hard to review or roll back.

Personal Workbench keeps these concerns separate:

| Layer | Contains | Shareable? |
| --- | --- | --- |
| Public plugin | Routing rules, profile tooling, review workflow, privacy checks | Yes |
| Team pack | Internal Skills, paths, endpoints, schemas, and shared SOPs | Authorized team only |
| Private profile | Personal modules, team approvals, preferences, candidates, approved lessons | Owner only |
| Session evidence | Explicitly authorized local work records | Owner only |

## Included skills

| Skill | Purpose |
| --- | --- |
| [`use-workbench`](./skills/use-workbench/SKILL.md) | Route a request through the active profile and smallest relevant module |
| [`initialize-work-profile`](./skills/initialize-work-profile/SKILL.md) | Create an isolated profile with learning disabled |
| [`manage-team-workbench`](./skills/manage-team-workbench/SKILL.md) | Share internal modules and approve exact team snapshots |
| [`distill-work-experience`](./skills/distill-work-experience/SKILL.md) | Turn authorized evidence into sanitized candidates |
| [`review-experience-candidates`](./skills/review-experience-candidates/SKILL.md) | Approve, revise, reject, or defer proposed lessons |
| [`audit-workbench-privacy`](./skills/audit-workbench-privacy/SKILL.md) | Check public files before committing or sharing |

The repository itself is a Codex plugin. Additional domain-specific Skills stay where they already live and are referenced only by a private module registry.

## Quick start

Requirements: Python 3.10+ and Git.

```bash
git clone https://github.com/rzr002/personal-workbench.git
cd personal-workbench

python3 scripts/workbench.py init-profile \
  --name my_workbench \
  --root ~/.personal-workbench \
  --activate
```

The display name may contain underscores. The generated Codex Skill uses the normalized technical name `my-workbench`.

Check the active profile:

```bash
python3 scripts/workbench.py status --root ~/.personal-workbench
```

Every new profile starts with:

- `learning_mode: off`;
- an empty session allowlist;
- an empty private module registry;
- an empty team attachment registry;
- private candidate and approved-knowledge stores;
- a generated personal entry Skill.

## Connect a personal skill

Register a local Skill by reference. Its absolute path is written only to the private profile:

```bash
python3 scripts/workbench.py add-module \
  --root ~/.personal-workbench \
  --name incident-diagnosis \
  --skill-path /path/to/local-skill \
  --description "Diagnose incidents from bounded local evidence" \
  --trigger "diagnose this incident"
```

The public plugin does not copy or publish that Skill. Use a team pack instead when every authorized coworker should receive the capability.

## Share internal team capabilities

Create a team pack in an access-controlled shared directory or internal repository—not inside this public repository:

```bash
python3 scripts/workbench.py init-team \
  --name example_team \
  --path /shared/internal/example-team

python3 scripts/workbench.py add-team-module \
  --team /shared/internal/example-team \
  --name dataset-operations \
  --skill-path /shared/internal/skills/dataset-operations \
  --description "Create datasets and register internal services" \
  --trigger "create a dataset" \
  --resource-path /shared/internal/docs/dataset-contract.md
```

Each coworker creates their own profile and explicitly attaches the shared pack:

```bash
python3 scripts/workbench.py attach-team \
  --root ~/.personal-workbench \
  --team /shared/internal/example-team
```

Use `--replace-personal` during migration only when same-name personal modules point to the exact same Skill files. A name or path mismatch is rejected.

The profile stores an approved SHA-256 digest covering the team manifest, every registered Skill file, and declared external resources. If any covered manifest, instruction, script, or reference changes, those team modules are withheld until that profile owner reviews and approves the new digest:

```bash
python3 scripts/workbench.py list-teams --root ~/.personal-workbench

python3 scripts/workbench.py approve-team-update \
  --root ~/.personal-workbench \
  --team example-team \
  --digest CURRENT_DIGEST
```

Team packs provide shared capabilities, not shared memory. Candidates and approved lessons always remain in the active person's private profile.

## Controlled learning

Learning has two gates: candidate mode must be enabled, and the exact source session must be authorized.

```bash
python3 scripts/workbench.py set-learning \
  --root ~/.personal-workbench \
  --mode candidate

python3 scripts/workbench.py authorize-session \
  --root ~/.personal-workbench \
  --session-id SESSION_ID
```

Create a candidate—not an active rule:

```bash
python3 scripts/workbench.py add-candidate \
  --root ~/.personal-workbench \
  --source-session SESSION_ID \
  --title "Bound the evidence before diagnosing" \
  --lesson "Resolve the smallest relevant evidence window before drawing conclusions." \
  --confidence medium
```

Review it explicitly:

```bash
python3 scripts/workbench.py list-candidates --root ~/.personal-workbench

python3 scripts/workbench.py review-candidate \
  --root ~/.personal-workbench \
  --candidate CANDIDATE_ID \
  --decision approve
```

Approval updates only the private knowledge log. Updating a public Skill remains a normal Git change with tests, review, versioning, and rollback.

## Privacy model

Personal Workbench enforces a practical boundary:

1. Profiles and team packs live outside the public repository.
2. Team packs use real filesystem or repository access control.
3. Every person separately approves the exact team content they load.
4. Learning defaults to off.
5. Exact session IDs must be allowlisted.
6. Archived prompts, logs, and tool output are treated as untrusted data.
7. Extracted lessons enter a candidate inbox, never an active Skill.
8. Human approval is required before private promotion.
9. Public promotion requires a separate code review and privacy scan.

Before publishing changes:

```bash
python3 scripts/privacy_scan.py .
python3 -m unittest discover -s tests -v
git diff --check
```

Before sharing a team pack internally, use the team policy, which permits operational paths but still blocks secrets and personal records:

```bash
python3 scripts/privacy_scan.py --policy team /shared/internal/example-team
```

The scanner detects common secrets, credentials, private keys, personal identifiers, profile records, session records, and absolute user paths. Manual review is still required for confidential business context that does not match a pattern.

> **Access-control warning:** a profile or team name is not a security boundary. Protect team packs with repository permissions or filesystem groups, and use separate operating-system accounts or Codex session roots when users must not read one another's personal data.

## Repository layout

```text
personal-workbench/
├── .codex-plugin/plugin.json
├── assets/architecture.svg
├── scripts/
│   ├── privacy_scan.py
│   └── workbench.py
├── skills/
│   ├── audit-workbench-privacy/
│   ├── distill-work-experience/
│   ├── initialize-work-profile/
│   ├── manage-team-workbench/
│   ├── review-experience-candidates/
│   └── use-workbench/
└── tests/test_workbench.py
```

## Project status

This is an early privacy-first foundation. The current release provides deterministic profile isolation, owner-approved team snapshots, personal module registration, candidate review, secret redaction, and public/team scanning policies. Automatic session collection and public-skill promotion remain deliberately out of scope until their ownership and validation boundaries are equally reliable.

## License

No open-source license has been selected yet. The source is public for inspection, but reuse terms should be chosen deliberately before broader distribution.

## 中文说明

Personal Workbench 是一个面向 Codex 的“个人工作台”：对外分享干净的通用插件；团队内部路径、服务地址、数据协议和共享 Skill 放在受权限保护的团队包；每个人自己的偏好、工作记录、候选经验和已确认经验保存在私人 Profile。

核心原则很简单：

- 一个统一入口，内部按任务选择最小的 Skill；
- 新用户第一次使用时创建并命名自己的 Profile；
- 团队包共享能力，不共享任何人的工作记忆；
- 团队内容变化后，各成员必须分别批准新指纹才能继续加载；
- 默认不学习，开启后也只生成候选经验；
- 候选经验必须由本人明确审核，不能自动修改正式 Skill；
- 同事使用时创建自己的 Profile，不会写入你的个人记录；
- 对外发布前必须通过隐私扫描、测试和 Git diff 检查。

第一次使用：

```bash
python3 scripts/workbench.py init-profile \
  --name my_workbench \
  --root ~/.personal-workbench \
  --activate
```

标注平台路径、内部接口和团队 SOP 不应该进入公开仓库，也不应该只放在某个人的 Profile；它们应进入团队包，由每位有权限的同事挂载。无论任务使用了哪个团队 Skill，学习结果始终只进入当前用户自己的 Profile。

如果多人共用同一台机器或同一个系统账号，仅靠 Profile 或团队名称无法实现真正的权限隔离；需要使用独立系统账号、仓库权限或独立的 Codex sessions root。
