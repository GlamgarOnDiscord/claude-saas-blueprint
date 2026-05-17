# Audio & voix (ex. ElevenLabs)

Pour **TTS**, **voiceover**, **avatars audio** dans un SaaS : même discipline que les images — **clés et appels côté serveur** (voir `.claude/rules/media-apis.md`).

## ElevenLabs (exemple courant)

- Création de clés et billing : [elevenlabs.io](https://elevenlabs.io/) (compte développeur).
- **Ne pas** exposer la clé API au client pour génération à la demande facturée.
- Prévoir **stockage** des fichiers audio générés (objet + URL) et **droits** (voix clonées = contrats spécifiques).

```bash
ELEVENLABS_API_KEY=
```

## Alternatives (selon besoin)

- **OpenAI TTS** / **Google Cloud Text-to-Speech** — choisir une seule stack par produit pour limiter la complexité.
- **Whisper** (transcription) côté serveur si besoin — pas de clé dans le front.

## Intégration produit

- Routes dédiées `POST /api/.../speech` ou workers pour jobs longs.
- Quotas par `organizationId` si multi-tenant.

→ [`assets-pipeline.md`](./assets-pipeline.md)
