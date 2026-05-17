# Image pipeline — Generation visuels via Gemini

## Quand utiliser
- Hero backgrounds, feature illustrations, avatars synthetiques
- Apres avoir genere la structure de la page (`/ui premium` ou `/ui landing`)
- **Pas pour** les cas ou l'image affecte la comprehension factuelle (specs produit, schemas, prix)

## Pipeline

### 1. Detection des zones
Scanner le HTML/JSX pour :
- `<img>` avec sources placeholder
- `bg-[url(...)]` Tailwind ou CSS inline
- Conteneurs SVG vides
- URLs `placehold.co` ou `picsum.photos`

### 2. Crafting du prompt
Pour chaque zone :
```
Generate an image: <contexte produit>, <secteur>, <couleur accent du design system>,
<zone-specifique : "wide cinematic" pour hero, "icon-sized clean" pour feature,
"portrait minimal" pour avatar>, <mood>, <style: "Clean digital illustration,
no text overlays, SaaS-appropriate">
```

### 3. Generation

**Avec `GEMINI_API_KEY`** (server-side uniquement, voir `rules/media-apis.md`) :
```bash
curl -s "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent?key=$GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"contents":[{"parts":[{"text":"<prompt>"}]}],"generationConfig":{"responseModalities":["TEXT","IMAGE"]}}'
```

**Sans cle (fallback placeholder)** :
```
https://picsum.photos/seed/<context-slug>/800/600
https://placehold.co/800x600/09090b/ffffff?text=<label>
```

### 4. Validation
Pour les zones qui affectent la comprehension :
- Alt text precis et factuel
- Pas de texte critique non-label dans l'image
- Contraste lisible (overlay si fond utilise)
- Pas de personnes / marques / resultats trompeurs
- Statut "image synthetique" indique si pertinent

## Securite et stockage

- Cles API **jamais** en `NEXT_PUBLIC_*`
- Sortie → stockage objet (Supabase Storage / S3) + URL signee ou CDN
- Voir `rules/media-apis.md` et `docs/integrations/pipeline-images.md`

## Pour les SVG / icones

- Utiliser `lucide-react` ou `@phosphor-icons/react` en priorite
- Generation custom : `docs/integrations/quiver-svg.md` (Quiver API server-side)
- Les SVG decoratifs : `aria-hidden="true"`
