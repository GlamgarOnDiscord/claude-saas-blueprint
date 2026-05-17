---
name: apex
description: "Workflow APEX — Analyze, Plan, Execute, Examine. À invoquer avant une tâche non triviale ou quand le contexte est flou."
argument-hint: "[objectif ou ticket en une phrase]"
disable-model-invocation: true
---

# APEX — Cadre d’exécution

Utilise ce skill quand la tâche n’est **pas** un one-liner (sinon `/oneshot` ou `/fix`).

## A — Analyze
- Définir le **blast radius** (fichiers / modules touchés).
- Lire les types ou interfaces existantes qui seront modifiées.
- Charger **une** rule `.claude/rules/` pertinente (api, db, auth, ui, tests, config) — pas toutes.
- Consulter `.claude/rules/_learned.md` pour erreurs déjà vues.

## P — Plan
- Répondre en **3 lignes** : **QUOI** · **POURQUOI** · **COMMENT**.
- Si **plus de 5 fichiers** ou incertitude forte → **Plan Mode** / validation utilisateur avant code.

## E — Execute
- Un **diff par intention** ; pas de refactor gratuit hors scope.
- Paralléliser seulement ce qui est **indépendant** (fichiers sans dépendance croisée).

## X — Examine
- `tsc --noEmit` (ou équivalent stack).
- Tests sur le **blast radius** (pas toute la suite si inutile).
- Revue sécurité minimale sur les changements (auth, inputs, secrets).
- UI modifiée → capture ou description visuelle des écarts.

## Fail-stop
- **2 échecs consécutifs** sur la même étape → arrêt, diagnostic, demande à l’utilisateur.

## Références projet
- `CLAUDE.md` (workflow APEX), `docs/workflow-pragmatique.md` (niveaux d’usage).
