# Feature — Step 1: Explore

## Objectif
Comprendre le contexte AVANT de coder quoi que ce soit.

## Actions (paralléliser via sous-agents)

### Agent 1 — Scan du codebase
- Lire `.claude/memory/stack.md` et `.claude/memory/domains.md`
- Chercher des features similaires déjà implémentées (Grep patterns)
- Identifier le style et les conventions du code existant
- Lister les fichiers qui seront dans le blast radius

### Agent 2 — Recherche externe
- Chercher la documentation des libs/APIs nécessaires (WebSearch)
- Vérifier les bonnes pratiques pour ce type de feature
- Chercher des exemples d'implémentation de référence

### Agent 3 — Rules contextuelles
- Lire les rules correspondant aux fichiers qui seront touchés
- Lire `.claude/rules/_learned.md` pour les erreurs passées
- Charger le guide platform approprié (`platforms/*.md`)

## Output attendu
Synthèse courte dans ce format :
```
## Exploration terminée
- Stack: [framework + ORM + auth]
- Pattern existant: [comment les features similaires sont structurées]
- Blast radius: [liste des fichiers à créer/modifier]
- Libs nécessaires: [à installer si besoin]
- Rules actives: [rules à respecter]
- Risques: [points d'attention identifiés]
```

## Transition
→ Passer à `step-2-plan.md`
