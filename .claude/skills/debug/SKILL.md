---
name: debug
description: "Debugging systématique avec analyse profonde. Traque la cause racine, pas le symptôme."
---

## Instructions

### Phase 1 — Reproduire
1. Comprendre le symptôme exact (message d'erreur, comportement attendu vs observé)
2. Identifier le fichier et la ligne si disponible
3. Identifier le contexte : quand ça arrive, quand ça n'arrive pas

### Phase 2 — Isoler (paralléliser via sous-agents)
Lancer en parallèle :

**Agent Explore** → Tracer le call stack :
- Trouver la fonction qui crash
- Remonter la chaîne d'appels
- Identifier les inputs qui causent le problème

**Agent Explore** → Chercher des patterns similaires :
- Le même code fonctionne-t-il ailleurs ?
- Y a-t-il eu un changement récent dans le blast radius ?
- `git log --oneline -10 -- [fichier]` pour l'historique récent

**Agent WebSearch** (si erreur de lib) → Chercher :
- Message d'erreur exact + nom de la lib
- Issues GitHub connues
- Breaking changes dans les mises à jour récentes

### Phase 3 — Diagnostiquer
Utiliser l'agent `unit-testing:debugger` si le problème est complexe.

Checklist de causes courantes :
- [ ] Type mismatch (null/undefined inattendu)
- [ ] Import cassé ou circulaire
- [ ] Variable d'environnement manquante
- [ ] Race condition / async mal géré
- [ ] Cache stale (build, node_modules, .next)
- [ ] Version de dépendance incompatible
- [ ] Changement de schema DB sans migration

### Phase 4 — Fix
1. Écrire le fix minimal ciblé
2. Ajouter un test qui aurait attrapé le bug
3. Vérifier que le fix ne casse rien d'autre (`tsc --noEmit` + tests)
4. Documenter dans `.claude/memory/errors.md` si le pattern est réutilisable

### Anti-Patterns de Debug
- Ne PAS ajouter des `console.log` partout → utiliser un breakpoint mental
- Ne PAS deviner → vérifier avec des faits (logs, valeurs, types)
- Ne PAS corriger le symptôme → trouver la cause racine
- Ne PAS réessayer en boucle → si 2 tentatives échouent, changer d'approche
