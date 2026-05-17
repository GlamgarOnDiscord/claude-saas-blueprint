# Platform: Monorepo

## Quand Utiliser un Monorepo
- App web + app mobile partageant du code (core, types, validation)
- App web + API backend séparée
- SaaS multi-produits sous le même toit
- Design system + apps consommatrices

## Stacks Recommandées (2026)

### Option A — Turborepo + pnpm (Recommandé)
- **Monorepo tool**: Turborepo
- **Package manager**: pnpm (workspaces natifs)
- **Build**: Turbopack / tsup pour les packages
- **Versioning**: Changesets (si packages publics)

### Option B — Nx
- Pour les très gros projets avec graphe de dépendances complexe

## Structure Recommandée
```
monorepo/
├── apps/
│   ├── web/              # Next.js web app
│   ├── mobile/           # Expo React Native app
│   ├── api/              # API backend standalone
│   └── admin/            # Admin dashboard
├── packages/
│   ├── core/             # Logique métier partagée
│   │   ├── entities/
│   │   ├── usecases/
│   │   └── ports/
│   ├── ui/               # Composants UI partagés
│   ├── config-ts/        # Config TypeScript partagée
│   ├── config-eslint/    # Config ESLint partagée
│   └── validators/       # Schemas Zod partagés
├── turbo.json
├── pnpm-workspace.yaml
└── package.json
```

## Conventions Monorepo
- Chaque package a son propre `package.json` et `tsconfig.json`
- Les packages internes utilisent `"workspace:*"` pour les dépendances
- Le `core/` est IDENTIQUE à l'architecture hexagonale — il ne dépend de rien
- Les apps importent depuis `@monorepo/core`, `@monorepo/ui`, etc.
- CI/CD : Turborepo cache les builds, ne rebuild que ce qui a changé

## Scripts Racine
```json
{
  "scripts": {
    "dev": "turbo dev",
    "build": "turbo build",
    "test": "turbo test",
    "lint": "turbo lint",
    "typecheck": "turbo typecheck",
    "dev:web": "turbo dev --filter=web",
    "dev:mobile": "turbo dev --filter=mobile",
    "dev:api": "turbo dev --filter=api"
  }
}
```

## Checklist Monorepo
- [ ] pnpm-workspace.yaml configuré
- [ ] turbo.json avec pipelines (build, test, lint, typecheck)
- [ ] tsconfig base partagé dans packages/config-ts
- [ ] ESLint config partagée dans packages/config-eslint
- [ ] CI pipeline avec cache Turborepo
- [ ] Chaque package buildable indépendamment
- [ ] Imports cross-package fonctionnels
