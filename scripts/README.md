# Scripts Python — claude-saas-blueprint

Scripts autonomes pour automatiser les tâches répétitives.
**Objectif** : remplacer les longues chaînes de commandes shell qui gaspillent des tokens.

## Usage rapide

```bash
# Santé globale du projet
python scripts/project_health.py

# Avant chaque déploiement
python scripts/pre_deploy_check.py --env staging
python scripts/pre_deploy_check.py --env production

# Migrations Supabase
python scripts/supabase_migrate.py --new nom-de-la-migration
python scripts/supabase_migrate.py --diff
python scripts/supabase_migrate.py --env local
python scripts/supabase_migrate.py --env staging
python scripts/supabase_migrate.py --env production

# Sécurité RLS
python scripts/supabase_rls_check.py
python scripts/supabase_rls_check.py --fix     # génère une migration correctrice

# Scan secrets (avant commit)
python scripts/scan_secrets.py
python scripts/scan_secrets.py --staged-only   # uniquement les fichiers staged
python scripts/scan_secrets.py --json          # output JSON pour CI

# Intégrité du workflow
python scripts/verify-workflow-integrity.py

# Memory rotate (archive ancien, déduplique _learned)
python scripts/memory-rotate.py --dry-run        # voir ce qui serait fait
python scripts/memory-rotate.py --days 90        # archive les sections > 90 jours

# RTK — Rust Token Killer (réduction tokens 60-90%)
python scripts/rtk_setup.py            # check + guide installation
python scripts/rtk_setup.py --check    # statut uniquement
python scripts/rtk_setup.py --stats    # économies de tokens
python scripts/rtk_setup.py --install  # guide d'installation détaillé
```

## Scripts disponibles

| Script | Rôle | Tokens économisés |
|--------|------|-------------------|
| `project_health.py` | Dashboard santé : TS, lint, tests, sécurité, structure | ~500/run |
| `pre_deploy_check.py` | 8 checks obligatoires avant deploy | ~800/run |
| `supabase_migrate.py` | Wrapper migrations Supabase (filtre output verbeux) | ~300/run |
| `supabase_rls_check.py` | Audit RLS sur toutes les tables | ~200/run |
| `scan_secrets.py` | Détection secrets/clés API dans le code | ~400/run |
| `verify-workflow-integrity.py` | Vérification cohérence du workflow AI | ~200/run |
| `memory-rotate.py` | Rotation memory : archive sections > N jours, déduplique `_learned.md` | — |
| `rtk_setup.py` | Installation/config RTK token optimizer | — |

## Intégration Claude Code

Ces scripts sont conçus pour être appelés par l'agent IA à la place de chaînes de commandes :

**Avant** (gaspillage tokens) :
```
→ tsc --noEmit          # 500 lignes d'output
→ npm run lint          # 300 lignes d'output
→ npm test              # 1000 lignes d'output
→ git status            # verbeux
→ grep -r "console.log" # 200 matches
```

**Après** (avec scripts) :
```
→ python scripts/project_health.py  # 20 lignes résumées, exit code clair
```

## Conventions

- Tous les scripts retournent `exit 0` si OK, `exit 1` si problème
- Output minimal et structuré — pas de verbosité inutile
- Paramètre `--json` disponible sur les scripts utilisés en CI
- Compatible Python 3.9+, aucune dépendance externe (stdlib uniquement)
