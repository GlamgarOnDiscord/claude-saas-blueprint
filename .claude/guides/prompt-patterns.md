# Prompt Patterns Réutilisables

## Patterns pour des résultats optimaux avec les sous-agents

### Pattern 1 — Recherche Ciblée
```
Prompt: "Dans le projet [path], trouve tous les fichiers qui [critère].
Pour chaque fichier trouvé, liste :
- Le chemin
- Les exports principaux
- Les dépendances (imports)
Retourne un résumé structuré, pas le contenu complet."
```
Usage : Agent Explore pour mapper un domaine

### Pattern 2 — Analyse Comparative
```
Prompt: "Compare ces deux approches pour [problème] :
1. [Approche A]
2. [Approche B]
Critères : performance, maintenabilité, complexité.
Recommande une approche avec justification en 3 lignes max."
```
Usage : Agent general-purpose pour les décisions techniques

### Pattern 3 — Génération de Tests
```
Prompt: "Génère les tests pour [fichier].
Couvre :
- Le happy path
- Les cas d'erreur (input invalide, not found, unauthorized)
- Le cas multi-tenant (isolation par organizationId)
Utilise Vitest, des mocks pour les dépendances, et le pattern AAA."
```
Usage : Agent test-automator

### Pattern 4 — Documentation de Code
```
Prompt: "Cherche la documentation officielle de [lib] version [X] pour [cas d'usage].
Retourne :
- L'API exacte à utiliser
- Un exemple de code minimal
- Les pièges courants à éviter"
```
Usage : Agent websearch

### Pattern 5 — Debug Distribué
```
Prompt: "L'erreur '[message]' apparaît dans [fichier:ligne].
Trace la chaîne d'appels en remontant depuis ce point.
Identifie :
- D'où vient la donnée qui cause l'erreur
- Quel est le type attendu vs reçu
- Où le contrat est violé"
```
Usage : Agent debugger

### Pattern 6 — Review de Code
```
Prompt: "Review les changements dans [fichiers].
Vérifie :
- Respect des conventions du projet (voir CLAUDE.md)
- Pas de régression dans le blast radius
- Types corrects, pas de any
- Pas de faille de sécurité
Retourne uniquement les problèmes trouvés."
```
Usage : Agent general-purpose post-implémentation

## Principes de Prompting pour Sous-Agents
1. **Être spécifique** — Dire exactement quoi chercher/faire
2. **Demander un format structuré** — Pas de prose, des listes
3. **Limiter le scope** — Un sujet par agent
4. **Demander un résumé** — Pas le contenu brut, une synthèse
