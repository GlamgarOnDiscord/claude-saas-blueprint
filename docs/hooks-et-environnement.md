# Hooks et environnement (Claude Code)

La configuration active des hooks est dans **`.claude/settings.json`** (champ `hooks`).
Les **scripts** executes sont dans **`.claude/hooks/scripts/*.ps1`** (PowerShell-first).
Les fichiers `.claude/hooks/*.md` servent uniquement a documenter l'intention / la checklist.

## Types de hooks

| Type | Declencheur | Usage typique |
|------|-------------|---------------|
| **command** | Avant/apres une commande shell | Bloquer commandes dangereuses, formater apres edit |
| **http** | Avant/apres une requete HTTP | Logger, modifier headers, rate limit |
| **prompt** | Transformation du prompt | Injecter contexte, traduire, filtrer |
| **agent** | Lifecycle de l'agent | Init, cleanup, monitoring |

## Evenements lifecycle (21 disponibles)

| Phase | Evenements |
|-------|-----------|
| Session | `SessionStart`, `SessionEnd` |
| Prompt | `PrePrompt`, `PostPrompt` |
| Tool use | `PreToolUse`, `PostToolUse` |
| Agent | `AgentStart`, `AgentStop`, `AgentError` |
| Subagent | `SubagentSpawn`, `SubagentComplete` |
| Stop | `Stop`, `PreStop`, `PostStop` |
| Edit | `PreEdit`, `PostEdit` |
| Bash | `PreBash`, `PostBash` |
| HTTP | `PreHTTP`, `PostHTTP` |
| Memory | `MemoryUpdate` |

> Reference complete : `code.claude.com/docs/en/hooks`

## Hooks branches dans ce dépôt

Voir `.claude/hooks/scripts/README.md` pour le détail. Resume :

| Hook | Script | Comportement |
|------|--------|--------------|
| `PreToolUse` Bash | `pre-bash-dangerous.ps1` | Bloque `rm -rf /`, `DROP DATABASE`, `git push -f`, `format c:`, etc. |
| `PreToolUse` Edit/Write | `pre-edit-protect.ps1` | Bloque edition `.env`, credentials ; detecte secrets (AKIA, sk_live, ghp, sk-ant, AIza, cles privees) |
| `PostToolUse` Edit/Write | `post-edit-format.ps1` | `npx prettier --write` sur les fichiers JS/TS modifies (best-effort) |
| `PostToolUse` Bash | `post-bash-audit.ps1` | Log les commandes dans `.claude/bash-audit.jsonl` |
| `SessionStart` (compact) | `session-start-context.ps1` | Recharge un recap projet apres `/compact` |
| `Notification` / `Stop` | `notify-toast.ps1` | Toast Windows |

## Pourquoi PowerShell-first ?

L'ancienne config utilisait `bash -c '...python3 -c \"...\"'` ce qui :

- **Cassait silencieusement** sur Windows sans WSL/Git Bash + Python3 dans le PATH (cas par defaut).
- Empilait l'echappement de quotes (4 niveaux de `\\\\\\\"`).
- Cachait les erreurs (`exit 0` par defaut sur erreur).

Avec PowerShell natif (`"shell": "powershell"`, dispo Claude Code v2.1+) :

- **Aucune dependance externe** sur Windows.
- Scripts independants, lisibles et **testables** localement.
- Erreurs visibles, exit codes explicites.

Pour macOS/Linux : creer des equivalents `.sh` dans `.claude/hooks/scripts/` et adapter `settings.json` (`"shell": "bash"`).

## Variables d'environnement persistantes

Les hooks peuvent persister des variables via `CLAUDE_ENV_FILE` :

```powershell
# Dans un hook PreToolUse PowerShell
Add-Content -Path $env:CLAUDE_ENV_FILE -Value "MY_VAR=value"
```

## Tester un hook localement

```powershell
# Test du blocage commande dangereuse
'{ "tool_input": { "command": "rm -rf /" } }' | `
  powershell -NoProfile -ExecutionPolicy Bypass -File .claude/hooks/scripts/pre-bash-dangerous.ps1
# Doit afficher BLOCK et exit 2

# Test secret detecte
'{ "tool_input": { "file_path": "src/x.ts", "new_string": "sk_live_abc..." } }' | `
  powershell -NoProfile -ExecutionPolicy Bypass -File .claude/hooks/scripts/pre-edit-protect.ps1
```

## Recommandations

- Garde les **PreToolUse** (securite) — ils bloquent les commandes dangereuses et l'edition de fichiers sensibles.
- Le **PostToolUse Prettier** est confort, pas critique : tu peux le retirer ou le remplacer par le formatage IDE.
- Le **PostToolUse Bash audit** est utile pour traquer ce que l'agent a vraiment execute (`.claude/bash-audit.jsonl`, deja gitignore).
- Sur **Windows**, garde `"shell": "powershell"` partout pour eviter la dependance bash.
- Les hooks **prompt** et **agent** sont utiles pour injecter du contexte dynamique ou monitorer les sessions.
