---
name: docs-gen
description: "Génère la documentation du projet : API docs, README, architecture. Utilise les scripts Python et l'analyse du code réel."
---

## Modes

### `/docs-gen api` — Documentation API

1. Scanner les routes : `Grep "export.*async function (GET|POST|PUT|DELETE|PATCH)" app/api/`
2. Pour chaque route, lire le fichier et extraire : méthode, auth requise, body Zod schema, réponses
3. Format de chaque endpoint :
   ```markdown
   ### POST /api/invoices
   **Auth** : Requis — `session.user.organizationId`
   **Body** : `{ amount: number, clientId: string }` (Zod schema: `CreateInvoiceSchema`)
   **201** : `{ data: Invoice }`
   **400** : `{ error: string, details: ZodError[] }`
   **401** : `{ error: "Unauthorized" }`
   **Rate limit** : 10 req/min
   ```
4. Écrire dans `docs/api.md`

### `/docs-gen readme` — README du projet

1. Lire `.claude/memory/stack.md` + `project-scan.md` + `package.json`
2. Lire la structure réelle avec Glob
3. Générer un README avec :
   - Description + stack (versions réelles du lockfile)
   - Prérequis (Node, pnpm, Supabase CLI, Vercel CLI)
   - Setup en 5 commandes : clone → install → `.env.local` → `supabase start` → `pnpm dev`
   - Scripts disponibles (depuis `package.json`)
   - Architecture hexagonale (`src/core/`, `src/adapters/`, etc.)
   - Commandes Python utiles (`scripts/README.md`)

### `/docs-gen architecture` — Diagramme d'architecture

1. Scanner la structure réelle avec Glob
2. Générer un diagramme Mermaid des flux principaux :
   - Auth flow (login → session → middleware → route)
   - Data flow (request → Zod → usecase → port → adapter → DB)
   - Multi-tenancy flow (`organizationId` dans chaque query)
3. Documenter les choix techniques depuis `.claude/memory/decisions.md` et `docs/adr/`
4. Écrire dans `docs/architecture.md`

### `/docs-gen schema` — Documentation DB

1. Lire les fichiers de migration `supabase/migrations/*.sql`
2. Extraire toutes les tables, colonnes, FK, index
3. Générer un diagramme ERD en Mermaid
4. Documenter les policies RLS pour chaque table
5. Écrire dans `docs/db-schema.md`

### `/docs-gen onboarding` — Guide développeur

Générer `docs/ONBOARDING.md` step-by-step :
- Prérequis + setup env (pointer vers `/env-setup`)
- Architecture expliquée (hexagonale : core vs adapters)
- Conventions (kebab-case, types, erreurs typées)
- Workflow de contribution (branch → APEX → PR → deploy)
- Commandes du quotidien : `project_health.py`, `supabase_migrate.py`, etc.
