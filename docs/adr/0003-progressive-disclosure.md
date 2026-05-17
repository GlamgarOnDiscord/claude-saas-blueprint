# ADR 0003: Progressive Disclosure (niveaux d'usage)

## État
Accepté

## Date
2026-03-21

## Contexte
L'outillage IA (skills, agents, rules, mémoire) grossit avec le temps. Un `CLAUDE.md` qui charge **tout** en contexte à chaque session dégrade la qualité de l'agent :

- **HumanLayer** documente une dégradation de l'adhérence au-delà de ~150-200 instructions injectées (modèle + prompt système + `CLAUDE.md` combinés).
- **Anthropic** recommande explicitement un `CLAUDE.md` court et actionnable, avec le détail dans des fichiers séparés chargés à la demande.
- En pratique, les agents ignorent silencieusement des règles quand le contexte est surchargé.

## Décision
Nous adoptons un système à **3 niveaux** (progressive disclosure) :

| Niveau | Contenu chargé | Cas d'usage |
|--------|----------------|-------------|
| **Essentiel** | `CLAUDE.md` seul (~90 lignes) | Scripts, POC, repos simples |
| **Standard** | + mémoire (`stack`, `session`) + 2-3 skills ciblés | SaaS en développement actif |
| **Complet** | + tout `.claude/` (36 skills, 7 agents, roadmap, ADR) | Multi-produits, équipes |

**Principes** :
1. Le `CLAUDE.md` racine ne contient que ce qui s'applique à **chaque** session.
2. Les skills se chargent **à la demande** via `/nom` — jamais globalement.
3. Les rules se chargent **avant** de toucher au domaine concerné (API, DB, auth, UI).
4. Le skill `/scope-task` aide à sélectionner le bon niveau pour la tâche courante.
5. **Règle d'or** : si un fichier n'a pas été ouvert depuis une semaine, il ne devrait pas être dans le flux par défaut.

## Conséquences
- Meilleure adhérence de l'agent aux instructions critiques.
- Réduction du coût (moins de tokens consommés par session).
- Courbe d'apprentissage légèrement plus haute pour savoir quel skill charger quand.
- Nécessite un index de skills à jour (`.claude/skills/README.md`).

## Sources
- [HumanLayer — Writing a good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md)
- [Anthropic — Best practices](https://docs.anthropic.com/en/docs/claude-code/best-practices)
- `docs/recherche-sources-2026.md` (synthèse locale)
