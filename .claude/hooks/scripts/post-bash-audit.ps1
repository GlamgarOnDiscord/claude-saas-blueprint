# Hook: PostToolUse Bash — log les commandes executees dans bash-audit.jsonl.
# Exit 0 quoiqu'il arrive.

$ErrorActionPreference = 'SilentlyContinue'
$payload = [Console]::In.ReadToEnd()
if ([string]::IsNullOrWhiteSpace($payload)) { exit 0 }

try {
    $data = $payload | ConvertFrom-Json
    $cmd = [string]$data.tool_input.command
} catch {
    exit 0
}

if ([string]::IsNullOrEmpty($cmd)) { exit 0 }
if ($cmd.Length -gt 200) { $cmd = $cmd.Substring(0, 200) }

$projectDir = $env:CLAUDE_PROJECT_DIR
if ([string]::IsNullOrEmpty($projectDir)) { $projectDir = $PWD.Path }

$logDir = Join-Path $projectDir '.claude'
if (-not (Test-Path $logDir)) { exit 0 }

$logFile = Join-Path $logDir 'bash-audit.jsonl'
$entry = [PSCustomObject]@{
    ts  = (Get-Date).ToString('o')
    cmd = $cmd
} | ConvertTo-Json -Compress

try {
    Add-Content -Path $logFile -Value $entry -ErrorAction SilentlyContinue
} catch {}

exit 0
