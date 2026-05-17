---
name: env-setup
description: "Configure l'environnement de développement pour un SaaS Next.js + Supabase + Vercel : outils CLI, variables d'env, RTK, vérifications."
---

## Instructions

### 1. Vérification des outils CLI requis

Vérifier que ces outils sont installés, sinon donner la commande d'installation :

| Outil | Vérification | Install |
|-------|-------------|---------|
| Node.js LTS | `node -v` ≥ 20 | https://nodejs.org |
| pnpm | `pnpm -v` | `npm i -g pnpm` |
| Supabase CLI | `supabase -v` | `brew install supabase/tap/supabase-cli` |
| Vercel CLI | `vercel -v` | `pnpm i -g vercel` |
| Git | `git -v` | — |
| RTK (token optimizer) | `rtk --version` | `brew install rtk-ai/tap/rtk && rtk init --global` |
| Python 3.9+ | `python --version` | https://python.org |

### 2. Variables d'environnement

Créer `.env.local` à partir de `.env.example`.
Si `.env.example` n'existe pas, le générer avec ces variables minimales pour un SaaS Supabase :

```bash
# App
NEXT_PUBLIC_APP_URL=http://localhost:3000

# Supabase
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=
DATABASE_URL=          # pooler port 6543
DIRECT_URL=            # direct port 5432

# Auth (si Better Auth ou NextAuth)
AUTH_SECRET=           # openssl rand -base64 32

# Paiements (si Stripe)
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=

# Emails (si Resend)
RESEND_API_KEY=

# Monitoring
SENTRY_DSN=
NEXT_PUBLIC_POSTHOG_KEY=
```

Vérifier que `.env*` est bien dans `.gitignore`.

### 3. Configuration Git

```bash
git config user.name   # vérifier configuré
git config user.email  # vérifier configuré
git config core.autocrlf false  # Windows : éviter les conflits CRLF
```

### 4. Supabase local

```bash
supabase start         # Démarrer la DB locale
supabase status        # Vérifier Studio URL + anon key locale
```

### 5. Vérification finale

```bash
python scripts/project_health.py   # Santé globale
python scripts/rtk_setup.py --check  # RTK actif ?
pnpm install && pnpm dev              # App démarre ?
```

### 6. RTK — si non installé
RTK réduit les tokens Claude Code de 60-90%. Installer une fois globalement :
```bash
brew install rtk-ai/tap/rtk && rtk init --global
# Windows : winget install rtk-ai.rtk
```
Doc : `docs/integrations/rtk-token-optimizer.md`
