# `.claude/hooks/scripts/` — Scripts PowerShell des hooks

Tous les hooks branchés dans `.claude/settings.json` utilisent ces scripts via `"shell": "powershell"`.

| Script | Hook | Rôle |
|--------|------|------|
| `pre-bash-dangerous.ps1` | `PreToolUse` Bash | Bloque `rm -rf /`, `DROP DATABASE`, `git push -f`, `format c:`, `shutdown`, etc. |
| `pre-edit-protect.ps1` | `PreToolUse` Edit/Write | Bloque édition de `.env`, credentials, et détecte les secrets (AKIA, sk_live, ghp, sk-ant, AIza, clés privées) |
| `post-edit-format.ps1` | `PostToolUse` Edit/Write | Lance `npx prettier --write` sur les fichiers JS/TS modifiés (best-effort) |
| `post-bash-audit.ps1` | `PostToolUse` Bash | Log les commandes dans `.claude/bash-audit.jsonl` |
| `session-start-context.ps1` | `SessionStart` (compact) | Recharge un récap projet après `/compact` |
| `notify-toast.ps1` | `Notification` / `Stop` | Toast Windows (NotifyIcon) |

## Convention de sortie

- **Exit 0** → autorisation, pas de blocage.
- **Exit 2** → blocage, message sur stderr (Claude Code remontera ce message à l'utilisateur).
- **stdout** sur `SessionStart` → ajouté au contexte de la session.

## Lecture du payload Claude Code

Tous les hooks Pre/Post reçoivent un JSON sur stdin :

```json
{
  "tool_input": {
    "command": "...",       // Bash
    "file_path": "...",     // Edit/Write
    "new_string": "...",    // Edit
    "content": "..."        // Write
  }
}
```

Pattern PowerShell pour le parser :

```powershell
$payload = [Console]::In.ReadToEnd()
$data = $payload | ConvertFrom-Json
$cmd = [string]$data.tool_input.command
```

## Tests manuels

```powershell
# Test commande dangereuse
'{ "tool_input": { "command": "rm -rf /" } }' | `
  powershell -NoProfile -File .claude/hooks/scripts/pre-bash-dangerous.ps1

# Test secret dans le contenu
'{ "tool_input": { "file_path": "src/x.ts", "new_string": "sk_live_abcdef..." } }' | `
  powershell -NoProfile -File .claude/hooks/scripts/pre-edit-protect.ps1
```

## Pourquoi PowerShell et pas bash ?

L'ancienne version utilisait `bash -c '...python3 -c \"...\"'` ce qui :
- Casse silencieusement si bash ou python3 ne sont pas dans le PATH (Windows par défaut)
- Empile l'échappement de quotes (4 niveaux de `\\\\\\\"`)
- Cache les erreurs (`exit 0` par défaut sur erreur)

Avec PowerShell natif (`"shell": "powershell"`, dispo Claude Code v2.1+) :
- Aucune dépendance externe sur Windows
- Scripts indépendants et testables
- Erreurs visibles, exit codes explicites

Pour macOS/Linux, créer des équivalents `.sh` dans le même dossier et adapter `settings.json` (`"shell": "bash"`).
