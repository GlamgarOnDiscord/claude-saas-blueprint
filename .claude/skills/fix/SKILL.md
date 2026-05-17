---
name: fix
description: "Quick fix — plus rapide que `/debug`, plus structuré que `/oneshot`. Pour les bugs simples avec une cause évidente."
---

## Quand utiliser
- Message d'erreur clair avec fichier et ligne
- Bug de régression après un changement récent
- Erreur TypeScript ou lint à corriger
- Import cassé, variable undefined, prop manquante

## Quand NE PAS utiliser
- Bug sans message d'erreur clair → `/debug`
- Bug qui nécessite de comprendre le flux complet → `/debug`
- Simple changement cosmétique → `/oneshot`

## Instructions

### 1. Comprendre (30 secondes)
- Lire le message d'erreur
- Identifier le fichier et la ligne
- Lire le fichier concerné

### 2. Fix (immédiat)
- Appliquer la correction minimale
- Ne PAS refactorer le code autour — juste le fix

### 3. Vérifier
- `tsc --noEmit`
- Exécuter le test du fichier modifié (s'il existe)
- Si le fix est dans un pattern qui pourrait se répéter → ajouter dans `rules/_learned.md`

### 4. Done
- « Fix appliqué : [description en 1 ligne] »

## Note
- Style / format : laisser **ESLint, Prettier, Biome** ou les **hooks** (`.claude/settings.json`) faire le travail — pas de réécriture « cosmétique » via l’agent sauf demande explicite.
