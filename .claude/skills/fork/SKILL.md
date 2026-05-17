---
name: fork
description: "\"Fork and Hack\" — Cloner un projet Open Source existant et le customiser pour son besoin. Plus rapide que tout coder from scratch."
argument-hint: "- `repo` : URL GitHub du repo à forker (ou nom court ex: "shadcn/ui") - `goal` : Ce qu'on veut en faire / les modificati"
disable-model-invocation: true
---

## Arguments
- `repo` : URL GitHub du repo à forker (ou nom court ex: "shadcn/ui")
- `goal` : Ce qu'on veut en faire / les modifications à apporter

## Instructions

### Phase 1 — Évaluer le Repo
Avant de cloner, vérifier via sous-agents :

**Agent WebSearch :**
- License compatible ? (MIT, Apache = OK, GPL = attention)
- Dernière activité ? (> 6 mois sans commit = risque)
- Stars / forks / issues ouvertes ?
- Stack compatible avec la nôtre ?

**Agent WebFetch (README du repo) :**
- Quelles features sont déjà implémentées ?
- Quelles sont les dépendances ?
- Comment le setup ?

### Phase 2 — Cloner et Explorer
1. `git clone [repo] [nom-projet]`
2. Lancer `/onboard` pour scanner le projet cloné
3. Lancer `/onboard` pour comprendre la structure
4. Identifier les fichiers à modifier vs ceux à garder tel quel

### Phase 3 — Plan de Customisation
Via EnterPlanMode, planifier :
```
## Ce qu'on garde
- [liste des features/fichiers à conserver]

## Ce qu'on modifie
- [feature] → [modification]
- [UI] → [nouveau design]

## Ce qu'on ajoute
- [nouvelle feature]
- [intégration]

## Ce qu'on supprime
- [feature inutile]
- [pages/routes non nécessaires]
```

### Phase 4 — Exécuter
1. Supprimer le code inutile d'abord (réduire la surface)
2. Rebrander (nom, logo, couleurs, textes)
3. Modifier les features existantes
4. Ajouter les nouvelles features
5. Tester le tout

### Phase 5 — Nettoyer
1. Supprimer l'historique git du projet original : `rm -rf .git && git init`
2. Mettre à jour le README
3. Mettre à jour le `package.json` (nom, version, description)
4. Vérifier les licenses et attributions
5. `/deploy-check`

### Anti-Patterns
- Ne PAS forker un projet plus complexe que ce qu'on a besoin
- Ne PAS garder du code qu'on ne comprend pas
- Ne PAS ignorer la license
- Préférer les projets avec une architecture propre (plus facile à modifier)
