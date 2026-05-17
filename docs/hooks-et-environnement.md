# Hooks et environnement (Claude Code)

La configuration active des hooks est dans **`.claude/settings.json`** (champ `hooks`).
Les **scripts** executes sont dans **`.claude/hooks/scripts/*.ps1`** (PowerShell-first).
Les fichiers `.claude/hooks/*.md` servent uniquement a documenter l'intention / la checklist.

> Reference officielle : https://code.claude.com/docs/en/hooks

## Types de hooks (5)

| Type | Declencheur | Usage typique |
|------|-------------|---------------|
| **command** | Commande shell | Bloquer commandes dangereuses, formater apres edit |
| **http** | POST HTTP vers une URL | Logger, valider via service externe, webhook |
| **mcp_tool** | Tool d'un serveur MCP connecte | Audit, scan securite via service interne |
| **prompt** | Prompt envoye a un modele Claude (single-turn) | Decision allow/block via LLM |
| **agent** | Subagent avec acces tools (multi-turn, experimental) | Verification approfondie avec lecture de fichiers |

## Evenements lifecycle officiels

Liste complete des evenements valides selon la doc officielle (regroupes par cadence) :

### Une fois par session
- `SessionStart` — debut ou reprise de session (matchers : `startup`, `resume`, `clear`, `compact`)
- `SessionEnd` — fin de session (matchers : `clear`, `resume`, `logout`, `prompt_input_exit`, etc.)
- `Setup` — `claude --init-only` ou `--init` / `--maintenance` en mode `-p`

### Une fois par tour
- `UserPromptSubmit` — apres soumission d'un prompt utilisateur
- `UserPromptExpansion` — quand un slash command s'expand en prompt
- `Stop` — Claude principal a fini de repondre
- `StopFailure` — fin de tour suite a erreur API (rate_limit, auth, billing, etc.)

### Boucle agentique (chaque tool call)
- `PreToolUse` — avant l'execution d'un tool (matchers : `Bash`, `Edit`, `Write`, `Read`, `Glob`, `Grep`, `Agent`, `WebFetch`, `WebSearch`, `AskUserQuestion`, `ExitPlanMode`, ou `mcp__server__tool`)
- `PostToolUse` — apres tool execute avec succes
- `PostToolUseFailure` — apres tool en echec
- `PostToolBatch` — une fois apres tout un batch de tools paralleles
- `PermissionRequest` — quand une boite de dialogue de permission s'affiche
- `PermissionDenied` — quand le classifier auto-mode refuse un tool

### Subagents
- `SubagentStart` — un subagent demarre (matchers : nom du subagent comme `Explore`, `Plan`, `general-purpose`, ou un nom custom)
- `SubagentStop` — un subagent finit
- `TaskCreated` — creation de tache via TaskCreate
- `TaskCompleted` — tache marquee completee
- `TeammateIdle` — un teammate d'agent team va devenir idle

### Memory / Configuration / Worktree
- `InstructionsLoaded` — `CLAUDE.md` ou `.claude/rules/*.md` charges (matchers : `session_start`, `nested_traversal`, `path_glob_match`, `include`, `compact`)
- `ConfigChange` — un fichier de config change (matchers : `user_settings`, `project_settings`, `local_settings`, `policy_settings`, `skills`)
- `CwdChanged` — changement de working directory
- `FileChanged` — fichier surveille modifie
- `WorktreeCreate` / `WorktreeRemove` — creation / suppression d'un worktree

### Compaction et notifications
- `PreCompact` / `PostCompact` — avant / apres compaction (matchers : `manual`, `auto`)
- `Notification` — Claude Code envoie une notification (matchers : `permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog`, `elicitation_complete`, `elicitation_response`)
- `Elicitation` / `ElicitationResult` — input demande par un MCP server

## Hooks branches dans ce dépôt

Voir `.claude/hooks/scripts/README.md` pour le détail. Resume :

