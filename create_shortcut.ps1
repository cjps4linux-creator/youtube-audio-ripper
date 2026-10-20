$WshShell = New-Object -ComObject WScript.Shell
$projectRoot = $PSScriptRoot
$python = Join-Path $projectRoot 'venv\Scripts\python.exe'
if (-not (Test-Path $python)) {
  $python = (Get-Command python.exe -ErrorAction SilentlyContinue).Source
}
if (-not $python) { throw 'No Python interpreter found. Create a venv at venv\ or install Python.' }
$Shortcut = $WshShell.CreateShortcut([Environment]::GetFolderPath('Desktop') + '\YouTube Audio Ripper.lnk')
$Shortcut.TargetPath = $python
$Shortcut.Arguments = Join-Path $projectRoot 'rip_gui.py'
$Shortcut.WorkingDirectory = $projectRoot
$Shortcut.Description = 'YouTube Audio Ripper'
$Shortcut.IconLocation = 'shell32.dll,13'
$Shortcut.Save()
Write-Host 'Shortcut created with music icon'
