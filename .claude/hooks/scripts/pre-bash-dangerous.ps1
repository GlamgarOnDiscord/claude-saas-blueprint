# Hook: PreToolUse Bash — bloque les commandes destructives.
# Lit le payload JSON Claude Code sur stdin et vérifie tool_input.command.
# Exit 2 = block + message stderr ; Exit 0 = autorise.

$ErrorActionPreference = 'Stop'
$payload = [Console]::In.ReadToEnd()
if ([string]::IsNullOrWhiteSpace($payload)) { exit 0 }

try {
    $data = $payload | ConvertFrom-Json
    $cmd = [string]$data.tool_input.command
} catch {
    exit 0
}

if ([string]::IsNullOrWhiteSpace($cmd)) { exit 0 }

$dangerous = @(
    'rm\s+-rf\s+[/~]',
    'DROP\s+(DATABASE|TABLE|SCHEMA)',
    'format\s+[a-z]:',
    '\bshutdown\b',
    '\breboot\b',
    'mkfs\.',
    '>\s*/dev/sd',
    'Remove-Item\s+-Recurse\s+-Force\s+[/~]',
    'rd\s+/s\s+/q\s+c:'
)

foreach ($pattern in $dangerous) {
    if ($cmd -match $pattern) {
        [Console]::Error.WriteLine("BLOCK: commande destructive detectee (pattern: $pattern). Confirmez manuellement.")
        exit 2
    }
}

# Push direct sur main/master ou force push
if ($cmd -match 'git\s+push.*(origin\s+(main|master)|--?force\b|-f\b)') {
    [Console]::Error.WriteLine("BLOCK: push direct sur main/master ou force push interdit. Cree une branche et une PR.")
    exit 2
}

exit 0
