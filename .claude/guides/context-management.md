# Stratégies de Context Management

## Problème
Le contexte Claude a une limite. Sur un gros projet (100+ fichiers), il est impossible de tout lire. Il faut être stratégique.

## Stratégie 1 — Lecture en Entonnoir
```
1. Glob → Lister la structure (noms de fichiers uniquement)
2. Read → Lire uniquement les fichiers interfaces/types (contrats)
3. Read → Lire le(s) fichier(s) à modifier
4. Grep → Chercher les usages avant de modifier
```
Ne JAMAIS lire tout le projet. Toujours commencer par la structure.

## Stratégie 2 — Délégation aux Sous-Agents
Pour les recherches larges, utiliser des agents Explore qui :
- Parcourent le codebase dans leur propre contexte
- Retournent un résumé synthétique
- Ne polluent pas le contexte principal

## Stratégie 3 — Memory comme Cache
Sauver les découvertes durables dans `.claude/memory/` :
- `patterns.md` → Patterns de code récurrents
- `domains.md` → Map des domaines et entités
- `stack.md` → Stack complète avec versions

Au lieu de relire, vérifier d'abord la memory.

## Stratégie 4 — Compaction Proactive
Quand la conversation dépasse ~80k tokens :
1. Synthétiser l'état actuel dans `session.md`
2. Lister les fichiers modifiés et les changements faits
3. Documenter ce qui reste à faire
→ Le système compactera automatiquement l'historique

## Stratégie 5 — Index de Navigation
Maintenir dans `project-scan.md` un index navigable :
```
## Fichiers Clés
- Config DB → src/lib/db.ts
- Config Auth → src/lib/auth.ts
- Types partagés → src/shared/types.ts
- Routes API → app/api/
- Composants UI → src/components/ui/
```
Cet index permet de sauter directement au bon fichier sans scanner.

## Anti-Patterns
- Lire tous les fichiers d'un dossier "au cas où"
- Relire un fichier déjà lu dans la même session
- Garder de longs outputs de commande dans le contexte
- Ne pas synthétiser les résultats d'agents avant de continuer
