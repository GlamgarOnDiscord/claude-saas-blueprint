# CLAUDE.md — claude-saas-blueprint (Claude Code overlay)

> Conventions communes (architecture, workflow APEX, SaaS patterns, models) → **`@AGENTS.md`** (source unique).
> Ce fichier ne contient que les **spécificités Claude Code** (skills, hooks, memory, MCP, routing).

## [Usage levels]
- **Essentiel** : `AGENTS.md` + `CLAUDE.md` + `.claude/memory/stack.md` + `.claude/memory/session.md`. Ne pas charger les skills.
- **Standard** : + skills ciblés selon tâche (`/fix` `/feature` `/quality` `/deploy-check`)
- **Complet** : tout `.claude/` — équipe / multi-produits.
**Guide** : `docs/workflow-pragmatique.md`

## [First Contact Protocol]
1. Lire `~/.claude/projects/<project>/memory/MEMORY.md` (auto-memory) puis ce fichier.
2. Si profil utilisateur vide → `/session-start` (interview intégrée).
3. Si projet inconnu → `/onboard`.
4. Si dépôt vide → `/saas-init`.

## [Contextual Rules]
Charger la rule **avant** modification → `.claude/rules/`
- `api-routes` · `db-schema` · `auth` · `ui-components` · `tests` · `config` · `media-apis`
- **`security`** — obligatoire sur tout endpoint public, middleware, deploy
- Rules avec `paths:` frontmatter → chargement conditionnel (`src/api/**/*.ts`, etc.)
- Erreur découverte → ajouter dans `_learned.md`.

## [Skills] — Slash commands
- **Build** : `/feature` `/fix` `/oneshot` `/refactor` `/debug`
- **Quality** : `/quality` `/review` `/perf` `/deploy-check`
- **Generate** : `/api-gen` `/schema-gen` `/ui` (gen | premium | landing) `/docs-gen`
- **Explore** : `/onboard` `/brainstorm` `/scope-task` `/fork` `/variations`
- **Product** : `/prd` (brainstorm → generate → tasks → exec)
- **Lifecycle** : `/session-start` `/saas-init` `/env-setup` `/deps`
- **Domains** : `/stripe` `/e2e-tests` `/migrate` `/assets-pipeline`
- **Audit UI** : `/ui-audit`
- **Bundled** Claude Code : `/batch` `/loop` `/simplify` `/debug` `/claude-api`
- **Meta** : `/meta-prompt` (créer/améliorer skills, rules, hooks) · `/deep-update`
Index complet → `.claude/skills/README.md` · Conventions → `docs/skills-conventions.md`

## [Subagents & Agent Teams]
- **Subagents Claude Code intégrés** : `Explore`, `Plan`, `general-purpose`, `websearch`, `clean-code-generator`, `unit-testing:test-automator`, `unit-testing:debugger`.
- **Subagents custom** : `.claude/agents/` (réservé — voir `.claude/agents/README.md`). Ce dépôt n'en embarque pas par défaut.
- **Guides multi-agents** : `.claude/guides/` (orchestration, model routing, debugging, etc.) — consultés à la demande.
- **Agent Teams** (expérimental) : `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`.
- Max 4 agents parallèles. Routing : Opus pense, Sonnet code, Haiku cherche → `.claude/guides/model-routing.md`.
- Effort : `low` triage · `medium` Sonnet courant · `high` défaut · `max` Opus.
- Escalade : 2 tentatives échouées → demander à l'utilisateur.

## [Hooks de sécurité]
Config : `.claude/settings.json` → champ `hooks` (4 types : command, http, prompt, agent ; 21 événements lifecycle).
- **PreBash** : bloque `rm -rf /`, `DROP DATABASE`, `git push -f origin main`, etc.
- **PreEdit/PreWrite** : bloque édition de `.env`, credentials, secrets.
- **PostEdit/PostWrite** : Prettier auto sur `.ts`/`.tsx`/`.js`/`.jsx` (best-effort).
- **SessionStart (compact)** : recharge le contexte projet après compaction.
- **Windows** : tous les hooks utilisent `"shell": "powershell"` + scripts dans `.claude/hooks/scripts/`.
Doc → `docs/hooks-et-environnement.md`

## [Auto Memory]
- Notes auto dans `~/.claude/projects/<project>/memory/`. Index = `MEMORY.md` (200 premières lignes chargées auto).
- Toggle via `/memory` ou `autoMemoryEnabled: false`.
- `CLAUDE.md` survit à `/compact` (relu depuis le disque).
- Memory locale projet : `.claude/memory/` (`stack`, `session`, `domains`, `patterns`, `errors`, `decisions`).

## [MCP Servers]
**Aucun MCP installé par défaut.** Recommandés (max 2) : Context7 (docs à jour) + Supabase MCP.
Config : `.claude/mcp/config.json` ou `.vscode/mcp.json`. Doc : `docs/integrations/`.

## [Scripts Python — préférer aux commandes longues]
- `scripts/project_health.py` — santé globale (TS, lint, tests, sécurité)
- `scripts/pre_deploy_check.py --env [staging|production]` — 8 checks avant deploy
- `scripts/scan_secrets.py --staged-only` — scan secrets/clés API (à lancer avant chaque commit)
- `scripts/supabase_migrate.py` · `scripts/supabase_rls_check.py`
- `scripts/verify-workflow-integrity.py` — valide skills, liens, structure
Doc complète → `scripts/README.md`

## [Quality Gates Claude Code]
Avant commit : `python scripts/scan_secrets.py --staged-only` + 0 erreur TS/lint + 0 `console.log`.
Avant deploy : `python scripts/pre_deploy_check.py --env [staging|production]`.

## [Références]
- Workflow pragmatique → `docs/workflow-pragmatique.md`
- Outils 2026 → `docs/integrations/ai-tools-2026.md`
- Pipeline assets → `docs/integrations/assets-pipeline.md`
- Templates → `templates/` · Platform guides → `platforms/`
