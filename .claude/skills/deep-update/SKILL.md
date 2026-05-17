---
name: deep-update
description: "Mise à jour profonde d’une lib, framework ou API : recherche changelog officiel, breaking changes, puis migration clean — pas un simple npm update."
argument-hint: "[cible : ex. next@15, stripe SDK, API interne v2]"
disable-model-invocation: true
---

# Deep update — mise à jour profonde

## Idée
Tu veux savoir **ce qui a changé depuis** ta version actuelle et **adapter le code proprement**, pas seulement monter un numéro de version.

## Document maître
Suivre **`docs/processus-mise-a-jour-profonde.md`** étape par étape.

## Déroulé agent (obligatoire)

### A. Cadrage
- Identifier **une** cible principale (`X`) et la version **actuelle** dans le repo (fichiers de config, lockfile, imports).
- Si plusieurs sujets → proposer de découper en plusieurs sessions.

### B. Baseline
- Noter versions, chemins des fichiers sensibles, tests existants sur la zone.

### C. Recherche profonde
- **WebSearch** + **WebFetch** sur les pages **officielles** : release notes, migration guide, dépréciations.
- Synthèse structurée :
  - Breaking changes **pertinents** pour ce repo (pas tout le changelog).
  - Fichiers à modifier (liste).
  - Ordre des opérations (types → runtime → config).

### D. Plan court
- 3–10 puces : QUOI changer, POURQUOI (réf. doc), COMMENT (fichiers).

### E. Exécution clean
- Modifications minimales mais **complètes** (pas de TODO laissés sans issue).
- Pas de contournement type `any` massif sans plan de retypage.

### F. Examine
- `tsc`, tests ciblés, lint. **Fail-stop** : 2 échecs sur le même point → réanalyser la doc.

### G. Mémoire
- Mettre à jour `.claude/memory/stack.md` (versions). Décision notable → `decisions.md` ou ADR.

## Différence avec `/deps`
- `/deps` = inventaire, vulnérabilités, outdated **en masse**.
- `/deep-update` = **un sujet**, **veille changelog approfondie**, migration **raisonnée**.

## Liens
- `/apex` pour structurer la session si le chantier est large.
- `/scope-task` si tu hésites sur les fichiers à ouvrir en premier.
