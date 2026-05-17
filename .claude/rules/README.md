# Rules System — Règles Contextuelles

Pour le **cadre global** (ne pas surcharger le contexte) : `docs/workflow-pragmatique.md`.

## Concept
Les rules sont des micro-instructions qui s'activent **uniquement quand l'agent travaille sur un certain type de fichier ou domaine**. Elles ne polluent pas le contexte global.

## Comment ça marche
1. L'agent détecte le type de fichier qu'il va modifier
2. Il charge les rules associées à ce type
3. Les rules sont injectées dans le contexte juste avant l'action
4. Après l'action, les rules ne sont plus dans le contexte

## Chargement conditionnel avec `paths:`

Les rules peuvent inclure un frontmatter YAML avec un champ `paths:` pour s'activer automatiquement :

```yaml
---
paths:
  - "src/api/**/*.ts"
  - "app/api/**"
---
# Rules: API Routes
...
```

Quand l'agent modifie un fichier qui matche un des patterns glob, la rule est chargée automatiquement sans intervention manuelle.

## Niveaux de rules

Les rules existent à **3 niveaux** (du plus spécifique au plus général) :

| Niveau | Emplacement | Portée |
|--------|-------------|--------|
| **Projet** | `.claude/rules/*.md` | Ce dépôt uniquement |
| **Utilisateur** | `~/.claude/rules/*.md` | Tous les projets de l'utilisateur |
| **Symlink** | Lien symbolique vers un dossier partagé | Multi-projets |

Les rules projet ont priorité sur les rules utilisateur en cas de conflit.

## Structure
```
rules/
├── README.md              # Ce fichier
├── api-routes.md          # Quand on touche à des routes API
├── db-schema.md           # Quand on touche au schéma DB
├── auth.md                # Quand on touche à l'auth
├── ui-components.md       # Quand on touche aux composants UI
├── tests.md               # Quand on écrit/modifie des tests
├── config.md              # Quand on touche à la configuration
├── media-apis.md          # Génération images/SVG/audio (clés serveur, stockage)
├── security.md            # Sécurité — OBLIGATOIRE sur tout endpoint public
└── _learned.md            # Règles apprises par l'agent au fil du temps
```

## Convention de Nommage
- Nom du fichier = domaine/contexte d'activation
- Contenu = liste de règles courtes et actionables
- Max 20 lignes par fichier (rester concis pour ne pas polluer le contexte)

## Quand l'Agent Apprend une Nouvelle Règle
Si l'agent fait une erreur ou découvre une spécificité du projet :
1. Corriger l'erreur
2. Ajouter la règle dans le fichier approprié (ou `_learned.md` si pas de catégorie)
3. Format : `- [DATE] NE PAS / TOUJOURS + action + raison`

## Activation
L'agent DOIT lire la rule correspondante avant de modifier un fichier dans ces contextes :
- Fichier dans `app/api/` ou `adapters/api/` → lire `rules/api-routes.md`
- Fichier dans `adapters/db/` ou migration → lire `rules/db-schema.md`
- Fichier dans `adapters/auth/` ou middleware auth → lire `rules/auth.md`
- Fichier dans `components/` → lire `rules/ui-components.md`
- Fichier `*.test.*` ou `*.spec.*` → lire `rules/tests.md`
- Fichier dans `config/` ou `.env*` → lire `rules/config.md`
- Route ou service qui appelle **Quiver / Gemini / ElevenLabs / génération d'assets** → lire `rules/media-apis.md`
- Tout endpoint public, middleware auth, ou avant un déploiement → lire `rules/security.md`
