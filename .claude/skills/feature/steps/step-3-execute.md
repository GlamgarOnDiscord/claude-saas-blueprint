# Feature — Step 3: Execute

## Objectif
Implémenter le plan étape par étape, de manière atomique.

## Règles d'Exécution

### Ordre strict
1. **Core d'abord** — entities, validators, ports, usecases
   - Zéro import depuis `adapters/`
   - Types purs, logique testable
2. **Adapters ensuite** — DB, API, auth
   - Lire la rule contextuelle AVANT de modifier (`.claude/rules/`)
   - Vérifier `tsc --noEmit` après chaque fichier d'adapter
3. **UI en dernier** — composants, pages
   - Server Components par défaut
   - Réutiliser shadcn/ui avant de créer

### Discipline de code
- **Un fichier à la fois** — ne pas tout modifier en parallèle
- **Vérifier les imports** après chaque fichier créé
- **Respecter les templates** dans `templates/` (entity, port, usecase, api-route)
- **Max 200 lignes** par fichier — split si nécessaire
- **Pas de raccourcis** — pas de `any`, pas de `console.log`, pas d'erreurs non typées

### Utilisation des sous-agents (paralléliser si indépendant)
- Agent `test-automator` → générer les tests en parallèle du code
- Agent `websearch` → chercher de la doc si bloqué sur une API
- Ne PAS utiliser de sous-agent pour écrire le code core — le faire soi-même

## Transition
→ Passer à `step-4-verify.md`
