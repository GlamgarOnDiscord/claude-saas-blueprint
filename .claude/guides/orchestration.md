# Orchestration Multi-Agents

## Principe
Utiliser les sous-agents Claude Code pour paralléliser le travail et protéger le contexte principal.

## Quand Utiliser Quel Agent

### `Explore` (subagent_type: "Explore")
**Quand** : Besoin de comprendre le codebase avant d'agir
- Recherche de fichiers par pattern
- Comprendre comment une feature existante est implémentée
- Mapper les dépendances d'un module
- **Coût contexte** : Faible (résultat synthétisé)

### `general-purpose` (subagent_type: "general-purpose")
**Quand** : Tâche complexe multi-étapes autonome
- Recherche de documentation externe + synthèse
- Analyse comparative de solutions
- Debugging complexe nécessitant beaucoup de lectures
- **Coût contexte** : Moyen

### `unit-testing:test-automator` (subagent_type: "unit-testing:test-automator")
**Quand** : Générer ou améliorer des tests
- Après implémentation d'une feature → générer les tests
- Coverage insuffisant → identifier et combler les gaps
- **Coût contexte** : Faible

### `unit-testing:debugger` (subagent_type: "unit-testing:debugger")
**Quand** : Erreur difficile à comprendre
- Test qui échoue sans raison évidente
- Erreur runtime mystérieuse
- Régression après modification
- **Coût contexte** : Faible

### `Plan` (subagent_type: "Plan")
**Quand** : Feature complexe nécessitant un plan d'architecture
- Feature touchant > 5 fichiers
- Décision technique avec plusieurs approches possibles
- Refactoring majeur
- **Coût contexte** : Faible (retourne un plan)

### `clean-code-generator` (subagent_type: "clean-code-generator")
**Quand** : Écrire ou refactorer du code proprement
- Après un plan validé → implémenter
- Refactoring de code legacy
- **Coût contexte** : Moyen

### `websearch` (subagent_type: "websearch")
**Quand** : Besoin d'info externe rapide
- Vérifier la syntaxe d'une API
- Chercher la doc d'une lib
- Versions actuelles des packages
- **Coût contexte** : Très faible

## Patterns de Parallélisation

### Pattern: Feature Complète
```
[Parallèle]
├── Agent Explore → Scanner le code existant similaire
├── Agent WebSearch → Doc des libs nécessaires
└── Agent Plan → Préparer l'architecture

[Séquentiel après]
├── Implémenter (main thread ou clean-code-generator)
└── Agent test-automator → Générer les tests
```

### Pattern: Debug
```
[Parallèle]
├── Agent debugger → Analyser l'erreur
├── Agent Explore → Chercher des patterns similaires résolus
└── Agent WebSearch → Chercher l'erreur sur le web

[Séquentiel]
└── Appliquer le fix
```

### Pattern: Audit Qualité
```
[Parallèle]
├── Agent Explore → Structure et dead code
├── Agent general-purpose → Sécurité et dépendances
└── Agent test-automator → Coverage gaps

[Synthèse]
└── Rapport unifié
```

### Pattern: Onboarding Projet Existant
```
[Parallèle]
├── Agent Explore → Architecture et patterns
├── Agent Explore → Stack et dépendances
├── Agent Explore → Tests et coverage
└── Agent Explore → Config et infra

[Synthèse]
└── project-scan.md
```

### Pattern: Agent Team (Feature Complexe / XL)
Pour les features XL qui touchent backend + frontend + tests + docs :
```
Team Lead (agent principal, toi)
│
├── [Worktree A] Agent Backend (isolation: "worktree")
│   └── "Implémenter le core + adapters pour [feature].
│        Lire les rules dans .claude/rules/ avant chaque fichier.
│        Utiliser les templates dans templates/.
│        Terminer par tsc --noEmit."
│
├── [Worktree B] Agent Frontend (isolation: "worktree")
│   └── "Implémenter les composants UI pour [feature].
│        Utiliser shadcn/ui et les composants existants.
│        Server Components par défaut.
│        Responsive mobile-first."
│
├── [Background] Agent Tests
│   └── "Générer les tests unitaires + intégration pour [fichiers].
│        Pattern AAA, mocker les dépendances externes.
│        Couvrir happy path + erreurs + multi-tenancy."
│
└── [Team Lead] Coordonne, merge, résout les conflits
```
**Quand** : Feature qui prendrait > 30 minutes en séquentiel, avec front + back indépendants.
**Attention** : Bien définir les interfaces/types AVANT de lancer les agents en parallèle.

### Pattern: Tmux Multi-Agent (Features Indépendantes)
Quand l'utilisateur a plusieurs features indépendantes dans son sprint :
```
Terminal 1 → Agent sur Feature A (worktree A)
Terminal 2 → Agent sur Feature B (worktree B)
Terminal 3 → Agent sur Feature C (worktree C)
```
Chaque agent travaille sur son propre worktree git.
Le Team Lead merge les branches après validation.
**Pré-requis** : Aucun chevauchement de fichiers entre les features.

## Règles
1. **Max 4 agents en parallèle** pour éviter la surcharge
2. **Toujours synthétiser** le résultat des agents dans le contexte principal
3. **Background pour les tâches longues** : tests complets, audits, builds
4. **Foreground pour les dépendances** : quand le résultat influence l'étape suivante
5. **Worktree pour les expérimentations** : tester une approche sans impacter main
6. **Définir les interfaces AVANT** de lancer des agents en parallèle (éviter les conflits de types)
7. **Chaque agent lit ses rules** : les rules contextuelles ne sont PAS partagées automatiquement
