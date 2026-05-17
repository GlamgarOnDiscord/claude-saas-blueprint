---
name: brainstorm
description: "Mode exploration intensive. Lance plusieurs sous-agents pour explorer, challenger et synthétiser des recommandations sur un sujet complexe. Gourmand en tokens mais produit des décisions éclairées."
---

## Quand utiliser
- Choix d'architecture (monolith vs microservices, DB choice, auth strategy)
- Choix de stack pour un nouveau projet
- Refactoring majeur (plusieurs approches possibles)
- Décision technique avec des trade-offs non évidents
- "Comment implémenter X ?" quand X est complexe

## Arguments
- `question` : La question ou le problème à explorer

## Instructions

### Phase 1 — Lancement du Swarm (4 agents en parallèle)

**Agent 1 — Researcher (websearch)**
```
"Rechercher les meilleures pratiques 2026 pour [sujet].
Trouver :
- Ce que recommandent les docs officielles
- Les articles techniques récents (blog posts, talks)
- Les comparatifs objectifs (benchmarks, DX)
Retourner les 5 points clés avec sources."
```

**Agent 2 — Codebase Analyst (Explore)**
```
"Analyser le codebase actuel pour comprendre :
- Les patterns déjà en place
- Les contraintes techniques existantes
- Ce qui devrait être préservé vs ce qui peut changer
- Les dépendances qui influencent le choix
Retourner un résumé des contraintes."
```

**Agent 3 — Devil's Advocate (general-purpose)**
```
"Pour la question '[question]', jouer l'avocat du diable.
Pour chaque option envisagée :
- Lister les risques et inconvénients cachés
- Identifier les scénarios où ça pourrait mal tourner
- Challenger les hypothèses populaires
- Proposer des alternatives non évidentes
Être critique mais constructif."
```

**Agent 4 — Experience Scout (websearch)**
```
"Chercher des retours d'expérience (post-mortems, case studies) de projets
qui ont implémenté [sujet/option].
Trouver :
- Ce qui a bien marché
- Ce qui a échoué et pourquoi
- Les regrets courants
- Les surprises positives
Retourner 3-5 témoignages concrets."
```

### Phase 2 — Synthèse
Après réception des 4 résultats, synthétiser :

```markdown
## Brainstorm: [Question]

### Contexte Projet
[Résumé des contraintes du codebase — Agent 2]

### Options Analysées

#### Option A: [Nom]
- **Pour** : [arguments — Agents 1, 4]
- **Contre** : [risques — Agent 3]
- **Retour terrain** : [expériences réelles — Agent 4]
- **Effort** : S | M | L | XL
- **Score** : ★★★★☆

#### Option B: [Nom]
- **Pour** : [...]
- **Contre** : [...]
- **Retour terrain** : [...]
- **Effort** : S | M | L | XL
- **Score** : ★★★☆☆

[Etc.]

### Recommandation
**[Option recommandée]** parce que [raison principale].
Plan de migration : [étapes si applicable].
```

### Phase 3 — Décision
Demander à l'utilisateur via AskUserQuestion :
- Présenter le top 2-3 options avec un résumé d'une ligne chacune
- Laisser l'utilisateur choisir ou demander plus de détails

### Phase 4 — Documentation
- Sauver la décision dans `.claude/memory/decisions.md`
- Si c'est un choix d'architecture → créer un ADR dans `docs/adr/`
- Mettre à jour les fichiers de memory impactés (stack, patterns)
