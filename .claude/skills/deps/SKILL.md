---
name: deps
description: "Analyse, audite et gère les dépendances du projet intelligemment."
---

## Instructions

### Mode: Audit
Exécuter en parallèle :

1. **Outdated Check**
   - `npm outdated` ou `bun outdated` ou équivalent
   - Lister les packages avec mises à jour majeures disponibles
   - Vérifier les changelogs des mises à jour majeures (breaking changes)

2. **Security Audit**
   - `npm audit` ou équivalent + `python scripts/scan_secrets.py`
   - Vérifier [Socket.dev](https://socket.dev) pour supply-chain (malware, typosquatting)
   - Lister les vulnérabilités par sévérité
   - Proposer les fixes automatiques quand possible

3. **Bundle Analysis**
   - Identifier les dépendances les plus lourdes
   - Proposer des alternatives plus légères si pertinent
   - Exemples : moment.js → dayjs, lodash → lodash-es ou natif

4. **Dead Dependencies**
   - Scanner les imports du projet
   - Identifier les packages dans package.json qui ne sont jamais importés
   - Proposer leur suppression

### Mode: Add
Quand l'utilisateur veut ajouter une dépendance :
1. Vérifier la popularité et maintenance (dernière release, stars, issues)
2. Vérifier la taille du bundle (bundlephobia)
3. Vérifier les vulnérabilités connues
4. Proposer des alternatives si pertinent
5. Installer avec la bonne commande (`--save-dev` si outil de dev)

### Mode: Recommandations SaaS
Packages recommandés par catégorie :

**UI** : shadcn/ui (pas une dépendance, copié), tailwindcss, lucide-react
**Forms** : react-hook-form, zod
**State** : zustand, jotai
**Data Fetching** : @tanstack/react-query
**Date** : date-fns ou dayjs
**Email** : resend, react-email
**Auth** : next-auth, @supabase/ssr (si stack Supabase)
**DB** : drizzle-orm, @supabase/supabase-js (Supabase) ou @neondatabase/serverless (Neon)
**Paiements** : stripe
**Upload** : uploadthing
**Analytics** : @posthog/next
**Logging** : pino
**Testing** : vitest, @playwright/test

### Montée majeure avec veille changelog complète
- Si une **seule** dépendance ou API nécessite lecture des **release notes** officielles, breaking changes et migration propre → **`/deep-update`** (voir `docs/processus-mise-a-jour-profonde.md`) plutôt que seulement ce mode Audit.

### Rapport
```
## Dépendances : X total (Y prod, Z dev)
## Vulnérabilités : X critical, Y high, Z moderate
## Outdated : X packages (Y majeurs)
## Dead : X packages non utilisés
## Bundle : Xkb (top 5 plus lourds)
## Recommandation : [actions à prendre]
```
