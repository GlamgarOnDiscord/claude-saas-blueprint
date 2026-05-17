# Template: Git Workflow

## Trunk-Based (Recommandé pour solo/petite équipe)
```
main ──●──●──●──●──●──●──
       │        │
       └─feat─┘  (courte, < 1 jour)
```
- Commit direct sur main pour les petits changements
- Feature branches courtes (< 1 jour) pour les features
- Feature flags pour les features incomplètes en prod
- Tags pour les releases : `v1.0.0`, `v1.1.0`

## GitHub Flow (Recommandé pour équipes)
```
main ──●──────●──────●──
       │      ↑      │
       └─feat─┘      └─fix─┘
         PR            PR
```
- Toujours via PR
- Review requise
- CI doit passer avant merge
- Squash merge par défaut

## Conventions de Commit
```
type(scope): description courte

Types: feat, fix, refactor, test, docs, chore, perf, ci
Scope: optionnel, nom du domaine/module

Exemples:
feat(invoices): add PDF export
fix(auth): handle expired refresh tokens
refactor(db): migrate from Prisma to Drizzle
```

## Conventions de Branch
```
feat/invoice-pdf-export
fix/auth-token-refresh
refactor/db-migration
```
