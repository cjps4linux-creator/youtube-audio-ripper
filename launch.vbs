' YouTube Audio Ripper - Quick Launch
' Launches the application immediately without console window

Set oShell = CreateObject("WScript.Shell")
Set oFSO = CreateObject("Scripting.FileSystemObject")

strScriptPath = oFSO.GetParentFolderName(WScript.ScriptFullName)
strPythonPath = strScriptPath & "\venv\Scripts\python.exe"
strAppPath = strScriptPath & "\rip_gui.py"

' Run the application with window hidden (style 0 = hide)
oShell.Run strPythonPath & " " & strAppPath, 0, False

Set oShell = Nothing
Set oFSO = Nothing