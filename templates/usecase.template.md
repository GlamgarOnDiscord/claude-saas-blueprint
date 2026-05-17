# Template: Use Case (Core)

## Usage
Utilisé par `/feature` et `/api-gen` pour créer un cas d'utilisation dans `core/usecases/`.

## Structure TypeScript
```typescript
// core/usecases/{action}-{name}.ts
import type { I{Name}Repo } from '../ports/i-{name}-repo';
import type { {Name}, Create{Name}Input } from '../entities/{name}';

interface {Action}{Name}Deps {
  {name}Repo: I{Name}Repo;
}

interface {Action}{Name}Input {
  organizationId: string;
  userId: string;
  // ... input spécifique à l'action
}

type {Action}{Name}Result =
  | { success: true; data: {Name} }
  | { success: false; error: string; code: string };

export async function {action}{Name}(
  deps: {Action}{Name}Deps,
  input: {Action}{Name}Input
): Promise<{Action}{Name}Result> {
  // 1. Validation métier
  // 2. Exécution
  // 3. Retour typé
}
```

## Règles
- JAMAIS d'import depuis `adapters/`
- Injection de dépendances via le paramètre `deps`
- Retour typé avec union discriminée (success/error)
- Un fichier = un use case
