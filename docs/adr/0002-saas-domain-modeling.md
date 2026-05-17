# ADR 0002: Modélisation par Domaine (DDD)

## État
Accepté

## Date
2026-03-13

## Contexte
Les SaaS ont tendance à devenir monolithiques et difficiles à maintenir au fil du temps. Une séparation claire des responsabilités est nécessaire dès le premier jour.

## Décision
Nous adoptons une structure de **Domain Driven Design (DDD)** simplifiée :
1.  **Core Domain** : Contient uniquement la logique métier pure (Entités, Value Objects, Services de domaine). Indépendant de tout framework.
2.  **Application Layer** : Orchestre les cas d'utilisation (Services d'application, Commandes, Requêtes).
3.  **Infrastructure/Adapters** : Implémentations concrètes (Base de données, API, Mailers, Stripe).
4.  **Shared Kernel** : Types partagés et utilitaires transverses.

## Conséquences
- Testabilité accrue du coeur métier sans dépendance externe.
- Facilité de remplacement d'un adaptateur (ex: passer de Supabase à AWS RDS).
- Courbe d'apprentissage initiale légèrement plus élevée pour les nouveaux agents.
