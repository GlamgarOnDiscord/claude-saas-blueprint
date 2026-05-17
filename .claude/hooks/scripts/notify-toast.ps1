# Hook generique de notification toast Windows.
# Usage: -Title "..." -Message "..." -Duration 5000

param(
    [string]$Title = 'Claude Code',
    [string]$Message = 'Notification',
    [int]$Duration = 4000
)

try {
    Add-Type -AssemblyName System.Windows.Forms -ErrorAction SilentlyContinue
    $n = New-Object System.Windows.Forms.NotifyIcon
    $n.Icon = [System.Drawing.SystemIcons]::Information
    $n.Visible = $true
    $n.ShowBalloonTip($Duration, $Title, $Message, [System.Windows.Forms.ToolTipIcon]::Info)
    Start-Sleep -Milliseconds ($Duration + 1000)
    $n.Dispose()
} catch {}

exit 0
