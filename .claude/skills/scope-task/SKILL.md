---
name: scope-task
description: "Pour UNE tâche décrite, liste quelles rules, skills et docs ouvrir — progressive disclosure, anti-surcharge contexte."
argument-hint: "[description de la tâche]"
disable-model-invocation: true
---

# Scope Task — Charger le bon contexte

Objectif : éviter d'empiler rules, skills et fichiers inutiles.

## Entrée
Une phrase décrivant la tâche (ex. « ajouter endpoint factures », « corriger bug login »).

## Mapping automatique rules → domaine

| Mots-clés dans la tâche | Rules à charger |
|------------------------|-----------------|
| endpoint, route, API, handler | `api-routes.md` + `security.md` |
| schema, migration, table, colonne | `db-schema.md` |
| login, auth, session, token, permission | `auth.md` + `security.md` |
| composant, page, UI, form, button | `ui-components.md` |
| test, spec, vitest, playwright | `tests.md` |
| .env, config, variable, secret | `config.md` + `security.md` |
| image, SVG, audio, vidéo, asset | `media-apis.md` |
| deploy, prod, staging, vercel | `security.md` |

## Mapping automatique skill → complexité

| Complexité | Critère | Skill |
|------------|---------|-------|
| Trivial | 1 fichier, bug évident | `/fix` ou `/oneshot` |
| Simple | 2-3 fichiers, feature claire | `/api-gen` / `/ui gen` / `/schema-gen` |
| Moyen | 4-8 fichiers, plusieurs couches | `/feature` |
| Lourd | >8 fichiers ou architecture | `/feature` + EnterPlanMode |

## Sortie (format fixe)

```markdown
## Tâche
[reformulation courte — 1 ligne]

## Contexte minimal
- **Rules** : [fichiers à charger selon mapping ci-dessus]
- **Skill principal** : [1 seul skill]
- **Fichiers à lire en premier** : [chemins ou patterns]

## À ne PAS charger
[rules hors sujet, skills lourds inutiles — liste explicite]

## Prochaine commande
`/[skill] [args]` — [1 ligne de justification]
```

## Règles
- **1 skill principal** sauf orchestration explicite (`/prd exec`).
- Préférer `file:line` pointers plutôt que coller du code dans le chat.
- Si doute entre `/fix` et `/feature` → `/fix` d'abord (plus rapide, fail-safe).
- Charger les rules **avant** de modifier le premier fichier, pas après.
