# Visual Context — Donner des Yeux à l'Agent

## Principe
L'IA comprend les images. Un screenshot annoté vaut 1000 mots de prompt.

## Technique 1 — Screenshot Annoté (style Cleanshot X)
Quand l'utilisateur envoie un screenshot avec des annotations (carrés rouges, flèches, texte) :
1. **Analyser l'image** — Identifier les zones annotées
2. **Comprendre le problème** — L'annotation pointe exactement le bug/problème
3. **Localiser dans le code** — Trouver le composant correspondant
4. **Corriger** — Le contexte visuel est suffisant, pas besoin de long prompt

### Pour l'utilisateur
- Utiliser n'importe quel outil de capture (Cleanshot X, Snagit, outil Windows)
- Dessiner un carré rouge autour du problème
- Ajouter une flèche si nécessaire
- Coller directement dans le chat Claude Code

## Technique 2 — React Grab (MCP)
Si configuré, l'outil React Grab permet de :
1. Cliquer sur un élément directement dans le navigateur
2. Récupérer le code source exact du composant
3. L'injecter dans le contexte avec les styles computés
→ Plus besoin de chercher quel fichier correspond à quel élément

## Technique 3 — Comparaison Maquette vs Réalité
Quand l'utilisateur fournit une maquette (Figma export, screenshot, etc.) :
1. Analyser la maquette (couleurs, espacements, typographie, layout)
2. Comparer avec l'implémentation actuelle
3. Lister les différences pixel par pixel
4. Corriger jusqu'à correspondance

## Technique 4 — Screenshot Review Automatique
Après chaque modification UI :
1. Prendre un screenshot du composant modifié
2. Vérifier visuellement :
   - Alignement correct ?
   - Pas d'overflow ou de clip ?
   - Responsive (vérifier les breakpoints) ?
   - Loading/error states cohérents ?
3. Si problème détecté → corriger automatiquement

## Technique 5 — 10 Variations
Voir `/variations` — Générer N variations visuelles dans des fichiers séparés pour explorer les concepts UX.

## Outils Recommandés

### Screenshots & Annotations
- **Cleanshot X** (macOS) — Capture + annotation en 1 clic
- **ShareX** (Windows) — Equivalent gratuit
- **Outil intégré VS Code** — Copier depuis le terminal

### MCP pour le Visual
- **React Grab** — Sélection d'éléments dans le navigateur
- **Kombai** — Review UI/UX avec analyse humaine
- **Pencil** — Design dans le canvas intégré

### Auto-Review
- **React Doctor** — Scan automatique des anti-patterns React
- Toujours lancer après des modifications UI significatives
