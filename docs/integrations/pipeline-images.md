# Pipeline images (Gemini / Nano Banana Pro)

Complète [`assets-pipeline.md`](./assets-pipeline.md). Règle projet : **`.claude/rules/media-apis.md`** (clés **serveur uniquement**).

## Rôle

- Générer ou éditer des **images raster** (hero, marketing, mockups, variantes produit) via l’écosystème **Google** (Gemini / modèles type Nano Banana Pro selon les noms commercialisés sur chaque plateforme).

## Variables d’environnement (exemples)

Selon le chemin d’accès choisi — **une** source principale par projet pour la facturation :

```bash
# Google AI Studio / Gemini API (exemple)
GOOGLE_API_KEY=

# Ou Vertex AI — préférer workload identity en prod au lieu de clé en dur
# GOOGLE_APPLICATION_CREDENTIALS=...
```

- **Interdit** : exposer ces clés au navigateur pour de la génération facturée.

## Accès API (à choisir une fois)

| Canal | Usage typique |
|-------|----------------|
| [Google AI Studio](https://aistudio.google.com) | Prototypage, clé dev |
| [Gemini API — image generation](https://ai.google.dev/gemini-api/docs/image-generation) | Doc officielle |
| [Vertex AI](https://cloud.google.com/vertex-ai) | Entreprise, GCP |
| [fal.ai — Nano Banana Pro](https://fal.ai/models/fal-ai/nano-banana-pro/api) | Agrégateur, quotas fal |
| [Replicate](https://replicate.com/google/nano-banana-pro) | Jobs / scaling |

Vérifier **prix, résolution max, CGU** et **droits d’usage commercial** sur le canal retenu.

## Flux recommandé

1. Requête authentifiée → **ton** backend.
2. Appel fournisseur avec clé serveur.
3. Réception fichier ou URL → upload **stockage objet** → enregistrement métadonnées (org, user, hash).
4. Réponse client : URL CDN ou signée.

## Bonnes pratiques prompts

- Réutiliser `docs/brand-assets.md` (couleurs, style, interdits).
- Fixer **ratio** et **résolution** cible pour limiter coût et retouches.

## Voir aussi

- SVG (autre pipeline) : [`quiver-svg.md`](./quiver-svg.md)
