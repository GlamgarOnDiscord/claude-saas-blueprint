---
name: refactor
description: "Refactoring sûr et méthodique. Améliorer sans casser."
argument-hint: "- `scope` : Quoi refactorer (fichier, module, pattern) - `goal` : L'objectif du refactoring"
disable-model-invocation: true
---

## Arguments
- `scope` : Quoi refactorer (fichier, module, pattern)
- `goal` : L'objectif du refactoring

## Instructions

### Phase 1 — Comprendre l'existant
1. Lire le code à refactorer
2. Lister TOUS les fichiers qui importent/utilisent le code concerné (Grep)
3. Vérifier que les tests existent pour le code à refactorer
4. Si pas de tests → en écrire AVANT de refactorer

### Phase 2 — Planifier
Utiliser EnterPlanMode si blast radius > 3 fichiers.

Types de refactoring courants :
- **Extract** : Sortir une fonction/composant d'un fichier trop long
- **Rename** : Renommer pour clarifier (utiliser replace_all avec Grep)
- **Restructure** : Déplacer des fichiers dans une meilleure organisation
- **Simplify** : Réduire la complexité (dé-nester, éliminer les duplications)
- **Type-safe** : Remplacer `any` par des types stricts
- **Pattern** : Appliquer un design pattern (repository, factory, etc.)

### Phase 3 — Exécuter
Règles strictes :
1. **Un changement à la fois** — commit logique entre chaque transformation
2. **Tests verts entre chaque étape** — si un test casse, rollback
3. **Pas de changement de comportement** — le refactoring ne change que la forme
4. **Imports à jour** — vérifier après chaque déplacement de fichier

### Phase 4 — Valider
1. `tsc --noEmit` — zero erreur
2. Tous les tests passent
3. Grep pour vérifier qu'aucun ancien import/nom n'est resté
4. Review visuelle si UI impactée
