# Post-Edit Hook Instructions

## Après chaque modification de fichier
1. Vérifier la cohérence des imports (pas d'imports cassés)
2. Si le fichier modifié est dans `core/` : vérifier qu'il n'importe PAS depuis `adapters/`
3. Si c'est un schema DB : rappeler de générer la migration
4. Mettre à jour `.claude/memory/session.md` avec le fichier modifié
