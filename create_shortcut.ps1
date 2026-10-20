$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut('C:\Users\user\Desktop\YouTube Audio Ripper.lnk')
$Shortcut.TargetPath = 'C:\Users\user\youtube-audio-ripper\venv\Scripts\python.exe'
$Shortcut.Arguments = 'C:\Users\user\youtube-audio-ripper\rip_gui.py'
$Shortcut.WorkingDirectory = 'C:\Users\user\youtube-audio-ripper'
$Shortcut.Description = 'YouTube Audio Ripper'
$Shortcut.IconLocation = 'shell32.dll,13'
$Shortcut.Save()
Write-Host 'Shortcut created with music icon'
