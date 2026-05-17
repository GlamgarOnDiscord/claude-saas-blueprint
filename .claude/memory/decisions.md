# Décisions Techniques

## D001 — Architecture Hexagonale
- **Date**: 2026-03-15
- **Choix**: Architecture hexagonale (ports & adapters) pour tous les projets SaaS
- **Raison**: Testabilité, interchangeabilité des adapters, indépendance du framework
- **Alternative rejetée**: Architecture MVC classique (trop couplée)

## D002 — Workflow APEX
- **Date**: 2026-03-15
- **Choix**: Remplacer GRIP v2 par APEX (Analyze-Plan-Execute-Xamine)
- **Raison**: Plus clair, intègre la planification, le X rappelle la validation croisée
- **Alternative rejetée**: GRIP v2 (trop axé lecture, pas assez action)
