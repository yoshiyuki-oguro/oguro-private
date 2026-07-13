# Claude Code Notification hook script
# ASCII-only on purpose: Windows PowerShell 5.1 reads .ps1 as the system codepage
# (Shift-JIS on Japanese Windows), so any non-ASCII text here would be corrupted and
# break parsing. Keep this file 100% ASCII.
#
# Reads the hook JSON (message field) from stdin and shows a Windows toast + sound.
# Called like: powershell.exe -NoProfile -File "claude通知.ps1"

$ErrorActionPreference = "SilentlyContinue"

# Read hook JSON from stdin
$raw = [Console]::In.ReadToEnd()
$msg = ""
try { $msg = ($raw | ConvertFrom-Json).message } catch { $msg = "" }
if (-not $msg) { $msg = "Claude Code needs your attention" }

# Attention sound
[System.Media.SystemSounds]::Exclamation.Play()

# Balloon / toast notification (shown as a toast on Windows 11)
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
