---
name: ui-audit
description: "Audit UX/UI read-only — WCAG 2.2 AA, heuristiques Nielsen, anti-slop. Aucun changement de code, rapport file:line."
argument-hint: "[target-file-or-directory]"
---

# UI Audit — Read-only

## Role
Auditeur UX senior. Ce skill **ne modifie jamais le code** — il produit un rapport prioritise.

## Ce que fait ce skill
- Audit conformite **WCAG 2.2 AA** (contraste, semantique, ARIA, focus, target size, reduced motion)
- Evaluation des **10 heuristiques de Nielsen**
- Detection des patterns **anti-slop** (UI generique generee par IA)
- Verification des etats : loading / empty / error / success
- Rapport `file:line` avec severite

## Ce que ce skill NE fait PAS
- Modifier du code
- Generer de la nouvelle UI
- Proposer des implementations specifiques (uniquement le probleme et l'outcome attendu)

## Process

### 1. Scan
Lire le ou les fichiers cibles. Si l'utilisateur ne precise rien, demander quel scope auditer.

### 2. WCAG 2.2 AA
- Contraste : ratio body >= 4.5:1, large text >= 3:1, UI components >= 3:1
- HTML semantique : `<main>`, `<nav>`, `<section aria-label>`, headings hierarchiques
- Focus visible sur tous les elements interactifs (`focus-visible:ring`)
- Target size minimum 24x24px (44x44 ideal mobile)
- `prefers-reduced-motion` respecte sur les animations
- Images : `alt` non vide pour les images informatives, `alt=""` pour decoratives
- Formulaires : `<label>` lie a chaque input

### 3. Heuristiques Nielsen
1. Visibilite du statut systeme (loading, succes, erreur)
2. Correspondance avec le monde reel (vocabulaire utilisateur)
3. Controle et liberte utilisateur (back, undo, cancel)
4. Coherence et standards
5. Prevention des erreurs (validation avant submit)
6. Reconnaissance plutot que rappel
7. Flexibilite et efficacite (raccourcis pour power users)
8. Design minimaliste
9. Aide a reconnaitre, diagnostiquer, recuperer (messages d'erreur)
10. Aide et documentation contextuelle

### 4. Anti-slop
- Hero centre avec 3 cards egales
- Inter / Roboto / Arial / Space Grotesk
- Numeros ronds (`50%`, `1000+`)
- Gradient de fond purple-blue
- Spinner au lieu de Skeleton
- shadcn par defaut sans customisation
- Glassmorphism sur tout
- Emojis dans le code

### 5. Etats manquants
Pour chaque composant interactif, verifier :
- [ ] Loading state (Skeleton)
- [ ] Empty state (avec CTA pour creer le premier element)
- [ ] Error state (message clair + action de retry)
- [ ] Success state si applicable

## Format du rapport

```markdown
## UI Audit Report — [date]

### Summary
- WCAG AA violations : X
- Anti-slop patterns : X
- Missing states : X
- Nielsen concerns : X

### Critical (must fix avant ship)
- `path/file.tsx:42` — [WCAG 1.4.3] Contrast 2.1:1 sur body text (need 4.5:1)
- `path/file.tsx:87` — [Nielsen #1] Pas de loading state sur fetch async

### Warning (should fix)
- `path/file.tsx:15` — [anti-slop] Hero centre avec 3 cards egales
- `path/file.tsx:103` — [WCAG 2.4.7] Pas de focus visible sur le bouton

### Info (nice to fix)
- `path/file.tsx:200` — [Nielsen #1] Loading repose sur spinner ; preferer Skeleton sans CLS
- `path/file.tsx:220` — [Nielsen #7] Pas de raccourci clavier pour les power users

### Score
- WCAG : X/10
- UX : X/10
- Anti-slop : X/10
```

## References
- `platforms/web-app.md` — patterns web
- `rules/ui-components.md` — regles UI projet
- WCAG 2.2 quick reference : https://www.w3.org/WAI/WCAG22/quickref/
