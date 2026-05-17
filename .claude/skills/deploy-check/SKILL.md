---
name: deploy-check
description: "Validation complète pré-déploiement. Supporte Vercel, Railway, Docker/VPS. Utilise les scripts Python du projet."
argument-hint: "- `env` : staging | production (défaut: staging)"
disable-model-invocation: true
---

## Arguments
- `env` : staging | production

## Étape 1 — Pre-deploy checks (script unifié)

```bash
python scripts/pre_deploy_check.py --env [staging|production]
```

Couvre : TypeScript, lint, tests, secrets, `.env.example`, console.log, migrations, RLS.
**Bloquer si exit 1.**

## Étape 2 — Plateforme de déploiement

### Vercel (recommandé SaaS Next.js)
```bash
vercel --env staging      # Preview URL
vercel --prod             # Production
```
Variables requises dans Vercel : `DATABASE_URL` (pooler port 6543), `DIRECT_URL` (port 5432),
`NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`.

### Railway
```bash
railway up --environment staging
railway up --environment production
```

### Docker / VPS (Coolify, Dokku)
```bash
docker build -t app:$(git rev-parse --short HEAD) .
docker push [registry]/app:[tag]
# Puis trigger deploy via webhook ou CLI Coolify/Dokku
```

## Étape 3 — Migrations DB (si Supabase)

```bash
python scripts/supabase_migrate.py --diff          # Voir ce qui va être appliqué
python scripts/supabase_migrate.py --env [env]     # Appliquer
python scripts/supabase_rls_check.py               # Vérifier RLS
```

## Étape 4 — Post-deploy

1. Smoke test : `curl https://[domain]/api/health`
2. Logs plateforme — 0 erreur 500 dans les 2 premières minutes
3. Sentry — nouvelles erreurs ?
4. Mettre à jour `.claude/memory/session.md` avec la version déployée

## Rollback

**Vercel** : `vercel rollback [deployment-url]`
**Railway** : `railway rollback`
**Docker** : redéployer le tag précédent
**DB** : créer une nouvelle migration inverse (`python scripts/supabase_migrate.py --new rollback-[feature]`)
