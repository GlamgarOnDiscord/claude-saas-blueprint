# QuiverAI — SVG (génération & vectorisation)

Documentation officielle : [Introduction API](https://docs.quiver.ai/api-reference/introduction) · index LLMs : [docs.quiver.ai/llms.txt](https://docs.quiver.ai/llms.txt).

## Variables d’environnement

```bash
QUIVERAI_API_KEY=
```

- Charger **uniquement côté serveur** (voir rule `.claude/rules/media-apis.md`).
- Ne jamais préfixer en `NEXT_PUBLIC_`.

## Requêtes

- **Base URL** : `https://api.quiver.ai/v1`
- **Auth** : `Authorization: Bearer <QUIVERAI_API_KEY>`
- **JSON** : `Content-Type: application/json`

Endpoints courants (voir doc à jour pour le corps exact) :

- `GET /v1/models` / `GET /v1/models/{model}`
- `POST /v1/svgs/generations`
- `POST /v1/svgs/vectorizations`

## SDK Node

```bash
npm install @quiverai/sdk
```

Repo : [github.com/quiverai/quiverai-node](https://github.com/quiverai/quiverai-node).

## Crédits & limites

- Consommation de **crédits** et **rate limits** (ex. `429`, en-têtes `X-RateLimit-*`) : se référer à la [doc Introduction](https://docs.quiver.ai/api-reference/introduction).
- Implémenter **retry avec backoff** sur les erreurs réseau / 429.

## Retour au pipeline global

→ [`assets-pipeline.md`](./assets-pipeline.md) · skill **`/assets-pipeline`**
