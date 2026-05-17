---
name: perf
description: "Audit et optimisation des performances SaaS. Bottlenecks DB, bundle, Server Components, background jobs. Next.js + Supabase."
---

## Phase 1 — Identifier les bottlenecks

**Lancer d'abord :**
```bash
python scripts/project_health.py   # vue globale
```

**Web App (Next.js) :**
- Server Components vs Client Components inutiles (`"use client"` abusif ?)
- Re-renders inutiles (props instables, Context trop large)
- N+1 queries (boucle avec query DB à chaque itération)
- Images non optimisées (pas de `next/image`)
- Composants lourds non lazy-loadés (`dynamic(() => import(...))`)
- Bundle size : analyser `next build` output — alerter si JS client > 500KB
- Pas de `cache()` sur les Server Components qui refetch les mêmes données

**API + DB :**
- Index manquants sur FK et champs de recherche fréquents
- Endpoints sans pagination (retournent tout)
- Opérations lentes dans le handler (email, PDF, webhook) → doivent être async
- Connection pooling Supabase : utiliser le pooler (port 6543), pas direct

**Background jobs :**
- Emails, webhooks, exports PDF, traitements IA → ne JAMAIS bloquer le handler
- Solutions recommandées : **Trigger.dev v4** ou **Inngest** (voir `docs/integrations/ai-tools-2026.md`)
- Pattern : `POST /api/invoice` → créer job → return 202 → Trigger.dev exécute en fond

**Edge :**
- Endpoints légers (auth check, redirects) → Edge Runtime (`export const runtime = 'edge'`)
- DB géo-distribuée pour faible latence globale : **Turso** (SQLite edge) ou **Neon** (serverless Postgres)

## Phase 2 — Quick wins (par ordre d'impact)

1. **Index DB manquants** — impact immédiat, 0 code à changer
   ```sql
   CREATE INDEX ON public.invoices (organization_id, created_at DESC);
   ```
2. **Pagination** sur tous les endpoints de liste (`limit` + `cursor`)
3. **Lazy load** composants lourds (éditeurs, charts, maps)
4. **Cache React Query** : `staleTime: 5 * 60 * 1000` sur les queries stables
5. **next/image** pour toutes les images + formats WebP/AVIF
6. **Debounce** les inputs de recherche (300ms)
7. **Passer en async** les opérations lentes (email → Resend en background)

## Phase 3 — Optimisations avancées

- **Streaming + Suspense** : perceived performance sur les pages lentes
- **ISR** : contenu semi-statique avec `revalidate`
- **PgBouncer / Supabase pooler** : connection pooling DB (déjà intégré Supabase)
- **Trigger.dev** : background jobs pour tâches IA longues (génération, analyse)

## Output

Rapport avec :
- Bottlenecks identifiés par sévérité (CRITICAL / WARNING / INFO)
- Quick wins appliqués immédiatement
- Recommandations pour les optimisations avancées + estimation d'impact
