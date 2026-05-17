# Model Routing — Optimiser Coûts et Performance

## Principe
Utiliser le bon modèle pour la bonne tâche. Le modèle le plus cher n'est pas toujours nécessaire.

## Routing par Phase

### Phase de Réflexion → Opus (modèle le plus intelligent)
- `/brainstorm` — Décisions d'architecture complexes
- `/prd generate` — Rédaction du PRD
- `EnterPlanMode` — Plans d'implémentation
- `/feature` step-1 (explore) et step-2 (plan) — Analyse et planification
- Debugging complexe — Quand l'agent tourne en rond

### Phase d'Exécution → Sonnet ou Haiku (modèle rapide/économique)
- `/oneshot` — Modifications rapides
- `/fix` — Bug fixes évidents
- `/feature` step-3 (execute) — Écriture de code (le plan est déjà fait)
- Génération de tests — Pattern répétitif
- Refactoring mécanique — Renommage, déplacement

### Phase de Vérification → Sonnet (équilibre qualité/coût)
- `/review` — Code review
- `/quality` — Audit qualité
- `/deploy-check` — Validation pré-deploy
- `/feature` step-4 (verify) — Vérification post-implémentation

## Implémentation avec Claude Code
Dans les appels Agent, utiliser le paramètre `model` :
```
Agent(subagent_type: "Explore", model: "haiku")     ← Recherches simples
Agent(subagent_type: "Plan", model: "opus")          ← Planification complexe
Agent(subagent_type: "clean-code-generator", model: "sonnet")  ← Exécution
Agent(subagent_type: "websearch", model: "haiku")    ← Recherche web
```

## Règle d'Or
- **Penser** avec le meilleur modèle (Opus)
- **Coder** avec un modèle rapide (Sonnet)
- **Chercher** avec le modèle le plus léger (Haiku)

## Quand Monter en Gamme
- Si le sous-agent Haiku retourne un résultat de mauvaise qualité → relancer en Sonnet
- Si le sous-agent Sonnet échoue sur un plan → relancer en Opus
- Ne JAMAIS utiliser Opus pour des tâches mécaniques (waste de tokens)
