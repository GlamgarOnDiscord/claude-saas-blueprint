---
name: migrate
description: "Gère les migrations : DB, dépendances majeures, changement de lib, ou mise à jour de framework."
disable-model-invocation: true
---

## Modes

### `/migrate db [description]` — Migration de base de données

**Avant de commencer :**
```bash
# 1. Backup local obligatoire
python scripts/supabase_migrate.py --diff   # voir l'état actuel
git stash || git commit -m "chore: pre-migration checkpoint"
```

**Création et application :**
```bash
python scripts/supabase_migrate.py --new [description]   # crée le fichier migration
# Éditer le fichier créé dans supabase/migrations/
python scripts/supabase_migrate.py --env local           # appliquer en dev d'abord
```

**Checklist post-migration :**
1. Toute nouvelle table → vérifier `ENABLE ROW LEVEL SECURITY` + politiques RLS
2. `python scripts/supabase_rls_check.py` — doit retourner 0 tables sans RLS
3. Mettre à jour `core/entities/` et `core/ports/` si les types changent
4. Régénérer les types TypeScript : `pnpm supabase gen types`
5. Tests blast radius : `pnpm test -- --grep [feature]`

**Rollback :**
```bash
python scripts/supabase_migrate.py --new rollback-[description]
# Écrire le SQL inverse dans le nouveau fichier
python scripts/supabase_migrate.py --env local
```

**Règle stricte : jamais modifier une migration déjà appliquée — toujours créer une nouvelle.**

---

### `/migrate dep [package] [version]` — Mise à jour de dépendance majeure

1. Lire changelog/release notes officiel (WebSearch) — breaking changes uniquement
2. Grep les imports du package dans tout le projet
3. Appliquer les changements fichier par fichier
4. `tsc --noEmit` + tests après chaque fichier
5. Si la migration est complexe → `/deep-update` (veille changelog approfondie)
6. Documenter dans `decisions.md` si changement architecturel

---

### `/migrate lib [ancienne] → [nouvelle]` — Changement de librairie

1. Rechercher le guide de migration officiel (WebSearch)
2. Mapper les API ancienne → nouvelle (tableau de correspondance)
3. EnterPlanMode — plan fichier par fichier avant de toucher quoi que ce soit
4. Remplacer fichier par fichier, tests verts entre chaque
5. `pnpm remove [ancienne]` seulement quand 0 import restant (Grep)
6. Tests complets + `tsc --noEmit`

---

### `/migrate framework [version]` — Mise à jour de framework

1. Lire le guide de migration officiel (WebSearch) — ne pas supposer les breaking changes
2. Créer une branch dédiée : `git checkout -b migrate/[framework]-[version]`
3. Suivre le guide étape par étape — une étape = un commit
4. `tsc --noEmit` + build + tests après chaque étape
5. Si Next.js : vérifier App Router codemods disponibles (`npx @next/codemod`)
6. Créer un ADR documentant les décisions de migration
