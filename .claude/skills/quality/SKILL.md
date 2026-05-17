---
name: quality
description: "Audit qualité approfondi du codebase. Identifie les problèmes, propose des fixes."
disable-model-invocation: true
---

## Instructions

### 1. Scan Structurel
Utiliser l'agent Explore pour :
- Mapper l'arborescence complète du projet
- Identifier les fichiers > 200 lignes (candidats au split)
- Détecter les imports circulaires
- Vérifier le respect de l'architecture hexagonale (core n'importe pas adapters)

### 2. Scan de Code
Utiliser Grep pour détecter :
- `any` dans les fichiers TypeScript
- `console.log` / `console.error` hors logger
- `TODO` / `FIXME` / `HACK` non résolus
- Fonctions > 50 lignes
- Fichiers sans export (dead code potentiel)
- Duplications évidentes (patterns copiés-collés)

### 3. Scan de Sécurité
- Secrets hardcodés
- SQL non paramétré
- Injection de HTML non sanitisé (innerHTML, etc.)
- Dépendances avec vulnérabilités connues

### 4. Scan DX
- Scripts npm/bun manquants (dev, build, test, lint)
- `.env.example` à jour
- README avec instructions de setup

### 5. Dashboard global
Lancer `python scripts/project_health.py` — retourne en une passe : erreurs TS, lint, tests, console.log/any counts, audit sécurité, structure hexagonale.

### 6. Rapport
Générer un rapport structuré :
- **Critiques** (bloquants)
- **Warnings** (à traiter)
- **Suggestions** (nice to have)
- **Métriques** : Fichiers, Lignes, Coverage, Score qualité (A/B/C/D)

Proposer de fix automatiquement les issues simples (unused imports, console.log, etc.)
