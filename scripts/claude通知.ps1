# Claude Code Notification フック用スクリプト
# 標準入力でフックのJSON（message フィールド）を受け取り、Windowsのトースト通知＋音で知らせる。
# 呼び出し例: powershell.exe -ExecutionPolicy Bypass -File "claude通知.ps1"

$ErrorActionPreference = "SilentlyContinue"

# 標準入力からフックのJSONを読む
$raw = [Console]::In.ReadToEnd()
$msg = ""
try {
    if ($raw) { $msg = ([string]([System.Text.Json.JsonDocument]::Parse($raw).RootElement.GetProperty("message").GetString())) }
} catch {
    # JsonDocument が使えない環境向けフォールバック
    try { $msg = ($raw | ConvertFrom-Json).message } catch { $msg = "" }
}
if (-not $msg) { $msg = "Claude Code が入力を待っています" }

# 音（アテンション用のシステム音）
[System.Media.SystemSounds]::Exclamation.Play()

# バルーン/トースト通知（Windows 11 ではトーストとして表示される）
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
$notify = New-Object System.Windows.Forms.NotifyIcon
$notify.Icon = [System.Drawing.SystemIcons]::Information
$notify.Visible = $true
$notify.BalloonTipTitle = "Claude Code"
$notify.BalloonTipText = $msg
$notify.ShowBalloonTip(8000)
Start-Sleep -Milliseconds 6000
$notify.Dispose()
