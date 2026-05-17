# `.claude/hooks/scripts/` — Scripts PowerShell des hooks

Tous les hooks branchés dans `.claude/settings.json` utilisent ces scripts via `"shell": "powershell"` (officiellement supporté par Claude Code).

| Script | Hook | Rôle |
|--------|------|------|
| `pre-bash-dangerous.ps1` | `PreToolUse` matcher `Bash` | Bloque `rm -rf /`, `DROP DATABASE`, `git push -f`, `format c:`, `shutdown`, etc. |
| `pre-edit-protect.ps1` | `PreToolUse` matcher `Edit\|Write` | Bloque édition de `.env`, credentials, et détecte 8 patterns de secrets (AKIA, sk_live, ghp, sk-ant, AIza, clés privées) |
| `post-edit-format.ps1` | `PostToolUse` matcher `Edit\|Write` | Lance `npx prettier --write` sur les fichiers JS/TS modifiés (best-effort) |
| `post-bash-audit.ps1` | `PostToolUse` matcher `Bash` | Log les commandes dans `.claude/bash-audit.jsonl` (gitignore) |
| `session-start-context.ps1` | `SessionStart` matcher `compact` | Recharge un récap projet après `/compact` |
| `notify-toast.ps1` | `Notification` matcher `idle_prompt` + `Stop` | Toast Windows (NotifyIcon) |

## Convention d'exit codes

Selon la [doc officielle Claude Code hooks](https://code.claude.com/docs/en/hooks) :

- **Exit 0** → succès, pas de blocage. Stdout parsé pour JSON output (mais pour PreTooluse/PreEdit, exit 2 reste plus simple).
- **Exit 2** → **blocage** : message stderr remonté à Claude (PreToolUse) ou utilisateur (autres). C'est le code à utiliser pour bloquer.
- Tout autre exit code → erreur non-bloquante, message dans le debug log.

## Path resolution

Tous les hooks utilisent `${CLAUDE_PROJECT_DIR}` (variable injectée par Claude Code) pour pointer les scripts depuis n'importe quel cwd :

```json
{
  "type": "command",
  "shell": "powershell",
  "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/scripts/pre-bash-dangerous.ps1"
}
```

## Lecture du payload Claude Code

Tous les hooks Pre/Post reçoivent un JSON sur stdin :

```json
{
  "session_id": "...",
  "transcript_path": "...",
  "cwd": "...",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "...",
    "description": "...",
    "timeout": 120000,
    "run_in_background": false
  }
}
```

Pour `Edit` : `tool_input.file_path` + `tool_input.old_string` + `tool_input.new_string`.
Pour `Write` : `tool_input.file_path` + `tool_input.content`.

Pattern PowerShell pour parser :

```powershell
$payload = [Console]::In.ReadToEnd()
$data = $payload | ConvertFrom-Json
$cmd = [string]$data.tool_input.command
```

## Tests manuels

```powershell
# Test commande dangereuse (doit retourner exit 2)
$json = '{"tool_input":{"command":"rm -rf /"}}'
[System.IO.File]::WriteAllText("$PWD\payload.json", $json)
Get-Content payload.json -Raw | powershell -NoProfile -ExecutionPolicy Bypass -File .claude/hooks/scripts/pre-bash-dangerous.ps1
$LASTEXITCODE  # 2 = block
Remove-Item payload.json

# Test secret (doit retourner exit 2)
$fake = 'sk_' + 'live_' + 'abcdefghijklmnopqrstuvwx'
$json = '{"tool_input":{"file_path":"src/x.ts","new_string":"' + $fake + '"}}'
[System.IO.File]::WriteAllText("$PWD\payload.json", $json)
Get-Content payload.json -Raw | powershell -NoProfile -ExecutionPolicy Bypass -File .claude/hooks/scripts/pre-edit-protect.ps1
$LASTEXITCODE  # 2 = block
Remove-Item payload.json
```

## Pourquoi PowerShell-first ?

- L'ancienne version utilisait `bash -c '...python3 -c ...'` — cassé silencieusement sur Windows sans WSL/Git Bash + Python3 dans le PATH.
- `"shell": "powershell"` est **officiellement supporté** par Claude Code (auto-detect `pwsh.exe` 7+, fallback `powershell.exe` 5.1).
- Aucune dépendance externe. Scripts indépendants et **testables** localement.

Pour macOS/Linux, créer des équivalents `.sh` dans le même dossier et omettre le champ `shell` (défaut bash).

## JSON output (alternative à exit codes)

Pour des besoins plus fins, exit 0 + JSON sur stdout :

```powershell
# Bloquer un PreToolUse avec raison
$output = @{
    hookSpecificOutput = @{
        hookEventName = 'PreToolUse'
        permissionDecision = 'deny'
        permissionDecisionReason = 'Custom block reason'
    }
} | ConvertTo-Json -Compress -Depth 5
Write-Output $output
exit 0
```

Voir la [doc officielle JSON output](https://code.claude.com/docs/en/hooks#json-output) pour les options par event.
