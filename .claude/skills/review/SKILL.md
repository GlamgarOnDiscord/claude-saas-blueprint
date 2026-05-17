---
name: review
description: "Code review automatique des changements récents. 3 agents parallèles + scan secrets + vérification architecture hexagonale."
---

## Instructions

### 1. Identifier les changements

```bash
git diff --name-only HEAD~1   # derniers fichiers modifiés
```
Si pas de git → demander quels fichiers reviewer.

### 2. Scan secrets (obligatoire en premier)

```bash
python scripts/scan_secrets.py --staged-only
```
Si exit 1 → **bloquer la review, corriger avant tout**.

### 3. Review automatique (3 agents en parallèle)

**Agent 1 — Clean Code (Explore)**
```
Lire [fichiers modifiés] et vérifier :
- Fichiers > 200 lignes ?
- Fonctions > 50 lignes ?
- Duplication de code ?
- `any` utilisé ?
- `console.log` oublié ?
- Imports inutilisés ?
Retourner UNIQUEMENT les problèmes trouvés, pas les OK.
```

**Agent 2 — Sécurité (Explore)**
```
Lire [fichiers modifiés] et vérifier :
- Inputs validés avec Zod AVANT usage ?
- Auth + organizationId vérifiés sur chaque route ?
- Pas de secrets hardcodés ?
- Rate limiting présent sur les endpoints publics ?
- Headers sécurité en place (CSP, X-Frame-Options) ?
- SQL/HTML injection possible ?
Référence : .claude/rules/security.md
Retourner UNIQUEMENT les vulnérabilités trouvées.
```

**Agent 3 — Architecture (Explore)**
```
Lire [fichiers modifiés] et vérifier :
- core/ importe-t-il depuis adapters/ ? (violation hexagonale)
- Les types sont cohérents avec core/entities/ ?
- Les usecases retournent des types typés, pas des objets bruts ?
- Pas d'accès DB direct dans les routes (passer par usecase) ?
- Conventions respectées : kebab-case fichiers, PascalCase types ?
Retourner UNIQUEMENT les violations trouvées.
```

### 4. Rapport

```markdown
## Code Review — [date] — [branche]

### Fichiers reviewés
[liste]

### Secrets
✓ Aucun secret détecté  |  ✗ [problèmes]

### Problèmes trouvés
- [CRITICAL] ...
- [WARNING] ...
- [SUGGESTION] ...

### Verdict
APPROVE | CHANGES_REQUESTED

Score sécurité : x/5
```

### 5. Auto-fix

Proposer de corriger automatiquement : imports inutilisés, `console.log`, nommage évident.
Pour les problèmes architecturaux → utiliser `/refactor`.
