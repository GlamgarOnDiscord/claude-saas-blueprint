# Template: Port (Core Interface)

## Usage
Utilisé par `/schema-gen` pour créer l'interface du repository dans `core/ports/`.

## Structure TypeScript
```typescript
// core/ports/i-{name}-repo.ts
import type { {Name}, Create{Name}Input, Update{Name}Input } from '../entities/{name}';

export interface I{Name}Repo {
  findById(id: string, organizationId: string): Promise<{Name} | null>;
  findMany(organizationId: string, options?: {
    page?: number;
    limit?: number;
    orderBy?: string;
    order?: 'asc' | 'desc';
  }): Promise<{ data: {Name}[]; total: number }>;
  create(input: Create{Name}Input): Promise<{Name}>;
  update(id: string, organizationId: string, input: Update{Name}Input): Promise<{Name}>;
  softDelete(id: string, organizationId: string): Promise<void>;
}
```
