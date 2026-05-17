# Rules: API Routes

## Obligatoire
- Toujours valider le body avec Zod AVANT d'utiliser les données
- Toujours vérifier l'auth (session) en premier
- Toujours retourner le format standardisé `{ data, error, meta }`
- Toujours gérer les erreurs avec try/catch et codes HTTP appropriés
- Toujours isoler par `organizationId` (multi-tenancy)
- Jamais d'accès DB direct dans la route — passer par un usecase

## Interdit
- Ne PAS utiliser `req.body` directement sans validation
- Ne PAS retourner des erreurs 500 génériques — toujours un message clair
- Ne PAS oublier le rate limiting sur les endpoints publics
- Ne PAS exposer des IDs internes ou des stack traces en production

## Learned
<!-- Règles ajoutées automatiquement par l'agent -->
