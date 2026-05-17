# Feature — Step 2: Plan

## Objectif
Créer un plan d'action détaillé AVANT d'écrire du code.

## Actions

### 1. Architecture de la Feature
Définir la structure en suivant l'architecture hexagonale :
```
1. Entity      → core/entities/{name}.ts
2. Validator   → shared/validators/{name}.ts
3. Port        → core/ports/i-{name}-repo.ts
4. Use Cases   → core/usecases/create-{name}.ts, list-{names}.ts, etc.
5. Repository  → adapters/db/{name}-repo.ts
6. API Routes  → adapters/api/{name}/route.ts
7. UI (si web) → components/features/{name}/ ou app/(dashboard)/{name}/
8. Tests       → __tests__/ à côté de chaque fichier
```

### 2. Plan d'Exécution
Écrire le plan étape par étape avec les fichiers exacts :
```markdown
## Plan: [Nom de la Feature]

### Étape 1 — Core (logique métier)
- [ ] Créer entity + validation Zod
- [ ] Créer port (interface repository)
- [ ] Créer usecase(s)

### Étape 2 — Adapters (infrastructure)
- [ ] Créer/modifier schema DB + migration
- [ ] Implémenter repository
- [ ] Créer routes API

### Étape 3 — UI (si applicable)
- [ ] Créer les composants
- [ ] Connecter au data fetching

### Étape 4 — Tests
- [ ] Tests unitaires usecases
- [ ] Tests intégration API
```

### 3. Validation du Plan
- Si blast radius > 5 fichiers → utiliser EnterPlanMode pour approbation utilisateur
- Si blast radius <= 5 fichiers → continuer directement
- Vérifier que le plan respecte les rules actives (de step-1)

## Transition
→ Passer à `step-3-execute.md`
