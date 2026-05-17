# Conventions — Skills (Claude Code)

> Référence officielle : https://code.claude.com/docs/en/skills

## Norme

Les skills de ce dépôt suivent le standard officiel **Claude Code Skills** (basé sur [Agent Skills](https://agentskills.io/) avec extensions Claude Code) :

- Un dossier par skill : `.claude/skills/<nom-kebab>/`
- Fichier d'entrée obligatoire : **`SKILL.md`**
- En-tête **YAML** entre `---` avec au minimum `description` (recommandé fortement).

## Champs frontmatter officiels

Tous les champs sont **optionnels** sauf `description` qui est recommandé.

| Champ | Rôle |
|--------|------|
| `name` | Nom d'affichage. Si omis, utilise le nom du dossier. Lettres minuscules / chiffres / tirets uniquement (max 64 caractères). |
| `description` | **Recommandé.** Quoi + quand l'utiliser. Claude utilise ça pour décider d'auto-loader. Si omis, utilise le premier paragraphe du markdown. Tronqué à 1 536 caractères dans la liste. |
| `when_to_use` | Contexte additionnel pour quand invoquer (trigger phrases, exemples). Concaténé à `description` pour la liste. |
| `argument-hint` | Hint d'autocomplétion : `[issue-number]` ou `[filename] [format]`. |
| `arguments` | Arguments positionnels nommés (string ou liste YAML) pour substitution `$nom` dans le contenu. |
| `disable-model-invocation` | `true` empêche Claude de l'auto-loader. À utiliser pour les workflows qu'on veut **manuel only** (ex: `/deploy`, `/commit`). Aussi exclu du preload subagents. Défaut : `false`. |
| `user-invocable` | `false` cache du menu `/`. Pour le contexte background non-actionnable. Défaut : `true`. |
| `allowed-tools` | Tools que Claude peut utiliser sans demander permission quand le skill est actif (string ou liste). |
| `model` | Modèle override pour le tour courant (mêmes valeurs que `/model`, ou `inherit`). |
| `effort` | `low` / `medium` / `high` / `xhigh` / `max`. Override l'effort de session. |
| `context` | `fork` pour exécuter dans un subagent isolé. |
| `agent` | Type de subagent à utiliser quand `context: fork` (`Explore`, `Plan`, `general-purpose`, ou un agent custom). |
| `hooks` | Hooks scopés au lifecycle du skill. Même format que dans `settings.json`. |
| `paths` | Glob patterns d'activation conditionnelle (`src/api/**/*.ts`). String CSV ou liste YAML. |
| `shell` | `bash` (défaut) ou `powershell` pour les commandes inline `` !`...` `` et blocs `` ```! ``. PowerShell requiert `CLAUDE_CODE_USE_POWERSHELL_TOOL=1`. |

## Quand utiliser `disable-model-invocation: true`

| Situation | `disable-model-invocation` |
|-----------|---------------------------|
| Effets de bord multi-fichiers (génération, scaffolding, refactor) | `true` |
| Interactif avec `AskUserQuestion` | `true` |
| Workflow long avec étapes obligatoires | `true` |
| Action avec timing critique (deploy, commit, message slack) | `true` |
| Quick fix mono-fichier (`/fix`, `/oneshot`) | `false` |
| Read-only (audit, review, scan) | `false` |
| Reference content / knowledge | `false` |

## Substitutions disponibles dans le contenu

| Variable | Rôle |
|----------|------|
| `$ARGUMENTS` | Tous les arguments passés à l'invocation. |
| `$ARGUMENTS[N]` | Argument à l'index N (0-based). |
| `$N` | Raccourci pour `$ARGUMENTS[N]` (`$0`, `$1`...). |
| `$nom` | Argument nommé déclaré dans `arguments:` frontmatter. |
| `${CLAUDE_SESSION_ID}` | ID de la session courante. |
| `${CLAUDE_EFFORT}` | Niveau d'effort actif. |
| `${CLAUDE_SKILL_DIR}` | Dossier contenant `SKILL.md` (résolution correcte personal/project/plugin). |

## Injection dynamique de contexte

Les skills supportent l'exécution de commandes **avant** que Claude voie le contenu :

````markdown
## Current changes
!`git diff HEAD`

## Multi-line block
```!
node --version
npm --version
git status --short
```
````

La commande s'exécute, sa sortie remplace le placeholder. Claude reçoit le résultat préfabriqué.

## Skills bundled (built-in Claude Code)

Disponibles sans installation :

| Skill | Usage |
|-------|-------|
| `/batch` | Changements massifs parallèles sur plusieurs fichiers |
| `/loop` | Polling / boucle itérative avec condition d'arrêt |
| `/simplify` | Review par 3 agents parallèles (structure, lisibilité, perf) |
| `/debug` | Debugging systématique avec hypothèses |
| `/claude-api` | Appels à l'API Claude depuis le terminal |

## Invocation

- Commande slash = **`/` + nom du dossier** (ex. `/feature`, `/apex`).
- Live change detection : ajouter / modifier un skill prend effet **dans la session courante**, sans redémarrer.
- Auto-discovery dans les sous-répertoires (monorepo) : skills dans `packages/frontend/.claude/skills/` chargés à la demande.

## Limitations à connaître

- Le contenu d'un skill invoqué **reste dans le contexte tout le reste de la session** — chaque ligne coûte des tokens. Garder concis.
- `SKILL.md` cible **moins de 500 lignes**. Mettre les détails dans des fichiers de référence chargés à la demande.
- Le combo `description + when_to_use` est tronqué à **1 536 caractères** dans le listing initial. Mettre les keywords clés en premier.
- Pendant `/compact`, jusqu'à 25 000 tokens de skills invoqués sont conservés (5 000 par skill, du plus récent au plus ancien).

## Index

Voir `.claude/skills/README.md` pour la liste à jour.
