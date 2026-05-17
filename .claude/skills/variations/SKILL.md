---
name: variations
description: "Génère N variations UI/UX d'un composant dans des fichiers séparés pour explorer visuellement les concepts. L'utilisateur ouvre son navigateur, compare, choisit, et supprime le reste."
argument-hint: "- `component` : Quel composant ou quelle page à explorer - `count` : Nombre de variations (défaut: 5, max: 10)"
---

## Arguments
- `component` : Quel composant ou quelle page à explorer
- `count` : Nombre de variations (défaut: 5, max: 10)

## Instructions

### 1. Comprendre le Composant
- Lire le composant existant (si il existe)
- Identifier les props, le data model, les contraintes
- Lire le design system en place (shadcn, tailwind config, etc.)

### 2. Planifier les Variations
Avant de coder, lister les approches UX différentes. Exemples :
- **Layout** : Cards grid vs Table vs List vs Kanban vs Timeline
- **Navigation** : Tabs vs Accordion vs Wizard vs Split view vs Sidebar
- **Interaction** : Modal vs Inline edit vs Drawer vs Full page vs Popover
- **Densité** : Compact vs Comfortable vs Spacious
- **Style** : Minimal vs Rich vs Glassmorphism vs Brutalist

Chaque variation doit être **fondamentalement différente** en approche UX, pas juste une variation de couleur.

### 3. Générer les Fichiers
Créer un dossier temporaire :
```
src/components/_variations/
├── [component]-v1-cards-grid.tsx
├── [component]-v2-table-view.tsx
├── [component]-v3-kanban.tsx
├── [component]-v4-timeline.tsx
├── [component]-v5-split-view.tsx
└── _preview.tsx  ← Page qui affiche toutes les variations
```

Le fichier `_preview.tsx` :
```tsx
// Page de preview — accéder via /variations ou route temporaire
// Affiche toutes les variations côte à côte ou en tabs
// Avec des données mock réalistes
```

### 4. Chaque Variation Doit
- Être un composant standalone fonctionnel
- Utiliser les mêmes props/données
- Avoir un titre visible indiquant le concept (ex: "V3 — Kanban Board")
- Être responsive
- Utiliser shadcn/ui et Tailwind

### 5. Présentation
Informer l'utilisateur :
```
5 variations générées dans src/components/_variations/
Ouvre [URL preview] pour les comparer visuellement.

V1 — Cards Grid : Layout classique en grille de cartes
V2 — Table View : Vue tabulaire dense avec tri et filtres
V3 — Kanban : Vue en colonnes draggable
V4 — Timeline : Vue chronologique verticale
V5 — Split View : Master-detail avec panneau latéral

Dis-moi laquelle tu préfères (ou un mix), et je supprime le reste.
```

### 6. Après le Choix
1. Copier la variation choisie vers l'emplacement final
2. Adapter les imports et le naming
3. Supprimer tout le dossier `_variations/`
4. Connecter au vrai data fetching (remplacer les mocks)
