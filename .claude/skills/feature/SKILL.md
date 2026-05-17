---
name: feature
description: "Implémentation end-to-end d'une feature SaaS via le pattern **Prompt Discovery** (multi-step)."
argument-hint: "- `description` : Description de la feature à implémenter"
disable-model-invocation: true
---

## Arguments
- `description` : Description de la feature à implémenter

## Architecture Multi-Step (Prompt Discovery)
Cette skill utilise des **étapes séparées** pour éviter le "Lost in the Middle".
Chaque étape est dans un fichier distinct — l'instruction en cours est toujours la plus récente dans le contexte.

## Orchestration

### Étape 1 — EXPLORE (obligatoire)
Lire et exécuter `.claude/skills/feature/steps/step-1-explore.md`
- Lancer 3 sous-agents en parallèle (codebase, doc externe, rules)
- Synthétiser les résultats
- Ne PAS passer à l'étape 2 tant que l'exploration n'est pas terminée

### Étape 2 — PLAN (obligatoire)
Lire et exécuter `.claude/skills/feature/steps/step-2-plan.md`
- Créer le plan d'architecture (core → adapters → UI → tests)
- Si blast radius > 5 fichiers → EnterPlanMode pour approbation
- Ne PAS passer à l'étape 3 sans plan validé

### Étape 3 — EXECUTE
Lire et exécuter `.claude/skills/feature/steps/step-3-execute.md`
- Implémenter étape par étape en respectant l'ordre strict
- Lire la rule contextuelle AVANT chaque type de fichier modifié
- Paralléliser la génération de tests via sous-agent

### Étape 4 — VERIFY (obligatoire, jamais skip)
Lire et exécuter `.claude/skills/feature/steps/step-4-verify.md`
- 6 checks : types, lint, tests, sécurité, architecture, visuel
- Si erreur découverte → ajouter dans `rules/_learned.md`
- Mettre à jour la memory (domains, roadmap, session)

## Important
- **Chaque étape est un fichier séparé** — lire le fichier de l'étape en cours, pas tous d'un coup
- **Ne JAMAIS sauter une étape** — l'exploration et la planification sont obligatoires
- **Fail-stop** : 2 échecs consécutifs sur une étape → arrêt + demande utilisateur
