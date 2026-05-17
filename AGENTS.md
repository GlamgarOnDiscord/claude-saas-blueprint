# AGENTS.md — claude-saas-blueprint (Cross-Tool)

> **Source unique** des conventions communes à tous les outils IA (Claude Code, Cursor, Copilot, Windsurf, Cline, Aider…).
> Pour Claude Code, `CLAUDE.md` importe ce fichier et y ajoute uniquement les spécificités (skills, hooks, memory, MCP).

## Identity
Développeur SaaS full-stack senior. Code production-ready. Sécurité par défaut.

## Models (Mars 2026)
- **Opus 4.6** : tâches complexes, multi-agent, refactoring. 1M context (beta), 128k output.
- **Sonnet 4.6** : production, coût-efficace, approche Opus. Default recommandé.
- **Haiku 4.5** : sous-agents Explore, triage, haute fréquence.
- **Thinking** : `adaptive` par défaut (`budget_tokens` déprécié). Paramètre `effort`: `low | medium | high | max`.

## Architecture — Hexagonale
```
src/
├── core/           # Logique métier pure, ZERO import externe
│   ├── entities/   # Objets métier + validation Zod
│   ├── usecases/   # 1 fichier = 1 usecase
│   └── ports/      # Interfaces/contrats
├── adapters/       # Implémentations concrètes (db, api, auth, payments)
├── shared/         # Types partagés, utils, constantes
└── config/         # Configuration par environnement
```

## Conventions
- **Fichiers** : kebab-case. **Types** : PascalCase, `I` prefix interfaces.
- **Max 200 lignes/fichier** (composants UI : 150). Pas de `any`. Imports absolus `@/`.
- **Erreurs typées** toujours. Pas de `throw new Error()` nu.
- **Zod** au boundary (validation des entrées API). Pas de `Valibot` sauf décision projet explicite.
- **Réponse API** : `{ data, error, meta }`.

## Workflow APEX
1. **A — Analyze** : blast radius, lire types/interfaces. Si >5 fichiers → demander un plan.
2. **P — Plan** : 3 lignes. QUOI · POURQUOI · COMMENT.
3. **E — Execute** : diffs ciblés. Un commit = un changement logique. Subagents si parallélisable et indépendant.
4. **X — eXamine** : `tsc --noEmit`, tests blast radius, 0 secret, 0 `console.log`. **Fail-stop : 2 échecs consécutifs → arrêt.**

## SaaS Patterns
- **Multi-tenancy** : `organizationId` + RLS sur chaque table métier.
- **Auth** : authn ≠ authz. RBAC par défaut. Sessions DB préférées à JWT pour le web.
- **DB** : migrations versionnées. Soft delete (`deletedAt`). `createdAt` + `updatedAt` partout.
- **Sécurité** : rate limiting + CSP + HSTS sur les endpoints publics. CSRF sur les formulaires non-stateless.

## Quality Gates (avant commit)
- 0 erreur TS / lint
- Tests sur le blast radius
- 0 secret committé (scan obligatoire)
- 0 `console.log` en prod

## Skills & Sous-agents (terminologie)
- **Skills** = instructions réutilisables, standard [Agent Skills](https://agentskills.io/). Format `.claude/skills/<nom>/SKILL.md` avec frontmatter YAML.
- **Subagents** Claude Code = fichiers Markdown + YAML dans `~/.claude/agents/` ou `.claude/agents/` du projet (frontmatter `name`, `description`, `tools`, `model`). **Ce dépôt n'embarque pas de subagents** — uniquement des **guides** de pattern dans `.claude/guides/`.
- **Agent Teams** (expérimental Claude Code) : `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`.
- Routing modèle : Opus pense, Sonnet code, Haiku cherche.

## Références
- **Templates** : `templates/` (entity, port, usecase, api-route, env-example, ci-cd, subagent)
- **Platform guides** : `platforms/` (web-app, mobile-app, desktop-app, api-backend, monorepo)
- **Docs** : `docs/` (workflow pragmatique, skills conventions, hooks et environnement, intégrations)
- **Skills** : `.claude/skills/` (index `.claude/skills/README.md`)
- **Rules** : `.claude/rules/` (chargement contextuel par domaine)
- **Guides multi-agents** : `.claude/guides/` (orchestration, model-routing, debugging-techniques, etc.)
