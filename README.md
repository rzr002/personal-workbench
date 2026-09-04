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

Personal Workbench gives Codex one clear entry point for modular work skills. Each named workbench has one owner, identified by a bound machine IP. Generic tooling stays public, internal operational knowledge lives in access-controlled team packs, and the owner's work history and learning stay in a private profile. Coworkers may borrow the named workbench from other machines, but they receive team capabilities only.

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

The role decision is deterministic:

| Detected source IP | Effective role | Available scope | May change the workbench? |
| --- | --- | --- | --- |
| Bound owner IP | Owner | Public + approved team + personal | Yes, through explicit commands and review |
| Any other IP | Collaborator | Public + approved team only | No |

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

The display name may contain underscores. The generated Codex Skill uses the normalized technical name `my-workbench`. Initialization binds the host's detected IPv4 address as the owner machine.

Check the active profile:

```bash
python3 scripts/workbench.py identity --root ~/.personal-workbench
python3 scripts/workbench.py status --root ~/.personal-workbench
```

Every new profile starts with:

- `learning_mode: off`;
- an empty session allowlist;
- an empty private module registry;
- an empty team attachment registry;
- private candidate and approved-knowledge stores;
- an owner identity bound to the initializing machine's IPv4 address;
- a generated personal entry Skill.

Before moving to another owner machine or changing a stable address, add the new address while still on an authorized machine:

```bash
python3 scripts/workbench.py bind-owner-ip \
  --root ~/.personal-workbench \
  --ip '<new-owner-ip>'
```

Use `--replace` only when intentionally removing every previous owner address.

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
  --root ~/.personal-workbench \
  --name example_team \
  --path /shared/internal/example-team

python3 scripts/workbench.py add-team-module \
  --root ~/.personal-workbench \
  --team /shared/internal/example-team \
  --name dataset-operations \
  --skill-path /shared/internal/skills/dataset-operations \
  --description "Create datasets and register internal services" \
  --trigger "create a dataset" \
  --resource-path /shared/internal/docs/dataset-contract.md
```

The workbench owner attaches and approves the shared pack once:

```bash
python3 scripts/workbench.py attach-team \
  --root ~/.personal-workbench \
  --team /shared/internal/example-team
```

Use `--replace-personal` during migration only when same-name personal modules point to the exact same Skill files. A name or path mismatch is rejected.

The profile stores an approved SHA-256 digest covering the team manifest, every registered Skill file, and declared external resources. If any covered manifest, instruction, script, or reference changes, those team modules are withheld until the workbench owner reviews and approves the new digest:

```bash
python3 scripts/workbench.py list-teams --root ~/.personal-workbench

python3 scripts/workbench.py approve-team-update \
  --root ~/.personal-workbench \
  --team example-team \
  --digest CURRENT_DIGEST
```

Team packs provide shared capabilities, not shared memory. A coworker borrowing this named workbench from another IP can use the approved team modules, including internal dataset or service procedures, but cannot see personal modules or use any learning, session, candidate, attachment, or approval command. Candidates and approved lessons remain available only from an owner IP.

### Borrow an owner's workbench

In a controlled shared deployment, point the coworker's installed entry Skill at the same named profile. The coworker verifies the automatically selected role and asks for the effective modules:

```bash
python3 scripts/workbench.py identity --profile '<owner-profile>'
python3 scripts/workbench.py list-modules --profile '<owner-profile>'
```

From any unbound machine IP, both commands report `collaborator`, and `list-modules` returns team entries only. The coworker does not create a second personal profile and cannot contribute learning to the owner's profile. This workflow does not bypass operating-system permissions: the deployment still has to make the entry point and team pack readable without weakening the owner's personal files.

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
3. The local CLI detects the machine's source IPv4 address; a match selects owner mode and every other address selects collaborator mode.
4. Only the owner may attach or approve team snapshots; collaborators inherit that approved shared surface.
5. Learning defaults to off and is forced off in collaborator mode.
6. Exact session IDs must be allowlisted by the owner.
7. Archived prompts, logs, and tool output are treated as untrusted data.
8. Extracted lessons enter a candidate inbox, never an active Skill.
9. Human approval is required before private promotion.
10. Public promotion requires a separate code review and privacy scan.

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

> **Access-control warning:** IP binding is a practical machine-role gate, not cryptographic authentication. It assumes one stable, distinct IP per person. Shared hosts, NAT, reused addresses, or direct filesystem access can defeat that assumption; filesystem/repository permissions remain necessary, and address changes should be bound before migration.

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

This is an early privacy-first foundation. The current release provides IP-based owner/collaborator routing, owner-approved team snapshots, personal module isolation, candidate review, secret redaction, and public/team scanning policies. Automatic session collection and public-skill promotion remain deliberately out of scope until their ownership and validation boundaries are equally reliable.

## License

No open-source license has been selected yet. The source is public for inspection, but reuse terms should be chosen deliberately before broader distribution.

## 中文说明

Personal Workbench 是一个面向 Codex 的“个人工作台”：每个命名工作台只有一个所有者；对外分享干净的通用插件；团队内部路径、服务地址、数据协议和共享 Skill 放在受权限保护的团队包；所有者自己的偏好、工作记录、候选经验和已确认经验保存在私人 Profile。

核心原则很简单：

- 一个统一入口，内部按任务选择最小的 Skill；
- 新用户第一次使用时创建并命名自己的 Profile，同时自动绑定当前机器的内网 IPv4；
- 团队包共享能力，不共享任何人的工作记忆；
- 所有者 IP 命中时可使用公共、团队和个人三层，并拥有唯一的维护与审批权；
- 其他 IP 自动进入协作者模式，只能使用所有者已批准的公共层和团队层；
- 团队内容变化后，只有所有者批准新指纹才能恢复加载；
- 默认不学习，开启后也只生成候选经验；
- 候选经验必须由本人明确审核，不能自动修改正式 Skill；
- 同事借用你的工作台时不能查看个人模块，也不能读取或写入学习记录；
- 对外发布前必须通过隐私扫描、测试和 Git diff 检查。

第一次使用：

```bash
python3 scripts/workbench.py init-profile \
  --name my_workbench \
  --root ~/.personal-workbench \
  --activate
```

标注平台路径、内部接口和团队 SOP 不应该进入公开仓库，也不应该只放在个人区；它们应进入团队包。所有者挂载并批准团队包后，同事从其他 IP 借用这个工作台时就可以使用这些团队能力，但不能修改团队挂载或审批状态。

IP 识别的前提是每个人使用不同且稳定的机器地址。如果多人共用主机、经过同一 NAT、IP 被重复分配，或者同事能直接读取 Profile 文件，IP 本身就不是完整的安全边界；仍需配合系统账号、目录权限、仓库权限或独立的 Codex sessions root。
