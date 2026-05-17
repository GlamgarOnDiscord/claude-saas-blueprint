# Hook: PreToolUse Edit/Write — bloque l'edition de fichiers sensibles
# (env files, credentials, cles privees) ET la presence de secrets dans le contenu.
# Exit 2 = block ; Exit 0 = autorise.

$ErrorActionPreference = 'Stop'
$payload = [Console]::In.ReadToEnd()
if ([string]::IsNullOrWhiteSpace($payload)) { exit 0 }

try {
    $data = $payload | ConvertFrom-Json
    $filePath = [string]$data.tool_input.file_path
    $content = [string]$data.tool_input.new_string
    if ([string]::IsNullOrEmpty($content)) { $content = [string]$data.tool_input.content }
} catch {
    exit 0
}

# 1. Chemins sensibles
$sensitivePaths = @(
    '\.env$',
    '\.env\.local$',
    '\.env\.production$',
    '\.env\.staging$',
    'credentials\.json$',
    'id_rsa$',
    '\.pem$',
    '\.p12$',
    '\.pfx$'
)

if (-not [string]::IsNullOrEmpty($filePath)) {
    foreach ($pattern in $sensitivePaths) {
        if ($filePath -match $pattern) {
            [Console]::Error.WriteLine("BLOCK: fichier sensible protege ($filePath). Modifiez manuellement si necessaire.")
            exit 2
        }
    }
}

# 2. Secrets dans le contenu
if (-not [string]::IsNullOrEmpty($content)) {
    $secretPatterns = @(
        @{Name='AWS Access Key'; Pattern='AKIA[0-9A-Z]{16}'},
        @{Name='Stripe Live Secret'; Pattern='sk_live_[0-9a-zA-Z]{24,}'},
        @{Name='GitHub Personal Token'; Pattern='ghp_[0-9a-zA-Z]{36}'},
        @{Name='GitHub OAuth Token'; Pattern='gho_[0-9a-zA-Z]{36}'},
        @{Name='OpenAI Key'; Pattern='sk-(proj-)?[A-Za-z0-9]{40,}'},
        @{Name='Anthropic Key'; Pattern='sk-ant-[A-Za-z0-9-]{60,}'},
        @{Name='Google API Key'; Pattern='AIza[0-9A-Za-z_-]{35}'},
        @{Name='Generic Private Key'; Pattern='-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----'}
    )

    foreach ($s in $secretPatterns) {
        if ($content -match $s.Pattern) {
            [Console]::Error.WriteLine("BLOCK: secret detecte dans le contenu ($($s.Name)). Ne pas committer de secrets.")
            exit 2
        }
    }
}

exit 0
