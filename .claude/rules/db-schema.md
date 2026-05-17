# Rules: DB Schema & Migrations

## Obligatoire
- Toujours ajouter `createdAt`, `updatedAt`, `deletedAt` sur chaque table
- Toujours ajouter `organizationId` pour le multi-tenancy (sauf tables système)
- Toujours créer un index sur les FK et les champs de recherche fréquents
- Toujours générer la migration après modification du schema
- Toujours utiliser UUID v7 (ordonné chronologiquement) pour les IDs
- Mettre à jour `core/entities/` et `core/ports/` après changement de schema

## Interdit
- Ne PAS modifier une migration déjà appliquée — en créer une nouvelle
- Ne PAS utiliser de hard delete — toujours soft delete (`deletedAt`)
- Ne PAS oublier les contraintes de FK (ON DELETE)
- Ne PAS créer de colonnes `TEXT` sans limite raisonnable

## Learned
<!-- Règles ajoutées automatiquement par l'agent -->
