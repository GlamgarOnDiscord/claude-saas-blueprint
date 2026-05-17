---
name: api-gen
description: "Génère un endpoint API complet avec validation, auth, error handling et tests."
argument-hint: "- `resource` : Nom de la ressource (ex: "invoices", "projects") - `operations` : CRUD complet par défaut, ou spécifier ("
---

## Arguments
- `resource` : Nom de la ressource (ex: "invoices", "projects")
- `operations` : CRUD complet par défaut, ou spécifier (ex: "create,read,list")

## Instructions

### 1. Analyse
- Lire `rules/api-routes.md` + `rules/security.md` avant toute modification
- Lire le schema DB pour la ressource (si existant)
- Identifier le pattern API utilisé dans le projet (REST, tRPC, GraphQL)
- Lire un endpoint existant comme référence de style

### 2. Génération
Pour chaque opération demandée, créer :

**Validation (Zod)** dans `shared/validators/` :
- Schema de création (tous les champs requis)
- Schema de mise à jour (tous les champs optionnels via `.partial()`)
- Schema de query params (pagination, filtres, tri)

**Use Case** dans `core/usecases/` :
- Un fichier par opération : `create-{resource}.ts`, `list-{resources}.ts`, etc.
- Injection du port repository via paramètre
- Vérification d'autorisation intégrée

**Route/Controller** dans `adapters/api/` :
- Middleware d'auth appliqué
- Validation du body/params/query avec le schema Zod
- Réponse standardisée : `{ data, error, meta: { page, total } }`
- Gestion d'erreur avec codes HTTP appropriés

**Tests** :
- Test unitaire par use case
- Test d'intégration par route (si framework de test dispo)

### 3. Validation
- `tsc --noEmit`
- Exécuter les tests générés
- Vérifier qu'il n'y a pas de routes dupliquées
