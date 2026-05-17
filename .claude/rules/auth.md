# Rules: Auth & Sécurité

## Obligatoire
- Toujours séparer authentication (qui?) de authorization (quoi?)
- Toujours vérifier les permissions AVANT l'action, pas après
- Toujours hasher les mots de passe (bcrypt/argon2), JAMAIS en clair
- Toujours utiliser des tokens HTTP-only secure pour les sessions web
- Toujours valider les tokens côté serveur, jamais côté client uniquement

## Interdit
- Ne PAS stocker de secrets dans le code source ou les variables client
- Ne PAS utiliser JWT pour les sessions (sauf API stateless) — préférer les sessions DB
- Ne PAS oublier CSRF protection sur les formulaires
- Ne PAS logger les tokens, mots de passe ou données sensibles

## Learned
<!-- Règles ajoutées automatiquement par l'agent -->
