# Remotion — vidéo programmatique (optionnel)

Ne fait pas partie du runtime web classique : c’est un **projet Node/React** qui **rend** de la vidéo (MP4, etc.). Doc : [Remotion](https://www.remotion.dev/) · [Remotion + AI](https://www.remotion.dev/docs/ai/) · [Claude Code](https://www.remotion.dev/docs/ai/claude-code).

## Quand créer un sous-projet `video/`

Crée un dossier **`video/`** à la racine du monorepo (ou package `apps/video`) si :

- tu produis des **démos produit**, **exports social**, **tutoriels** à partir de données ou de templates ;
- tu veux des **rendus reproductibles** (CI, même charte que le code) ;
- la durée de rendu dépasse quelques secondes → **jobs async** / file d’attente, pas une route HTTP synchrone.

**Ne crée pas** `video/` si tu n’as besoin que de vidéos ponctuelles faites à la main — utilise un outil externe.

## Bootstrap rapide

```bash
npx create-video@latest
# ou suivre https://www.remotion.dev/docs/
```

Ensuite, intégration agent : [Generate with LLMs](https://www.remotion.dev/docs/ai/generate).

## Licence

Usage commercial : vérifier [Remotion — licensing](https://www.remotion.dev/docs/) selon taille d’équipe / revenus.

## Lien

→ [`assets-pipeline.md`](./assets-pipeline.md) (matrice globale)
