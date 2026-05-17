# Rules: APIs média (images, SVG, audio)

## Obligatoire
- Appels **serveur uniquement** (API route, worker). Voir `docs/integrations/pipeline-images.md`, `quiver-svg.md`, `audio-voice.md`.
- Sorties → **stockage objet** + URL signée / CDN ; pas de clés en client pour APIs payantes.

## Interdit
- `NEXT_PUBLIC_*` pour `QUIVERAI_*`, `GOOGLE_API_KEY`, `ELEVENLABS_*`, etc.
- Clés commitées ; seulement noms dans `.env.example`.
