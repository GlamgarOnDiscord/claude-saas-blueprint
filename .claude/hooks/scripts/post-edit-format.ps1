# Hook: PostToolUse Edit/Write — formatte les fichiers JS/TS modifies via Prettier (best-effort).
# Exit 0 quoiqu'il arrive (ne bloque jamais).

$ErrorActionPreference = 'SilentlyContinue'
$payload = [Console]::In.ReadToEnd()
if ([string]::IsNullOrWhiteSpace($payload)) { exit 0 }

try {
    $data = $payload | ConvertFrom-Json
    $filePath = [string]$data.tool_input.file_path
} catch {
    exit 0
}

if ([string]::IsNullOrEmpty($filePath)) { exit 0 }
if (-not (Test-Path $filePath)) { exit 0 }

$ext = [System.IO.Path]::GetExtension($filePath).TrimStart('.')
if ($ext -notin @('ts', 'tsx', 'js', 'jsx', 'mjs', 'cjs')) { exit 0 }

$npx = Get-Command npx -ErrorAction SilentlyContinue
if (-not $npx) { exit 0 }

# Run prettier in background, ne bloque jamais le hook
try {
    Start-Process -FilePath npx -ArgumentList "prettier --write `"$filePath`"" -NoNewWindow -Wait -ErrorAction SilentlyContinue | Out-Null
} catch {
    # Ignore les erreurs (prettier pas configure, etc.)
}

exit 0
