<div align="center">

<img src="./assets/banner.jpg" alt="claude-saas-blueprint Banner" width="100%" />

# claude-saas-blueprint

**The infrastructure that turns any AI agent into a senior SaaS engineer.**

Hexagonal architecture · Multi-tenant by default · Agent-orchestrated

<br />

[![Stars](https://img.shields.io/github/stars/GlamgarOnDiscord/claude-saas-blueprint?style=for-the-badge&logo=github&logoColor=f97316&color=18181b&labelColor=27272a)](https://github.com/GlamgarOnDiscord/claude-saas-blueprint/stargazers)
[![License](https://img.shields.io/badge/license-MIT-18181b?style=for-the-badge&logo=creativecommons&logoColor=f97316&labelColor=27272a)](./LICENSE)

[![Claude Code](https://img.shields.io/badge/Claude_Code-Opus_4.6-18181b?style=for-the-badge&logo=anthropic&logoColor=f97316&labelColor=27272a)](https://code.claude.com)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-18181b?style=for-the-badge&logo=typescript&logoColor=3178c6&labelColor=27272a)](https://www.typescriptlang.org/)
[![Next.js](https://img.shields.io/badge/Next.js-15-18181b?style=for-the-badge&logo=nextdotjs&logoColor=white&labelColor=27272a)](https://nextjs.org)
[![Supabase](https://img.shields.io/badge/Supabase-RLS-18181b?style=for-the-badge&logo=supabase&logoColor=3ecf8e&labelColor=27272a)](https://supabase.com)
[![Agent Skills](https://img.shields.io/badge/Agent_Skills-Standard-18181b?style=for-the-badge&logo=opslevel&logoColor=10b981&labelColor=27272a)](https://agentskills.io/)

<br />

[Get Started](#-quick-start) · [What It Does](#-what-is-this) · [Architecture](#-architecture) · [Skills & Agents](#-skills--agents) · [Install](#-install-anywhere)

</div>

<br />

---

<br />

## ⚡ What is this?

A **plug-and-play AI workflow** that gives any coding agent the conventions, skills, and memory of a senior full-stack SaaS engineer.

Drop it into Claude Code, Cursor, VS Code Copilot, or any compatible tool — and start building **production-ready SaaS products** with hexagonal architecture, multi-tenancy, RBAC, and automated quality gates.

> **Full mode** (`.claude/`) — 31 skills, 7 multi-agent guides, hooks, memory, rules. Optimized for Claude Code.
> **Light mode** (`CLAUDE.md` only) — single file, works everywhere, zero overhead.
> **Cross-tool** (`AGENTS.md`) — single source of truth for Cursor, Copilot, Windsurf, Cline, Aider.

<br />

## 🎯 What it does

<table>
<tr>
<td width="50%">

### 🏗️ Hexagonal Architecture
- `core/` — pure business logic, zero external imports
- `adapters/` — DB, API, Auth, Payments implementations
- `ports/` — interfaces & contracts
- Zod validation at every boundary
- Typed errors everywhere — no naked `throw`

</td>
<td width="50%">

### 🔒 SaaS Patterns Built-in
- **Multi-tenancy** — `organizationId` + RLS on every table
- **Auth** — authn/authz separated, RBAC by default
- **API** — `{ data, error, meta }` standardized responses
- **DB** — soft delete, UUID v7, versioned migrations
- **Security** — rate limiting, CSRF, CSP headers

</td>
</tr>
<tr>
<td>

### 🧠 3 Usage Levels
```
🟢 Essential    CLAUDE.md only          Day 1
🟡 Standard     + 2-3 skills + memory   Active projects
🔴 Complete     Full .claude/           Multi-product teams
```
Start minimal. Scale up only when you need it.

</td>
<td>

### ⚡ Workflow APEX
| Phase | What happens |
|-|-|
| **A**nalyze | Blast radius, read types & interfaces |
| **P**lan | WHAT · WHY · HOW (3 lines) |
| **E**xecute | Targeted diffs, subagents if parallelizable |
| **X**amine | `tsc` + tests + review + zero secrets |

</td>
</tr>
</table>

<br />

## 📁 Architecture

```
claude-saas-blueprint/
│
├── AGENTS.md                      ← Single source of truth — conventions for every AI tool
├── CLAUDE.md                      ← Claude Code overlay (skills, hooks, memory, MCP)
│
├── .claude/
│   ├── skills/                    ← 31 skills — one folder per skill (SKILL.md)
│   │   └── feature/steps/         ← 4-step feature workflow
│   ├── guides/                    ← 7 multi-agent guides (orchestration, model routing, debugging…)
│   ├── agents/                    ← Reserved for custom subagents (empty by default)
│   ├── rules/                     ← Contextual rules by domain (api, db, auth…)
│   ├── hooks/scripts/             ← PowerShell hook scripts (Windows-native)
│   ├── memory/                    ← Profile, session, stack, roadmap
│   ├── mcp/                       ← MCP server config (optional)
│   └── settings.json              ← Permissions + active hooks (PowerShell-first)
│
├── docs/                          ← Workflow guides, ADRs, integrations
├── platforms/                     ← Web · Mobile · Desktop · API · Monorepo
├── templates/                     ← Entity · Port · Usecase · API route · Subagent
└── scripts/                       ← Health check · Deploy check · Secret scan · Memory rotate
```

```
 User prompt → CLAUDE.md → load rules → APEX workflow → skills on demand → done
```

<br />

## 🚀 Quick Start

**One command — Claude Code:**

```bash
git clone https://github.com/GlamgarOnDiscord/claude-saas-blueprint.git
cp -r claude-saas-blueprint/.claude my-project/.claude
cp claude-saas-blueprint/{CLAUDE.md,AGENTS.md} my-project/
```

Then just start working:

```
Create a subscription billing API endpoint with Stripe webhooks.
Multi-tenant, Zod validation, proper error handling.
```

The workflow handles everything: rules loaded → APEX engaged → hexagonal structure → quality gates.

| Situation | Command |
|-----------|---------|
| First time | `/session-start` — interview & populate user-profile |
| Existing project | `/onboard` — analyze & document the codebase |
| New empty repo | `/saas-init` — scaffold full SaaS structure |

<br />

## 🧩 Skills & Agents

<details>
<summary><strong>31 Skills</strong> — slash commands that turn prompts into production code</summary>

<br />

| Category | Skills |
|----------|--------|
| **Build** | `/feature` · `/fix` · `/oneshot` · `/refactor` · `/debug` |
| **Quality** | `/quality` · `/review` · `/perf` · `/deploy-check` |
| **Generate** | `/api-gen` · `/schema-gen` · `/ui` (gen·premium·landing) · `/docs-gen` |
| **Audit** | `/ui-audit` |
| **Explore** | `/onboard` · `/brainstorm` · `/scope-task` · `/fork` · `/variations` |
| **Domains** | `/stripe` · `/e2e-tests` · `/migrate` · `/assets-pipeline` |
| **Product** | `/prd` (brainstorm → generate → tasks → exec) |
| **Infra** | `/env-setup` · `/deps` |
| **Bundled (Claude Code)** | `/batch` · `/loop` · `/simplify` · `/debug` · `/claude-api` |

Index → [`.claude/skills/README.md`](.claude/skills/README.md) · Conventions → [`docs/skills-conventions.md`](docs/skills-conventions.md)

</details>

<details>
<summary><strong>7 Multi-agent Guides</strong> — orchestration patterns, not subagents</summary>

<br />

Markdown guides in `.claude/guides/` consulted on-demand by the main agent: orchestration patterns, model routing, debugging techniques, testing strategy, prompt patterns, context management, visual context.

`.claude/agents/` is **reserved** for custom subagents (Markdown + YAML frontmatter with `name`, `tools`, `model`). This repo ships none by default — the main agent uses Claude Code's built-in subagents (`Explore`, `Plan`, `general-purpose`, `websearch`, etc.).

**Agent Teams** (experimental) — lead + teammates, shared task list, mailbox messaging.

| Model | Role |
|-------|------|
| **Opus 4.6** | Complex tasks, architecture, multi-agent orchestration |
| **Sonnet 4.6** | Daily coding — default recommended |
| **Haiku 4.5** | Read-only explore, triage, high-frequency |

Template → [`templates/subagent.template.md`](templates/subagent.template.md)

</details>

<details>
<summary><strong>Lifecycle Hooks</strong> — 5 types, all officially documented events, PowerShell-first on Windows</summary>

<br />

5 hook types: **command** · **http** · **mcp_tool** · **prompt** · **agent**

Officially-supported events (selection) :

| Phase | Events |
|-------|--------|
| Session | `SessionStart` · `SessionEnd` · `Setup` |
| Per turn | `UserPromptSubmit` · `UserPromptExpansion` · `Stop` · `StopFailure` |
| Per tool call | `PreToolUse` · `PostToolUse` · `PostToolUseFailure` · `PostToolBatch` · `PermissionRequest` · `PermissionDenied` |
| Subagents | `SubagentStart` · `SubagentStop` · `TaskCreated` · `TaskCompleted` · `TeammateIdle` |
| Memory / Config | `InstructionsLoaded` · `ConfigChange` · `CwdChanged` · `FileChanged` |
| Compaction / Notif | `PreCompact` · `PostCompact` · `Notification` · `Elicitation` · `ElicitationResult` |
| Worktree | `WorktreeCreate` · `WorktreeRemove` |

All hooks use `"shell": "powershell"` + scripts in `.claude/hooks/scripts/*.ps1` — no bash/python3 dependency on Windows.

Doc → [`docs/hooks-et-environnement.md`](docs/hooks-et-environnement.md) · Scripts → [`.claude/hooks/scripts/README.md`](.claude/hooks/scripts/README.md)

</details>

<br />

## 🔌 Install Anywhere

<details>
<summary><strong>Claude Code</strong></summary>

<br />

| Scope | Command |
|-------|---------|
| Full install | `cp -r claude-saas-blueprint/.claude my-project/.claude && cp claude-saas-blueprint/{CLAUDE.md,AGENTS.md} my-project/` |
| Light mode | `cp claude-saas-blueprint/{CLAUDE.md,AGENTS.md} my-project/` |
| Temporary | `claude --add-dir /path/to/claude-saas-blueprint` |

</details>

<details>
<summary><strong>Cursor · VS Code Copilot · Windsurf · Cline · Aider</strong></summary>

<br />

Copy `AGENTS.md` to your project root — all tools auto-discover it.

For skill support, copy the `.claude/skills/` folder to your tool's convention:

| Tool | Instructions path |
|------|-------------------|
| Cursor | `.cursor/rules/` or `.cursorrules` |
| VS Code Copilot | `.github/copilot-instructions.md` |
| Windsurf | `.windsurfrules` |
| Cline | `.clinerules` |
| Aider | `aider --read AGENTS.md` |

> Follows the open [Agent Skills](https://agentskills.io/) standard.

</details>

<br />

## 📦 Tech Stack

| | |
|-|-|
| **Agent** | Claude Code (Opus 4.6 · Sonnet 4.6 · Haiku 4.5) |
| **Framework** | Next.js 15 · Remix · Nuxt · SvelteKit |
| **Language** | TypeScript 5.x — strict mode, zero `any` |
| **Database** | Supabase (Postgres + RLS) · Neon · Turso |
| **Auth** | RBAC · Session-based · HTTP-only cookies |
| **Deploy** | Vercel · Docker · Cloudflare |
| **Quality** | Zod validation · ESLint · Prettier · Socket.dev |
| **Orchestration** | MCP servers · Trigger.dev · Inngest |

<br />

## 🛠️ Scripts

```bash
python scripts/verify-workflow-integrity.py    # Validate skills, links, structure
python scripts/project_health.py               # Full health check (TS, lint, tests, security)
python scripts/pre_deploy_check.py             # 8 checks before deploy
python scripts/scan_secrets.py --staged-only   # Scan for leaked secrets
python scripts/supabase_rls_check.py           # Audit RLS policies
python scripts/memory-rotate.py --dry-run      # Archive old memory sections
```

<br />

## 🌐 Platforms

| Web | Mobile | Desktop | API | Monorepo |
|:---:|:------:|:-------:|:---:|:--------:|
| Next · Remix · Nuxt · SvelteKit | Expo · Flutter | Tauri · Electron | Hono · Fastify · FastAPI · Go | Turborepo · Nx |

Guides → [`platforms/`](platforms/)

<br />

## 📜 License

MIT — use, modify, and share freely. See [LICENSE](./LICENSE).

---

<div align="center">
<sub>Ship production SaaS faster — with the precision of a senior engineer and the memory of an AI that never forgets your conventions.</sub>
</div>
