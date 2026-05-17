# Dossier `.claude/` — claude-saas-blueprint

| Zone | Rôle |
|------|------|
| `skills/` | Un dossier par skill : `<nom>/SKILL.md` — voir `skills/README.md` et `docs/skills-conventions.md`. |
| `rules/` | Micro-règles **par domaine** (API, DB, auth…) — chargées selon les fichiers touchés. |
| `guides/` | Guides multi-agents (orchestration, model routing, debug, tests). Consultés à la demande. |
| `agents/` | **Réservé** aux subagents custom (frontmatter YAML). Vide par défaut. |
| `memory/` | État persistant (profil, session, stack, roadmap). |
| `hooks/scripts/` | Scripts PowerShell des hooks branchés dans `settings.json`. |
| `mcp/` | Config MCP optionnelle. |
| `settings.json` | Permissions + hooks actifs (PowerShell-first). |

**Réduire l'overkill** : lire `../docs/workflow-pragmatique.md` avant d'ouvrir tous les skills.

**Intégrations (assets)** : `../docs/integrations/assets-pipeline.md` · skill `/assets-pipeline`
**Optionnel** : CodeRabbit → `../docs/integrations/coderabbit-optional.md` (skill non packagé — voir le doc) · deep update → `../docs/processus-mise-a-jour-profonde.md` · `/deep-update`
