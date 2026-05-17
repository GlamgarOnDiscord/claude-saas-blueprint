---
name: saas-init
description: "Bootstrap complet d'un projet SaaS from scratch. Système de Q/R interactif pour configurer chaque aspect."
disable-model-invocation: true
---

## Instructions

### Phase 0 — Interview Projet (Q/R obligatoire)
Utiliser AskUserQuestion pour chaque question. Ne RIEN supposer.

**Question 1 — Type de projet :**
- SaaS B2B (Recommandé)
- SaaS B2C
- Marketplace
- API / Backend only

**Question 2 — Framework :**
- Next.js 15 (Recommandé)
- Remix
- Nuxt 4
- SvelteKit
- FastAPI + React/Vue

**Question 3 — Base de données :**
- PostgreSQL + Drizzle (Recommandé)
- PostgreSQL + Prisma
- Supabase (inclut auth + storage)
- MongoDB + Mongoose

**Question 4 — Auth :**
- Auth.js v5 (Recommandé)
- Clerk (rapide mais payant)
- Supabase Auth
- Better Auth
- Custom (JWT + sessions DB)

**Question 5 — Paiements :**
- Stripe (Recommandé)
- Lemonsqueezy (simple, Merchant of Record)
- Pas encore

**Question 6 — UI :**
- shadcn/ui + Tailwind (Recommandé)
- Radix + Tailwind
- Mantine
- Material UI

**Question 7 — Déploiement :**
- Vercel (Recommandé)
- Railway
- Docker + VPS (Coolify/Dokku)
- AWS (ECS/Lambda)

**Question 8 — Package Manager :**
- pnpm (Recommandé)
- bun
- npm
- yarn

**Question 9 — Extras :** (multiSelect)
- Email transactionnel (Resend)
- File upload (UploadThing / S3)
- Real-time (WebSockets / SSE)
- Background jobs (Inngest / BullMQ)
- Analytics (PostHog / Plausible)
- Monitoring (Sentry)
- AI features (Vercel AI SDK)

**Question 10 — MCP Servers :** (multiSelect)
- Context7 — Docs à jour (Recommandé)
- Playwright — E2E testing
- Sequential Thinking — Raisonnement structuré
- Aucun pour l'instant

### Phase 1 — Scaffolding
1. Initialiser avec le CLI officiel du framework choisi
2. Créer la structure hexagonale :
   ```
   src/core/entities/  src/core/usecases/  src/core/ports/
   src/adapters/db/    src/adapters/api/   src/adapters/auth/
   src/shared/         src/config/
   ```
3. Configurer imports absolus (`@/`), TypeScript strict, ESLint, Prettier
4. Créer `.env.example` avec toutes les variables
5. Initialiser git + `.gitignore`
6. Installer les dépendances extras choisies (Q9)

### Phase 2 — Fondations SaaS
1. Schema DB de base :
   - `users` (id UUID v7, email, name, role, avatarUrl, createdAt, updatedAt, deletedAt)
   - `organizations` (id, name, slug unique, plan, createdAt, updatedAt, deletedAt)
   - `memberships` (userId, organizationId, role enum)
2. Provider auth choisi + middleware protection
3. Logger structuré (pino)
4. Pattern réponse API : `{ data, error, meta }`
5. Error types de base : `NotFoundError`, `UnauthorizedError`, `ValidationError`

### Phase 3 — DX Setup
1. Scripts : `dev`, `build`, `test`, `lint`, `db:push`, `db:studio`, `db:seed`
2. Configurer vitest avec coverage
3. Tests de base : health check, auth flow
4. Seed de dev avec données de test

### Phase 4 — Finalisation
1. Installer MCPs choisis (Q10) dans `.claude/mcp/config.json`
2. Sauver stack dans `.claude/memory/stack.md`
3. Mettre à jour `.claude/memory/session.md`
4. Créer ADR 0001 documentant les choix techniques
5. Afficher récap : stack, structure, prochaines étapes

### Post-Init — Suggestions
Proposer à l'utilisateur :
- "Voulez-vous que je génère une landing page ? → `/ui landing`"
- "Voulez-vous configurer le CI/CD ? → `/deploy-check`"
- "Voulez-vous ajouter une feature ? → `/feature [description]`"
- "Voulez-vous un PRD complet ? → `/prd brainstorm`"
