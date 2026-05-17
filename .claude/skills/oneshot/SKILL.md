---
name: oneshot
description: "Exécution ultra-rapide pour les petites modifications. Zappe la planification. Code → Test → Done."
---

## Quand utiliser
- Changement de couleur, texte, style
- Quick fix évident (typo, import manquant, variable renommée)
- Ajout d'un champ simple à un formulaire
- Modification < 3 fichiers avec blast radius minimal

## Quand NE PAS utiliser
- Feature complète → utiliser `/feature`
- Bug complexe → utiliser `/debug`
- Plus de 3 fichiers impactés → utiliser `/feature` avec planification

## Instructions

### 1. Identifier (10 secondes)
- Quel(s) fichier(s) modifier ?
- Y a-t-il un risque ? Si oui → basculer vers `/feature`
- Charger la rule contextuelle correspondante (`.claude/rules/`)

### 2. Exécuter (immédiat)
- Appliquer la modification directement avec Edit
- Pas de plan, pas d'EnterPlanMode, pas de sous-agents
- Un seul diff ciblé

### 3. Valider (rapide)
- `tsc --noEmit` uniquement
- Si UI modifiée → un screenshot rapide
- Pas de tests complets — seulement si le fichier modifié a un test existant

### 4. Done
- Informer l'utilisateur en 1 ligne : « Fait. [description du changement]. »
- Ne PAS mettre à jour la memory/roadmap pour les oneshots

## Note
- Si le changement touche auth, paiement ou schéma DB → ce n’est **pas** un oneshot ; utiliser `/feature` ou `/apex`.
