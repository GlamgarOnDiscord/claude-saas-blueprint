# Template: API Route (Adapter)

## Usage
Utilisé par `/api-gen` pour créer des endpoints dans `adapters/api/`.

## Structure Next.js App Router
```typescript
// adapters/api/{name}/route.ts (ou app/api/{name}/route.ts)
import { NextRequest, NextResponse } from 'next/server';
import { {Name}Schema } from '@/core/entities/{name}';
import { create{Name} } from '@/core/usecases/create-{name}';
import { {name}Repo } from '@/adapters/db/{name}-repo';
import { getSession } from '@/adapters/auth/session';

export async function POST(req: NextRequest) {
  const session = await getSession();
  if (!session) {
    return NextResponse.json({ error: 'Unauthorized', code: 'AUTH_REQUIRED' }, { status: 401 });
  }

  const body = await req.json();
  const parsed = {Name}Schema.omit({ id: true, createdAt: true, updatedAt: true, deletedAt: true }).safeParse(body);

  if (!parsed.success) {
    return NextResponse.json({ error: 'Validation failed', details: parsed.error.flatten() }, { status: 400 });
  }

  const result = await create{Name}(
    { {name}Repo },
    { ...parsed.data, organizationId: session.organizationId, userId: session.userId }
  );

  if (!result.success) {
    return NextResponse.json({ error: result.error, code: result.code }, { status: 422 });
  }

  return NextResponse.json({ data: result.data }, { status: 201 });
}
```

## Pattern de Réponse Standard
```typescript
// Succès
{ data: T, meta?: { page, limit, total } }

// Erreur
{ error: string, code: string, details?: unknown }
```
