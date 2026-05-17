# Skills — claude-saas-blueprint

Standard [Agent Skills](https://agentskills.io/). Structure : **`<nom>/SKILL.md`**. Invocation : **`/<nom>`**.
**31 skills** au total dans ce dépôt.

## Workflow & contexte

| Commande | Rôle |
|----------|------|
| `/session-start` | First contact — lire memory, router (onboard, saas-init), interview profil. |
| `/apex` | Cadre Analyze → Plan → Execute → Examine. |
| `/scope-task` | Quelles rules/skills/docs ouvrir pour **une** tâche (anti-surcharge contexte). |

## Lifecycle

| `/onboard` | `/saas-init` | `/env-setup` |

## Build

| `/oneshot` | `/fix` | `/feature` (multi-step) | `/refactor` |
| `/api-gen` | `/schema-gen` | `/ui` (gen·premium·landing) | `/migrate` |
| `/variations` | `/fork` | `/brainstorm` | `/deps` |

**Feature** : étapes dans `feature/steps/` (`step-1-explore` → `step-4-verify`).

## Domains

| `/stripe` | Checkout · Subscriptions · Webhooks · Customer Portal — best practices officielles. |
| `/e2e-tests` | Playwright — setup, Page Object Model, auth state, CI GitHub Actions. |
| `/assets-pipeline` | SVG (Quiver), images (Gemini), Remotion, scroll 3D. |

## Product

| `/prd` (brainstorm → generate → tasks → exec) |

## Qualité

| `/quality` | `/review` | `/debug` | `/perf` | `/docs-gen` |
| `/deploy-check` | `/ui-audit` (read-only WCAG/Nielsen/anti-slop) |

## Optionnel

| `/deep-update` | Mise à jour profonde : changelog officiel → migration clean. |
| `/meta-prompt` | Créer/améliorer un skill, une rule, un hook. |

## Bundled (Claude Code)

Skills intégrés au CLI, utilisables sans installation :

| `/batch` | `/loop` | `/simplify` | `/debug` | `/claude-api` |

> Voir `docs/skills-conventions.md` pour le format des skills custom.
