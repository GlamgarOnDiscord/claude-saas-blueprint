# Techniques de Debugging Avancées

## Technique 1 — Visual Feedback (UI)
Quand l'IA travaille sur du frontend, elle n'a pas d'yeux par défaut.

### Donner des yeux à l'agent
1. **Screenshots** : Après chaque modification UI, utiliser l'outil de screenshot
   - Prendre un screenshot de la page/composant modifié
   - Comparer visuellement avec l'attendu
   - Détecter les bugs visuels (overflow, alignement, couleurs)

2. **Maquettes comme input** : Si l'utilisateur fournit une maquette/screenshot
   - L'analyser via Read (si fichier image)
   - Identifier les composants, couleurs, espacements
   - Implémenter pixel-perfect en s'y référant

3. **Comparaison avant/après** : Pour les refactorings UI
   - Screenshot AVANT modification
   - Modifier le code
   - Screenshot APRÈS modification
   - Vérifier qu'il n'y a pas de régression visuelle

## Technique 2 — Log Technique (Backend)
Quand l'agent tourne en rond sur un bug backend (2+ tentatives échouées).

### Protocole
1. **Injecter des logs** : Ajouter des `console.log` stratégiques aux points clés :
   ```typescript
   console.log('[DEBUG] Input:', JSON.stringify(input));
   console.log('[DEBUG] DB result:', JSON.stringify(result));
   console.log('[DEBUG] Auth session:', JSON.stringify(session));
   ```
2. **Demander à l'utilisateur** d'exécuter l'action qui cause le bug
3. **Récupérer les logs** : L'utilisateur copie-colle les logs dans le chat
4. **Analyser** : Avec les données réelles, identifier exactement où ça coince
5. **Nettoyer** : Supprimer TOUS les `console.log` de debug après le fix

### Quand utiliser
- L'erreur dépend de données runtime que l'agent ne peut pas voir
- Le bug n'apparaît qu'avec certains inputs spécifiques
- L'agent a essayé 2 fixes sans succès

## Technique 3 — Bisect Logique
Pour les régressions : "ça marchait avant, maintenant non".

### Protocole
1. `git log --oneline -20` — voir les commits récents
2. Identifier le commit suspect
3. `git diff [commit]..HEAD -- [fichiers suspects]` — voir ce qui a changé
4. Analyser le diff pour trouver le changement qui casse

## Technique 4 — Isolation par Simplification
Quand un bug est trop complexe à comprendre.

### Protocole
1. Créer une version minimale du code qui reproduit le bug
2. Retirer les couches une par une (auth, validation, middleware)
3. Identifier quelle couche cause le problème
4. Fix la couche isolée, puis réintégrer

## Anti-Patterns de Debug
- **Shotgun debugging** — Changer plein de trucs au hasard en espérant que ça marche
- **Boucle infinie** — Réessayer la même approche > 2 fois
- **Fix le symptôme** — Ajouter un `if` pour masquer le bug au lieu de le corriger
- **Ignorer les types** — Si TypeScript dit qu'il y a un problème, il a raison
