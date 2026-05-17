# Conventions — Skills (Claude Code / Agent Skills)

## Norme

Les skills de ce dépôt suivent le standard **[Agent Skills](https://agentskills.io/)** tel qu'implémenté par **[Claude Code](https://code.claude.com/docs/en/skills)** :

- Un dossier par skill : `.claude/skills/<nom-kebab>/`
- Fichier d'entrée obligatoire : **`SKILL.md`**
- En-tête **YAML** (`---`) avec au minimum une **`description`** claire (pour l'auto-sélection par le modèle).

## Quand utiliser `disable-model-invocation: true`

Règle simple :

| Skill a… | `disable-model-invocation` |
|----------|---------------------------|
| **Effets de bord multi-fichiers** (génération, scaffolding, refactor) | `true` |
| **Interactif** avec AskUserQuestion / interview | `true` |
| **Workflow long** avec étapes obligatoires | `true` |
| Quick fix mono-fichier (`/fix`, `/oneshot`) | `false` (laisser libre) |
| Read-only (audit, review, scan) | `false` (laisser libre) |

Le but : ne pas auto-déclencher un skill qui crée 10 fichiers à la moindre mention dans le prompt utilisateur.

## Champs frontmatter

| Champ | Rôle |
|--------|------|
| `name` | Identifiant ; sinon = nom du dossier. |
| `description` | **Recommandé** — quoi + **quand** l'utiliser (1–2 phrases). |
| `argument-hint` | Aide à l'autocomplétion `/skill [args]`. |
| `disable-model-invocation: true` | Le skill **ne** se déclenche **pas** seul — réservé à l'invocation `/…` (workflows lourds, bootstrap, boucles). |
| `context` | Mode d'exécution : `fork` (worktree isolé), `inline` (défaut). |
| `agent` | Agent spécifique à utiliser (ex. `explore`, `code`). |
| `paths` | Glob patterns pour activation conditionnelle (ex. `src/api/**/*.ts`). |
| `effort` | Effort du modèle : `low`, `medium`, `high`, `max`. |
| `shell` | Shell pour les commandes : `bash` (défaut), `powershell`, `sh`. |
| `hooks` | Hooks spécifiques au skill (mêmes types que les hooks globaux). |
| `isolation` | `worktree` pour exécution dans un worktree git isolé. |

## Substitutions

Dans le contenu du SKILL.md, les variables suivantes sont remplacées automatiquement :

- `$ARGUMENTS` — les arguments passés après la commande slash (ex. `/feature $ARGUMENTS`)
- `$SKILL_DIR` — chemin absolu du dossier du skill
- `$WORKSPACE` — chemin absolu du workspace

## Skills bundled (built-in)

Claude Code inclut des skills intégrés utilisables sans installation :

| Skill | Usage |
|-------|-------|
| `/batch` | Changements massifs parallèles sur plusieurs fichiers |
| `/loop` | Polling/boucle itérative avec condition d'arrêt |
| `/simplify` | Review par 3 agents parallèles (structure, lisibilité, perf) |
| `/debug` | Debugging systématique avec hypothèses |
| `/claude-api` | Appels à l'API Claude depuis le terminal |

## Invocation

- Commande slash = **`/` + nom du dossier** (ex. `/feature`, `/apex`).
- Les anciens fichiers plats `.claude/skills/foo.md` ont été **migrés** vers `foo/SKILL.md`.

## Scripts

- `scripts/migrate-skills-to-agent-standard.py` — migration one-shot (conservé pour référence).

## Index

Voir `.claude/skills/README.md` pour la liste à jour.
