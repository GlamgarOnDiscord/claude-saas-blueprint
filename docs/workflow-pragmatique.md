# Workflow IA SaaS — version pragmatique (anti-overkill)

Ce dépôt peut servir de **cadre complet** ou de **noyau minimal** selon ton projet. L’objectif est d’éviter de tout charger en contexte à chaque session.

## Principes (alignés pratique 2025-2026)

1. **`CLAUDE.md` court et actionnable** — Stack, commandes (`build` / `test` / `lint`), structure des dossiers, décisions qui bloquent. Éviter le bruit générique : chaque ligne doit s’appliquer à *ce* repo.
2. **Règles et skills à la demande** — Charger `.claude/rules/*` seulement quand tu touches API, DB, auth, UI, etc. Idem pour les skills : une tâche = un ou deux skills max. Pour décider quoi ouvrir : **`/scope-task`** (progressive disclosure).
3. **Peu de MCP** — 0–2 serveurs MCP utiles (ex. doc à jour, DB), pas une collection « au cas où ».
4. **Mémoire utile** — `user-profile`, `session`, `stack` quand tu travailles sérieusement ; le reste au fil de l’eau.
5. **Contrats avant le code** — Pour une feature non triviale : petit plan (quoi / pourquoi / comment) + critères de fin, puis implémentation (proche EPCT / APEX).

## Trois niveaux (choisis un)

| Niveau | Quand | Tu utilises |
|--------|--------|-------------|
| **Essentiel** | Script, POC, repo déjà simple | Racine : `CLAUDE.md` + (si besoin) une règle ciblée. Pas d’obligation de lire toute `.claude/`. |
| **Standard** | SaaS ou équipe en croissance | `CLAUDE.md` + mémoire (`stack`, `session`) + skills ponctuels : `/fix`, `/quality`, `/feature`, `/onboard` selon le besoin. |
| **Complet** | Plusieurs produits, conventions strictes | Tout le dossier `.claude/` (skills, agents, roadmap, ADR) pour homogénéiser. |

**Règle d’or** : si tu n’as pas ouvert un fichier de skill depuis une semaine, tu n’en as probablement pas besoin dans le flux par défaut.

## Optionnel (uniquement si tu le veux)

| Besoin | Doc / skill |
|--------|-------------|
| **Revue PR IA** (CodeRabbit) | [`integrations/coderabbit-optional.md`](./integrations/coderabbit-optional.md) — guide opt-in, **pas de skill packagé**. |
| **Mise à jour profonde** d’une lib / API (changelogs, breaking changes, code propre) | [`processus-mise-a-jour-profonde.md`](./processus-mise-a-jour-profonde.md) · `/deep-update` |

## Correspondance avec les guides publics

- Hiérarchie `CLAUDE.md` / `.claude/CLAUDE.md` / `.claude/rules/` : garder le **projet** dans le root et le **détail** dans les sous-dossiers (évite la surcharge contextuelle).
- Qualité : des études et retours d’usage (dont guides type « structure CLAUDE.md après 1000+ sessions ») convergent vers **peu de lignes universelles** + **règles scopées**.

Références utiles (externes) :

- [The Ultimate Guide to CLAUDE.md — Buildcamp](https://www.buildcamp.io/guides/the-ultimate-guide-to-claudemd)
- [CLAUDE.md Structure — BSWEN](https://docs.bswen.com/blog/2026-03-10-how-to-structure-claude-md)
- [Claude Code — structure production (MCP, subagents) — Dev.to](https://dev.to/lizechengnet/how-to-structure-claude-code-for-production-mcp-servers-subagents-and-claudemd-2026-guide-4gjn)

**Recherche structurée (officiel + HumanLayer + MCP + arXiv)** : voir **[`recherche-sources-2026.md`](./recherche-sources-2026.md)** (table des liens, synthèse, alignement avec ce repo).

## Fichiers utiles dans ce repo

| Fichier | Rôle |
|---------|------|
| `CLAUDE.md` | Cerveau principal (identité, APEX, conventions SaaS). |
| `.claude/memory/user-profile.md` | Premier usage ou onboarding perso. |
| `.claude/rules/`, `.claude/skills/<nom>/SKILL.md` | **À ouvrir** quand la tâche correspond ; pas tout le dossier d’un coup. |
| `platforms/` | Quand tu initialises ou migres une stack précise. |
| `docs/adr/` | Décisions d’architecture à long terme. |
| `docs/integrations/` | Pipeline d’assets (images, SVG, vidéo, 3D) pour le SaaS. |
| `docs/processus-mise-a-jour-profonde.md` | Migration raisonnée après veille changelog (`/deep-update`). |

## Voir aussi

- [`hooks-et-environnement.md`](./hooks-et-environnement.md) — Bash, Windows, Prettier.  
- [`veille`](../.claude/memory/veille-2026-03.md) — Idées et outils (budget, MCP, loops).
