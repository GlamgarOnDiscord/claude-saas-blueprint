# Template: Variables d'environnement (.env.example)

## Usage
Copier ce fichier en `.env.example` à la racine du projet applicatif. Décommenter et remplir les variables nécessaires selon la stack.

## Fichier prêt-à-copier

```bash
# ─────────────────────────────────────────────────
# Core
# ─────────────────────────────────────────────────
NODE_ENV=development
PORT=3000
APP_URL=http://localhost:3000

# ─────────────────────────────────────────────────
# Database
# ─────────────────────────────────────────────────
DATABASE_URL=postgresql://user:password@localhost:5432/mydb
# DIRECT_URL=              # Prisma / Drizzle direct connection (si pooler)

# ─────────────────────────────────────────────────
# Auth
# ─────────────────────────────────────────────────
# AUTH_SECRET=              # Auth.js secret (openssl rand -base64 32)
# CLERK_SECRET_KEY=         # Si Clerk
# CLERK_PUBLISHABLE_KEY=    # Si Clerk (publique, ok côté client)

# ─────────────────────────────────────────────────
# Payments
# ─────────────────────────────────────────────────
# STRIPE_SECRET_KEY=
# STRIPE_WEBHOOK_SECRET=
# STRIPE_PUBLISHABLE_KEY=   # Publique, ok côté client

# ─────────────────────────────────────────────────
# Email
# ─────────────────────────────────────────────────
# RESEND_API_KEY=

# ─────────────────────────────────────────────────
# Storage (S3 / R2 / Supabase Storage)
# ─────────────────────────────────────────────────
# ASSETS_BUCKET=
# ASSETS_CDN_BASE_URL=
# S3_ACCESS_KEY_ID=
# S3_SECRET_ACCESS_KEY=
# S3_REGION=
# S3_ENDPOINT=              # Pour R2 / MinIO

# ─────────────────────────────────────────────────
# Média & IA (clés SERVEUR uniquement — jamais NEXT_PUBLIC_*)
# ─────────────────────────────────────────────────
# QUIVERAI_API_KEY=         # SVG (Quiver)
# GOOGLE_API_KEY=           # Images (Gemini / Nano Banana)
# ELEVENLABS_API_KEY=       # Audio / voix
# OPENAI_API_KEY=           # Si utilisé

# ─────────────────────────────────────────────────
# Monitoring
# ─────────────────────────────────────────────────
# SENTRY_DSN=
# POSTHOG_KEY=              # Publique, ok côté client
# POSTHOG_HOST=

# ─────────────────────────────────────────────────
# Redis (cache / queue)
# ─────────────────────────────────────────────────
# REDIS_URL=
```

## Règles
- **Jamais** de valeurs réelles dans `.env.example` — uniquement des placeholders.
- Les clés API de fournisseurs IA sont **serveur uniquement** — ne pas préfixer `NEXT_PUBLIC_`.
- Documenter chaque variable avec un commentaire si le nom n'est pas évident.
- Versionner `.env.example`, **jamais** `.env`.
