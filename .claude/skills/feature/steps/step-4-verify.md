# Feature — Step 4: Verify

## Objectif
Valider que tout est correct AVANT de considérer la feature comme terminée.

## Checks Automatiques (exécuter dans l'ordre)

### 1. Type Check
```bash
tsc --noEmit  # ou équivalent stack
```
Si erreur → fix immédiat, pas de skip.

### 2. Lint
```bash
npm run lint  # ou bun run lint
```
Si warning → corriger. Zero tolérance.

### 3. Tests
```bash
npm test -- --filter=[blast-radius-files]
```
Si échec → corriger le code OU le test (diagnostiquer lequel a tort).

### 4. Security Review (via sous-agent)
Lancer un agent Explore pour vérifier :
- [ ] Pas de secrets hardcodés dans les fichiers créés/modifiés
- [ ] Validation Zod sur tous les inputs utilisateur
- [ ] Auth vérifiée sur toutes les routes API
- [ ] Multi-tenancy respecté (organizationId)
- [ ] Pas de SQL injection ou d'injection HTML

### 5. Architecture Review
- [ ] `core/` n'importe RIEN depuis `adapters/`
- [ ] Chaque fichier a une seule responsabilité
- [ ] Les types sont corrects (pas de `any`)
- [ ] Les erreurs sont typées (pas de `throw new Error()` nu)

### 6. Visual Review (si UI)
- Prendre un screenshot avec l'outil approprié
- Vérifier le rendu mobile et desktop
- Vérifier les loading states et error states

## Post-Vérification
1. Mettre à jour `.claude/memory/domains.md` avec le nouveau domaine/feature
2. Mettre à jour `.claude/memory/roadmap/current-sprint.md` si task dans le sprint
3. Si une erreur a été découverte → l'ajouter dans `.claude/rules/_learned.md`
4. Informer l'utilisateur : feature terminée + résumé de ce qui a été créé
