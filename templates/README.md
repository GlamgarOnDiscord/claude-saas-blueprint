# Templates

Templates de fichiers à copier-coller pour démarrer rapidement, alignés sur l'architecture hexagonale et les conventions définies dans `AGENTS.md`.

## Architecture hexagonale

| Template | Rôle | Cible |
|----------|------|-------|
| `entity.template.md` | Entité métier avec validation Zod | `src/core/entities/` |
| `port.template.md` | Interface (contrat) entre core et adapter | `src/core/ports/` |
| `usecase.template.md` | Cas d'usage isolé, 1 fichier = 1 usecase | `src/core/usecases/` |
| `api-route.template.md` | Route API standardisée (Next.js / Hono / FastAPI) | `src/adapters/api/` ou `app/api/` |
| `env-example.template.md` | Variables d'environnement type pour `.env.example` | racine |

## CI/CD

| Template | Rôle |
|----------|------|
| `ci-cd/github-actions.md` | Workflows GitHub Actions (build, test, lint, deploy) |
| `ci-cd/git-workflow.md` | Conventions git (branches, commits, PRs) |

## Subagents

| Template | Rôle |
|----------|------|
| `subagent.template.md` | Subagent custom Claude Code (frontmatter YAML — déposer dans `.claude/agents/`) |

## Usage

```bash
# Copier un template dans ton projet
cp templates/entity.template.md src/core/entities/invoice.ts

# Puis adapter selon le contexte (nom, champs, validation)
```

Les templates sont volontairement **génériques** — ils s'adaptent à n'importe quelle stack respectant les conventions du dépôt (`AGENTS.md`).
