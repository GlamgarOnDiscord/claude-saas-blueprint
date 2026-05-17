# ADR 0001: Architecture de l'Outillage IA

## État
Accepté

## Date
2026-03-13

## Contexte
Le projet nécessite une orchestration d'agents IA robuste pour le développement d'un SaaS. La latence et la cohérence du contexte sont des facteurs critiques.

## Décision
Nous adoptons une architecture basée sur l'Agent SDK avec les piliers suivants :
1.  **Gestion du Contexte par Prompt Caching** : Le fichier `CLAUDE.md` sert de base de connaissances statique et dynamique pour réduire les coûts et améliorer la réactivité.
2.  **Utilisation systématique du Memory tool** : Pour le suivi des bugs récurrents, des préférences de style et des états de projet persistants.
3.  **Workflow GRIP v2** : Un protocole strict de Grep, Read, Intent et Prove pour garantir la fiabilité des modifications de code.
4.  **Skills Natives** : Définition de compétences réutilisables dans `.claude/skills/` pour automatiser les tâches transverses (ex: tests ciblés, validation de schémas).

## Conséquences
- Amélioration de la vitesse d'exécution des agents.
- Réduction drastique des hallucinations grâce au caching du contexte global.
- Traçabilité totale des décisions d'architecture via les dossiers `docs/adr/`.
- Dépendance à l'Agent SDK pour l'exécution des skills.
