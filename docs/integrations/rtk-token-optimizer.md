# RTK — Rust Token Killer

**Réduit la consommation de tokens Claude Code de 60-90%.**

- GitHub : https://github.com/rtk-ai/rtk
- Site : https://www.rtk-ai.app/
- Cas réel : 89% de réduction sur sessions Claude Code (10M+ tokens économisés)

## Concept

RTK est un proxy CLI en Rust (binaire unique, ~10ms overhead) qui s'intercale entre le terminal et l'IA. Il filtre, compresse et groupe les outputs verbeux AVANT qu'ils arrivent dans le contexte de Claude Code.

```
Claude Code → rtk → commande réelle → output filtré → Claude Code
```

## Installation

```bash
# macOS
brew install rtk-ai/tap/rtk

# Linux
curl -fsSL https://install.rtk-ai.app | sh

# Windows
winget install rtk-ai.rtk

# Activation globale (toutes les commandes passent par RTK)
rtk init --global

# Vérifier
rtk status
rtk gain   # statistiques d'économie
```

Ou via le script Python :
```bash
python scripts/rtk_setup.py --install
```

## Commandes optimisées

RTK supporte 50+ commandes. Les plus utiles pour un dev SaaS :

| Commande | Réduction typique |
|----------|------------------|
| `git diff` / `git log` | 70-85% |
| `pytest` / `jest` / `vitest` | 60-80% |
| `eslint` / `ruff` / `biome` | 65-75% |
| `pnpm install` | 80-90% |
| `docker build` | 75-85% |
| `tsc --noEmit` | 50-70% |

## Intégration avec ce workflow

Après `rtk init --global`, toutes les commandes Bash de Claude Code passent automatiquement par RTK. Aucune modification du workflow nécessaire.

**Complémentaire aux scripts Python** :
- Les scripts `scripts/*.py` remplacent les commandes longues par des résumés
- RTK optimise les commandes directes que l'agent doit quand même lancer
- Ensemble : économie estimée de 80%+ des tokens liés aux commandes

## Voir aussi

- `scripts/rtk_setup.py` — Check statut et guide installation
- `docs/integrations/ai-tools-2026.md` — Autres outils de l'écosystème
