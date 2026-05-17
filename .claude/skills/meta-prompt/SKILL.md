---
name: meta-prompt
description: "Métaprompt Creator — Génère des skills, rules, hooks et prompts optimisés."
disable-model-invocation: true
---

## Modes

### `/meta-prompt skill [nom] [description]` — Créer un nouveau skill
1. **Recherche** : Lancer un agent WebSearch pour trouver :
   - Les meilleures pratiques Anthropic pour le prompting (docs.anthropic.com)
   - Les patterns de prompt engineering récents
   - La doc officielle des libs/outils mentionnés dans la description
2. **Analyse** : Lire 2–3 `SKILL.md` existants sous `.claude/skills/*/SKILL.md` comme référence de style
3. **Génération** : Créer un dossier `.claude/skills/[nom]/` avec **`SKILL.md`** (norme [Agent Skills](https://agentskills.io/) + [doc Claude Code](https://docs.anthropic.com/en/docs/claude-code/skills)) :
   ```yaml
   ---
   name: [nom-kebab]
   description: "[1 phrase : quoi + quand l'utiliser — pour l'auto-détection]"
   argument-hint: "[optionnel]"
   disable-model-invocation: true   # si workflow manuel / effets de bord
   ---
   ```
   Puis corps markdown : sections courtes, critères de fin, liens vers `docs/` ou rules si besoin — **pas** de roman.
4. **Sauvegarde** : Écrire `.claude/skills/[nom]/SKILL.md` (jamais un seul `.md` à plat à la racine de `skills/`)
5. **Mise à jour** : Ajouter la ligne dans la table **Skills** de `CLAUDE.md` et une ligne dans `.claude/skills/README.md`

### `/meta-prompt rule [domaine]` — Créer une nouvelle rule
1. Lire le README des rules pour comprendre le format
2. Demander : "Quelle erreur as-tu rencontrée ?" ou "Quelle convention veux-tu imposer ?"
3. Générer le fichier `.claude/rules/[domaine].md` avec format :
   ```markdown
   # Rules: [Domaine]
   ## Obligatoire
   - TOUJOURS [action] [raison]
   ## Interdit
   - NE PAS [action] [raison]
   ## Learned
   ```

### `/meta-prompt hook [event]` — Créer un hook
1. Identifier l'événement déclencheur (pre-commit, post-edit, pre-push)
2. Lister les checks nécessaires
3. Générer dans `.claude/hooks/[event].md`

### `/meta-prompt improve [fichier]` — Améliorer un prompt existant
1. Lire le fichier existant
2. Lancer un agent WebSearch pour :
   - Chercher "anthropic prompt engineering best practices 2026"
   - Chercher les patterns spécifiques au domaine du skill
3. Identifier les faiblesses :
   - Instructions ambiguës ?
   - Cas non couverts ?
   - Structure sous-optimale ?
4. Réécrire une version améliorée
5. Montrer le diff à l'utilisateur avant d'appliquer

## Principes de Génération
- **Clarté** : Chaque instruction doit être non ambiguë
- **Actionable** : Dire quoi faire, pas quoi penser
- **Structuré** : Phases numérotées, listes à puces
- **Concis** : corps du skill **moins de ~120 lignes** si possible ; rules **moins de ~30 lignes** par fichier domaine
- **Contextuel** : Référencer les fichiers du projet quand pertinent
- **Testable** : Chaque phase doit avoir un critère de succès vérifiable
