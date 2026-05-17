---
name: onboard
description: "Onboarding complet sur un projet existant. Analyse, comprend et documente le projet pour que l'agent soit immédiatement productif."
disable-model-invocation: true
---

## Instructions

### Phase 1 — Scan Rapide (4 agents parallèles)

**Agent 1 — Structure & Stack :**
- Lire `package.json` / `pyproject.toml` (dépendances = stack réelle)
- Identifier framework, runtime, ORM, auth, paiements
- Détecter package manager (pnpm/bun/npm via lockfile)

**Agent 2 — Architecture & Patterns :**
- Arborescence 2 niveaux max
- Pattern architectural : hexagonal | MVC | feature-based | flat
- Conventions de nommage (kebab, camel, PascalCase sur les fichiers)
- Détecter si `organizationId` présent sur les tables → multi-tenant

**Agent 3 — Tests & Qualité :**
- Test runner + config (vitest.config, jest.config, playwright.config)
- Ratio fichiers test / fichiers source
- Chercher `console.log` et `any` (indicateurs de dette rapide)
- Chercher secrets hardcodés : patterns `sk_`, `pk_`, `password=`, `secret=`

**Agent 4 — Infra & Deploy :**
- CI/CD : `.github/workflows/`, `.gitlab-ci.yml`
- Provider déploiement (Vercel, Railway, Docker, AWS)
- DB et auth provider
- Variables `.env.example` présentes ?

### Phase 2 — Health Check (script unifié)
```bash
python scripts/project_health.py
```
Retourne : erreurs TS, lint, tests, console.log count, any count, structure hexagonale, audit sécurité.

### Phase 3 — Deep Dive (si nécessaire)
Lire les fichiers critiques :
1. Point d'entrée principal (`app/layout.tsx`, `main.ts`, `server.ts`)
2. Schema DB / dernières migrations
3. Middleware d'auth
4. 1-2 features complètes comme référence de style

### Phase 4 — Documentation
Générer/mettre à jour :
1. **`.claude/memory/project-scan.md`** — scan complet
2. **`.claude/memory/stack.md`** — stack + versions
3. **`.claude/memory/domains.md`** — domaines et entités détectés
4. **`.claude/memory/patterns.md`** — patterns de code observés

### Phase 5 — Recommandations
Basé sur le scan, identifier et prioriser :
- **Critique** : secrets hardcodés, tables sans RLS, 0 tests
- **Warning** : dette TS (`any`), console.log en prod, migrations non appliquées
- **Nice to have** : structure hexagonale absente, README vide

### Output Final

```
Projet analysé : [nom]
Stack : [framework] + [DB] + [auth]
Architecture : [pattern] — [conforme/non-conforme hexagonale]
Fichiers : X source, Y tests (ratio Z%)
Multi-tenant : oui/non (organizationId détecté : oui/non)
Secrets scan : OK / ⚠️ [X patterns suspects]

Santé : X/10
  - TS errors : X
  - console.log : X
  - any : X
  - Tests : X%

Priorité 1 : [action critique]
Priorité 2 : [action importante]

Prêt à travailler. → /feature ou /fix pour commencer.
```

**Critères Santé 10/10 :** 0 erreur TS, 0 console.log, <5% `any`, >60% coverage, RLS sur toutes les tables, 0 secret hardcodé.
