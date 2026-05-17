# `.claude/guides/` — Guides multi-agents

Ces fichiers sont des **guides de pattern** consultés à la demande par l'agent principal lorsqu'il doit orchestrer du travail en parallèle, choisir un modèle, ou debugger. Ce ne sont **pas** des subagents — voir `../agents/README.md`.

| Fichier | Rôle |
|---------|------|
| `orchestration.md` | Quand utiliser quel sous-agent · patterns de parallélisation · agent teams |
| `model-routing.md` | Routing Opus/Sonnet/Haiku par phase (penser/coder/chercher) |
| `context-management.md` | Stratégies pour ne pas saturer le contexte |
| `debugging-techniques.md` | Visual feedback, log technique, bisect, isolation |
| `testing-strategy.md` | Pyramide de tests SaaS · coverage cibles |
| `prompt-patterns.md` | Patterns réutilisables pour les sous-agents |
| `visual-context.md` | Screenshots annotés, React Grab, comparaison maquette/réalité |

**Quand consulter ces guides** : avant de lancer 2+ agents en parallèle, avant un debug long, avant une feature XL. Pas systématique.
