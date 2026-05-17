# Rules: Security — obligatoire sur tout endpoint public

## Obligatoire
- Headers HTTP de sécurité sur TOUTES les réponses : `Content-Security-Policy`, `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Strict-Transport-Security`
- Rate limiting sur TOUS les endpoints publics — `@upstash/ratelimit` + Vercel KV (ex: 10 req/10s par IP)
- Validation Zod AVANT tout traitement — jamais `req.body` brut (redondant avec api-routes.md, rappel global ici)
- Sanitisation HTML si `dangerouslySetInnerHTML` — utiliser `DOMPurify`
- CORS restrictif : whitelist explicite (`ALLOWED_ORIGINS`), jamais `*` en production
- RLS activé sur TOUTES les tables Postgres/Supabase — vérifier avec `scripts/supabase_rls_check.py`
- CSRF tokens sur les formulaires modifiant l'état serveur (hors API stateless JWT)
- Logger les 401/403 avec IP + user-agent (détection brute force)
- Scanner les secrets AVANT commit — `python scripts/scan_secrets.py --staged-only`
- Auditer les deps AVANT deploy — `pnpm audit` + `socket scan` (supply chain)

## Interdit
- Ne PAS exposer les stack traces en production (`NODE_ENV === 'production'` check)
- Ne PAS utiliser des packages avec CVEs HIGH/CRITICAL non patchés
- Ne PAS désactiver `eslint-plugin-security` rules
- Ne PAS stocker tokens/sessions en `localStorage` — cookies `httpOnly; Secure; SameSite=Strict`
- Ne PAS oublier `.env.example` pour chaque nouvelle variable sensible

## Activation
Charger cette rule pour : tout middleware, tout endpoint public, tout composant avec auth, avant deploy.

## RSS Feeds CVE (surveiller)
- CVEFeed (15 min) : https://cvefeed.io/rssfeed/
- CERT-FR : https://www.cert.ssi.gouv.fr/feed/
- CISA KEV : https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json

## Learned
