# `.claude/agents/` — Subagents Claude Code (réservé)

Ce dossier est réservé aux **vrais subagents** Claude Code : fichiers Markdown avec frontmatter YAML (`name`, `description`, `tools`, `model`, `memory`, `hooks`).

Ce dépôt **n'embarque pas de subagent** par défaut — l'agent principal utilise les subagents Claude Code intégrés (`Explore`, `Plan`, `general-purpose`, `websearch`, `clean-code-generator`, `unit-testing:test-automator`, `unit-testing:debugger`).

Pour créer un subagent custom : utiliser le template `templates/subagent.template.md` puis déposer le fichier ici.

Les **guides multi-agents** (orchestration, model routing, debugging…) sont dans `../guides/`.
