---
name: schema-gen
description: "Génère un schéma de base de données complet avec migrations, types et repository de base."
argument-hint: "- `entity` : Nom de l'entité (ex: "Invoice", "Project") - `fields` : Description des champs en langage naturel"
---

## Arguments
- `entity` : Nom de l'entité (ex: "Invoice", "Project")
- `fields` : Description des champs en langage naturel

## Instructions

### 1. Détection ORM
Lire `.claude/memory/stack.md` ou détecter :
- `drizzle.config.ts` → Drizzle ORM
- `schema.prisma` → Prisma
- `alembic/` → SQLAlchemy
- Sinon → demander à l'utilisateur

### 2. Génération du Schema
Créer le fichier de schema avec :
- Tous les champs demandés avec types appropriés
- `id` : UUID v7 par défaut (ordonné chronologiquement)
- `organizationId` : FK pour multi-tenancy (sauf si explicitement exclu)
- `createdAt` : timestamp, default now
- `updatedAt` : timestamp, auto-update
- `deletedAt` : timestamp nullable (soft delete)
- Index sur les FK et champs fréquemment recherchés
- Relations définies explicitement

### 3. Fichiers Générés
1. **Schema/Migration** : Dans le dossier de l'ORM
2. **Entity type** dans `core/entities/{entity}.ts` :
   - Type TypeScript pur (pas d'import ORM)
   - Validation via Zod schema
3. **Port** dans `core/ports/i-{entity}-repo.ts` :
   - Interface du repository avec CRUD de base
4. **Adapter** dans `adapters/db/{entity}-repo.ts` :
   - Implémentation du port avec l'ORM choisi
   - Inclut soft delete, pagination, filtres de base

### 4. Validation
- Générer et exécuter la migration
- `tsc --noEmit`
- Mettre à jour `.claude/memory/domains.md`
