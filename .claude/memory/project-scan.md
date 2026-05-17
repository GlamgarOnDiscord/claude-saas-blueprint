# Project Scan

## Status : Non scanné
Lancer `/onboard` pour analyser le projet courant.

## Format du Scan
Après `/onboard`, ce fichier contient :
- Stack technique détectée (framework, ORM, auth, paiements, déploiement)
- Architecture (hexagonal | MVC | feature-based | flat)
- Conventions de nommage observées
- Multi-tenancy détecté (oui/non)
- Ratio fichiers source / tests
- Indicateurs de dette (`any`, `console.log`, secrets hardcodés, RLS manquant)
- Health score (X/10) avec priorités d'action
