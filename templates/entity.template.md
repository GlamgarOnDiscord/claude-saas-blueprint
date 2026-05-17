# Template: Entity (Core)

## Usage
Utilisé par `/schema-gen` et `/feature` pour créer une entité dans `core/entities/`.

## Structure TypeScript
```typescript
// core/entities/{name}.ts
import { z } from 'zod';

export const {Name}Schema = z.object({
  id: z.string().uuid(),
  organizationId: z.string().uuid(),
  // ... champs métier
  createdAt: z.date(),
  updatedAt: z.date(),
  deletedAt: z.date().nullable(),
});

export type {Name} = z.infer<typeof {Name}Schema>;
export type Create{Name}Input = Omit<{Name}, 'id' | 'createdAt' | 'updatedAt' | 'deletedAt'>;
export type Update{Name}Input = Partial<Omit<{Name}, 'id' | 'organizationId' | 'createdAt' | 'updatedAt' | 'deletedAt'>>;
```
