# Pipeline d’assets multimédia (SaaS)

Guide de référence pour **générer, stocker et servir** des assets (SVG, images, vidéo, expériences 3D) sans exposer de secrets et sans mélanger les responsabilités.

## Principes (non négociables)

1. **Clés API uniquement côté serveur** (Route Handler, Server Action, worker, cron). Jamais dans le bundle client, jamais dans `NEXT_PUBLIC_*` pour les fournisseurs payants.
2. **Stockage objet** pour les fichiers générés (S3, R2, Supabase Storage, GCS) — URLs signées ou chemins publics après upload contrôlé.
3. **Traçabilité** : `request_id` / logs quand l’API les expose (ex. Quiver, Google).
4. **Charte unique** : un fichier `docs/brand-assets.md` (couleurs, typo, interdits) réutilisé dans les prompts — évite la dérive visuelle entre pages.

5. **Règle Cursor/Claude** : `.claude/rules/media-apis.md` — rappel **clés serveur uniquement**.

### Docs détaillées (intégration propre)

| Sujet | Fichier |
|--------|---------|
| Quiver + `QUIVERAI_API_KEY` | [`quiver-svg.md`](./quiver-svg.md) |
| Gemini / Nano Banana (images) | [`pipeline-images.md`](./pipeline-images.md) |
| Remotion + dossier `video/` | [`remotion-video.md`](./remotion-video.md) |
| ElevenLabs & audio | [`audio-voice.md`](./audio-voice.md) |
| Veille outils IA (MCP, buzz) | [`ai-tools-veille-2026.md`](./ai-tools-veille-2026.md) |

---

## Matrice : quoi utiliser quand

| Besoin | Piste recommandée | Notes |
|--------|-------------------|--------|
| **SVG** (icônes, illustrations vectorielles, logos exportables) | [QuiverAI API](https://docs.quiver.ai/api-reference/introduction) | `POST /v1/svgs/generations`, `POST /v1/svgs/vectorizations`. Auth Bearer, base `https://api.quiver.ai/v1`. Crédits + rate limits documentés. SDK : [`@quiverai/sdk`](https://github.com/quiverai/quiverai-node). |
| **Images raster** (hero, marketing, mockups) | **Gemini API** / **Nano Banana Pro** (Google) via [Google AI Studio](https://aistudio.google.com), [Vertex AI](https://cloud.google.com/vertex-ai), ou agrégateurs type [fal.ai](https://fal.ai/models/fal-ai/nano-banana-pro/api), [Replicate](https://replicate.com/google/nano-banana-pro) | Vérifier **prix, résolution max, CGU** avant production. Préférer **une** source par projet pour simplifier la facturation. |
| **Vidéo programmatique** (démos produit, exports batch, social) | [Remotion](https://www.remotion.dev/) + doc [Remotion + AI](https://www.remotion.dev/docs/ai/) | Projet **séparé** ou package `video/` dans le monorepo. Licence commerciale à valider sur [remotion.dev](https://www.remotion.dev). |
| **Site « scroll 3D »** (WebGL + scroll cinématique) | **React Three Fiber** + **GSAP ScrollTrigger** (+ option **Lenis** scroll) | Pas une API IA : c’est du **runtime front**. Tutoriels récents : [Codrops + GSAP 3D scroll](https://tympanus.net/codrops/2025/11/19/how-to-build-cinematic-3d-scroll-experiences-with-gsap/). L’IA aide à **coder** la scène et les assets ; le rendu reste Three.js. |

---

## Variables d’environnement (exemple)

À adapter dans **ton** dépôt applicatif. Détail par fournisseur : [`quiver-svg.md`](./quiver-svg.md), [`pipeline-images.md`](./pipeline-images.md), [`audio-voice.md`](./audio-voice.md).

```bash
QUIVERAI_API_KEY=
GOOGLE_API_KEY=          # ou équivalent Vertex / autre canal images
ELEVENLABS_API_KEY=      # si voix
ASSETS_BUCKET=
ASSETS_CDN_BASE_URL=
```

Documente les noms dans **`.env.example`** sans valeurs réelles.

---

## Flux type (image ou SVG)

```text
Client / admin UI
    → requête authentifiée vers TON API
        → appel fournisseur (Quiver / Google / autre) avec clé serveur
        → réception fichier ou JSON + URL
        → upload vers stockage objet
        → enregistrement métadonnées (DB : userId, orgId, type, hash, url)
        → réponse au client : URL signée ou id d’asset
```

Évite d’enchaîner **plusieurs** modèles sur la même requête utilisateur sans cache : coût et latence explosent.

---

## Quiver (SVG)

→ Détail complet : [`quiver-svg.md`](./quiver-svg.md)

---

## Images (Gemini / Nano Banana)

→ Détail complet : [`pipeline-images.md`](./pipeline-images.md)

---

## Vidéo (Remotion)

→ Quand créer `video/` et liens doc : [`remotion-video.md`](./remotion-video.md)

---

## Audio (ElevenLabs & co.)

→ [`audio-voice.md`](./audio-voice.md)

---

## Scroll 3D (front) — R3F + GSAP

- Stack : `@react-three/fiber`, `@react-three/drei`, `three`, **GSAP** (`ScrollTrigger`), souvent **Lenis** pour le scroll inertiel.
- Ce n’est **pas** une API IA : génération de code assistée ; runtime WebGL.
- Skill **`/ui`** (modes `landing` et `premium`) pointe cette stack pour les landings « scroll premium » ; guide : `platforms/web-app.md` section **Assets & médias**.
- Tutoriel récent : [Codrops — 3D scroll + GSAP](https://tympanus.net/codrops/2025/11/19/how-to-build-cinematic-3d-scroll-experiences-with-gsap/).

---

## Lien avec ce repo claude-saas-blueprint

- Skills utiles : `/ui` (modes `gen`, `premium`, `landing`), `/feature` (intégration pipeline dans une feature).
- Skill dédié : **`/assets-pipeline`** — rappelle ce document et la checklist agent.
- Veille : `.claude/memory/veille-2026-03.md` (section pipeline multimédia).

---

## Checklist avant mise en prod

- [ ] Aucune clé API dans le client ni dans le dépôt versionné.
- [ ] `.env.example` à jour ; secrets en gestionnaire (Vault, Doppler, Vercel env, etc.).
- [ ] Quotas et alertes budget sur chaque fournisseur IA.
- [ ] Politique de rétention des assets (RGPD / suppression compte).
- [ ] Tests smoke sur au moins un flux : génération → stockage → affichage.
