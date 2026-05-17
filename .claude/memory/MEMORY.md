# claude-saas-blueprint Memory Index

## Purpose
Infrastructure de contrôle IA pour le développement SaaS. Pas de code métier — uniquement config, skills, templates, et orchestration d'agents.

**Ne pas tout charger** : voir `docs/workflow-pragmatique.md` (niveaux Essentiel / Standard / Complet).

## Files
- `stack.md` — Stack technique du projet en cours
- `domains.md` — Domaines métier et features implémentés
- `patterns.md` — Patterns de code découverts et réutilisables
- `session.md` — État de la dernière session de travail
- `errors.md` — Erreurs récurrentes et solutions connues
- `decisions.md` — Décisions techniques prises
- `veille-2026-03.md` — Veille concurrentielle mars 2026

## Project Status
- Phase: `infrastructure` — Configuration de l'outillage IA
- Stack: non définie (template multi-stack)
- CLAUDE.md: ~70 lignes (overlay sur AGENTS.md, conventions communes là-bas)
- Skills: **31** (`*/SKILL.md`) + 4 étapes `feature/steps/`
- Rules: **9** (api-routes, db-schema, auth, ui-components, tests, config, media-apis, security, _learned + README)
- Multi-agent guides: **7** dans `.claude/guides/` (orchestration, model-routing, context-management, debugging-techniques, testing-strategy, prompt-patterns, visual-context)
- Subagents custom: **0** (`.claude/agents/` réservé pour ajouts futurs)
- Platforms: 5 (web-app, mobile-app, desktop-app, api-backend, monorepo)
- Hooks: PowerShell-first (Windows natif), scripts dans `.claude/hooks/scripts/`
