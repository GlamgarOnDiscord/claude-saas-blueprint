# Platform: API / Backend Service

## Stacks Recommandées (2026)

### Option A — Hono + Bun (Recommandé pour vitesse)
- **Framework**: Hono (ultraléger, edge-ready)
- **Runtime**: Bun ou Node.js 22+
- **Validation**: Zod
- **DB**: Drizzle ORM + PostgreSQL
- **Auth**: JWT custom ou Lucia Auth
- **Docs**: OpenAPI auto-générée
- **Deploy**: Cloudflare Workers, Vercel Edge, ou Docker

### Option B — Fastify + Node.js
- Pour APIs REST classiques avec écosystème mature

### Option C — FastAPI + Python
- Si l'utilisateur préfère Python ou besoin ML/AI

### Option D — Go + Chi/Fiber
- Pour performance maximale et concurrence

## Conventions API
- RESTful par défaut, GraphQL seulement si justifié
- Versioning via URL prefix (`/api/v1/`)
- Pagination cursor-based pour les listes volumineuses
- Rate limiting par tier (free/pro/enterprise)
- Idempotency keys pour les mutations critiques
- Webhook system pour les events async
- Health check endpoint (`GET /health`)

## Structure API Recommandée
```
src/
├── core/
│   ├── entities/
│   ├── usecases/
│   └── ports/
├── adapters/
│   ├── http/            # Routes + middleware
│   │   ├── routes/
│   │   ├── middleware/
│   │   └── validators/
│   ├── db/              # Repositories
│   ├── queue/           # Job queue (BullMQ, etc.)
│   ├── cache/           # Redis
│   └── email/           # Transactional email
├── shared/
│   ├── errors.ts        # Error types
│   ├── logger.ts        # Structured logging
│   └── config.ts        # Env config
└── index.ts             # Entry point
```

## Checklist API
- [ ] Health check endpoint
- [ ] Structured logging (JSON)
- [ ] Error handling middleware global
- [ ] Request ID tracking
- [ ] CORS configuré
- [ ] Rate limiting
- [ ] Input validation sur chaque endpoint
- [ ] Auth middleware
- [ ] OpenAPI / Swagger docs
- [ ] Graceful shutdown
- [ ] DB connection pooling
- [ ] Monitoring (uptime, latency)