| Hook | Matcher | Script | Comportement |
|------|---------|--------|--------------|
| `PreToolUse` | `Bash` | `pre-bash-dangerous.ps1` | Bloque `rm -rf /`, `DROP DATABASE`, `git push -f`, `format c:`, etc. |
| `PreToolUse` | `Edit\|Write` | `pre-edit-protect.ps1` | Bloque edition `.env`, credentials ; detecte secrets (AKIA, sk_live, ghp, sk-ant, AIza, cles privees) |
| `PostToolUse` | `Edit\|Write` | `post-edit-format.ps1` | `npx prettier --write` sur les fichiers JS/TS modifies (best-effort) |
| `PostToolUse` | `Bash` | `post-bash-audit.ps1` | Log les commandes dans `.claude/bash-audit.jsonl` |
| `SessionStart` | `compact` | `session-start-context.ps1` | Recharge un recap projet apres `/compact` |
| `Notification` | `idle_prompt` | `notify-toast.ps1` | Toast Windows quand Claude attend |
| `Stop` | (aucun) | `notify-toast.ps1` | Toast Windows quand Claude termine |

## Pourquoi PowerShell-first ?

L'ancienne config utilisait `bash -c '...python3 -c \"...\"'` ce qui :

- **Cassait silencieusement** sur Windows sans WSL/Git Bash + Python3 dans le PATH (cas par defaut).
- Empilait l'echappement de quotes (4 niveaux de `\\\\\\\"`).
- Cachait les erreurs (`exit 0` par defaut sur erreur).

Avec PowerShell natif (`"shell": "powershell"` selon la doc officielle) :

- **Aucune dependance externe** sur Windows.
- Scripts independants, lisibles et **testables** localement.
- Erreurs visibles, exit codes explicites.

> La doc officielle confirme : `"shell": "powershell"` est un champ valide sur `type: "command"`. Claude Code auto-detecte `pwsh.exe` (PowerShell 7+) avec fallback `powershell.exe` (5.1).

Pour macOS/Linux : creer des equivalents `.sh` dans `.claude/hooks/scripts/` et omettre le champ `shell` (defaut bash).

## Variables d'environnement persistantes

Les hooks `SessionStart`, `Setup`, `CwdChanged` et `FileChanged` ont acces a `CLAUDE_ENV_FILE` :

```powershell
# Dans un hook PowerShell
Add-Content -Path $env:CLAUDE_ENV_FILE -Value 'export NODE_ENV=production'
```

Les variables ecrites dans ce fichier persistent dans toutes les commandes Bash subsequentes de la session.

## Variables de path utiles

- `${CLAUDE_PROJECT_DIR}` — racine du projet (utiliser dans `command:` pour des paths absolus)
- `${CLAUDE_PLUGIN_ROOT}` — racine du plugin (pour les hooks bundled dans un plugin)

Exemple :
```json
{
  "type": "command",
  "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/scripts/pre-bash-dangerous.ps1",
  "shell": "powershell"
}
```

## Tester un hook localement

```powershell
# Test du blocage commande dangereuse
$json = '{"tool_input":{"command":"rm -rf /"}}'
[System.IO.File]::WriteAllText("$PWD\payload.json", $json)
Get-Content payload.json -Raw | powershell -NoProfile -ExecutionPolicy Bypass -File .claude/hooks/scripts/pre-bash-dangerous.ps1
$LASTEXITCODE  # Doit afficher 2 (block)
Remove-Item payload.json
```

## Recommandations

- Garde les **PreToolUse** (securite) — ils bloquent commandes dangereuses et edition de fichiers sensibles.
- Le **PostToolUse Prettier** est confort, pas critique : tu peux le retirer.
- Le **PostToolUse Bash audit** trace ce que l'agent a vraiment execute (`.claude/bash-audit.jsonl`, gitignore).
- Sur **Windows**, garde `"shell": "powershell"` partout pour eviter la dependance bash.
- Pour des verifications complexes, prefere les hooks `prompt` (LLM single-turn) ou `agent` (multi-turn experimental) plutot que des scripts shell tordus.
