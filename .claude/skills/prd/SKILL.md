---
name: prd
description: "Workflow complet \"PRD to Tasks\" pour construire un SaaS de A à Z. Brainstorm → PRD → Architecture → Tasks → Exécution automatique."
disable-model-invocation: true
---

## Modes

### `/prd brainstorm [idée]` — Phase 1 : Exploration
Utiliser `/brainstorm` pour explorer l'idée :
- Quel problème ça résout ?
- Qui sont les utilisateurs cibles ?
- Quels sont les concurrents ?
- Quel est le business model ?
- Quel est le MVP minimal ?

Output : Synthèse validée par l'utilisateur.

### `/prd generate` — Phase 2 : Rédiger le PRD
Générer un Product Requirements Document structuré dans `docs/prd.md` :

```markdown
# PRD — [Nom du Produit]

## 1. Vision
- Problème résolu
- Proposition de valeur unique
- Utilisateurs cibles

## 2. Scope MVP
- Features incluses (must-have)
- Features exclues (v2, v3)
- Contraintes techniques

## 3. User Stories
- En tant que [rôle], je veux [action], afin de [bénéfice]
- Organisées par priorité (P0, P1, P2)

## 4. Architecture Technique
- Stack choisie (via /brainstorm si pas encore décidé)
- Schema de données (entités principales + relations)
- Diagramme de flux (auth, paiement, features core)
- Intégrations tierces (Stripe, email, etc.)

## 5. Pages & Navigation
- Sitemap avec toutes les pages
- Wireframes textuels des pages clés

## 6. API Endpoints
- Liste des endpoints nécessaires
- Formats de requête/réponse

## 7. Métriques de Succès
- KPIs à tracker
- Critères de "done" pour le MVP
```

### `/prd tasks` — Phase 3 : Découper en Tasks
Transformer le PRD en tasks atomiques dans `.claude/memory/roadmap/backlog.md` :

**Règles de découpage :**
- `[S]` = 1 fichier ou moins, `[M]` = 2-5 fichiers, `[L]` = 6+ fichiers (→ décomposer avant exec)
- Chaque task = 1 commit logique, indépendante ou dépendances explicites
- Ordre : DB schema → Core logic → API → UI → Tests
- Grouper par sprint (Sprint 1 = fondations, Sprint 2 = features core, Sprint 3 = polish)

**Format :**
```markdown
### Sprint 1 — Fondations
- [ ] [S] Setup projet avec /saas-init
- [ ] [M] Schema DB users + organizations + memberships
- [ ] [M] Auth flow (register, login, logout)
- [ ] [S] Layout principal (sidebar, header, navigation)
- [ ] [S] Page dashboard vide

### Sprint 2 — Core Features
- [ ] [M] Feature: [feature 1 du PRD]
- [ ] [M] Feature: [feature 2 du PRD]
- [ ] [M] Intégration Stripe (plans, checkout, webhooks)

### Sprint 3 — Polish & Ship
- [ ] [M] Landing page
- [ ] [S] SEO + meta tags
- [ ] [M] Tests E2E parcours critiques
- [ ] [S] Deploy check + mise en production
```

### `/prd exec` — Phase 4 : Exécution Automatique

**Avant de démarrer :**
1. Lire `backlog.md` — vérifier que toutes les tasks `[L]` sont décomposées en `[M]` ou `[S]`
2. Confirmer le sprint à exécuter avec l'utilisateur

**Boucle d'exécution :**
1. Prendre la première task non cochée du sprint en cours
2. Si task `[L]` → **stop**, demander à l'utilisateur de la décomposer d'abord
3. Lancer le skill approprié :
   - Tasks DB → `/schema-gen`
   - Tasks API → `/api-gen`
   - Tasks Feature → `/feature`
   - Tasks UI → `/ui gen`
   - Tasks Landing → `/ui landing`
4. Après complétion → `tsc --noEmit` + tests ciblés. Si échec → **stop, signaler**
5. Cocher la task dans `backlog.md`, commit
6. Passer à la suivante

**Fin de sprint :**
- `/review` automatique
- `/deploy-check staging`
- **Pause obligatoire** — demander validation utilisateur avant sprint suivant

**Garde-fous :**
- Task échoue 2 fois → arrêt + demande utilisateur (ne pas retry en boucle)
- Ne PAS modifier le PRD sans validation utilisateur
- Ne PAS sauter les tests entre tasks — chaque task doit laisser le projet dans un état stable
