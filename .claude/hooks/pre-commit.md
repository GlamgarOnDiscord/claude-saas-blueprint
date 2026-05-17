# Pre-Commit Hook Instructions

## Checks automatiques avant chaque commit
Ces vérifications doivent être exécutées par l'agent avant de créer un commit :

1. **Type Check** : `tsc --noEmit` (si TypeScript)
2. **Lint** : `npm run lint` (si configuré)
3. **No Secrets** : Vérifier qu'aucun `.env`, clé API ou mot de passe n'est staged
4. **No Debug** : Pas de `console.log` dans les fichiers staged (sauf logger)
5. **Tests Blast Radius** : Exécuter les tests des fichiers modifiés uniquement
6. **Max File Size** : Alerter si un fichier staged > 300 lignes

## En cas d'échec
- Corriger automatiquement si possible (1 tentative)
- Sinon, informer l'utilisateur avec le détail de l'erreur
- Ne JAMAIS utiliser `--no-verify` pour contourner
