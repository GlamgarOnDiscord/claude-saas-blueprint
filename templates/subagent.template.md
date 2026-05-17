# Template — Subagent (`.claude/agents/`)

## Usage
Copier ce template pour créer un nouveau subagent dans `.claude/agents/<nom>.md`.

## Template

```markdown
---
name: mon-agent
description: "Description courte — quand et pourquoi utiliser cet agent (1-2 phrases)"
model: sonnet       # opus | sonnet | haiku
tools:
  - Read
  - Edit
  - Bash
  - grep_search
  - file_search
memory: true         # accès à la mémoire auto (~/.claude/projects/)
# hooks:             # hooks spécifiques à cet agent (optionnel)
#   PreToolUse:
#     - matcher: Bash
#       command: "echo 'hook triggered'"
# mcpServers:        # MCPs scopés à cet agent (optionnel)
#   context7:
#     command: npx
#     args: ["@context7/mcp"]
# skills:            # skills disponibles pour cet agent (optionnel)
#   - feature
#   - fix
---

# Mon Agent

## Rôle
Description détaillée de ce que fait cet agent.

## Quand l'utiliser
- Cas d'usage 1
- Cas d'usage 2

## Instructions
1. Étape 1
2. Étape 2
3. Étape 3

## Contraintes
- Ne PAS modifier les fichiers hors de son scope
- Toujours respecter les conventions du projet (`AGENTS.md`)
```

## Champs frontmatter

| Champ | Obligatoire | Description |
|-------|-------------|-------------|
| `name` | Oui | Identifiant unique de l'agent |
| `description` | Oui | Quand/pourquoi utiliser cet agent |
| `model` | Non | `opus`, `sonnet` (défaut), `haiku` |
| `tools` | Non | Liste des outils autorisés |
| `memory` | Non | `true`/`false` — accès à la mémoire |
| `hooks` | Non | Hooks spécifiques au lifecycle de cet agent |
| `mcpServers` | Non | MCP servers scopés (inline config) |
| `skills` | Non | Skills accessibles par cet agent |

## Bonnes pratiques

- **1 agent = 1 responsabilité** précise
- **3-5 agents** max dans une équipe (agent teams)
- Utiliser **Haiku** pour les agents read-only (explore, search)
- Utiliser **Opus** uniquement pour les tâches complexes (refactoring, architecture)
- Sonnet pour le **code au quotidien** (défaut recommandé)
