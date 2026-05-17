# Rules: Configuration

## Obligatoire
- Toute config sensible dans `.env`, jamais dans le code
- Toujours documenter les variables dans `.env.example`
- Valider les variables d'environnement au démarrage (Zod ou t3-env)
- Séparer les configs par environnement (dev, staging, production)

## Interdit
- Ne PAS committer `.env` ou `.env.local` — uniquement `.env.example`
- Ne PAS utiliser de valeurs par défaut pour les secrets (DB URL, API keys)
- Ne PAS mélanger config runtime et config build

## Learned
<!-- Règles ajoutées automatiquement par l'agent -->
