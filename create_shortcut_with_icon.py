#!/usr/bin/env python3
"""
Create desktop shortcut with music icon for YouTube Audio Ripper
"""

from pathlib import Path
import ctypes
from ctypes import wintypes
import struct

# Paths
app_dir = Path("C:/Users/user/youtube-audio-ripper")
desktop = Path("C:/Users/user/Desktop")
python_exe = app_dir / "venv/Scripts/python.exe"
script_file = app_dir / "rip_gui.py"
shortcut_path = desktop / "YouTube Audio Ripper.lnk"

# Remove old shortcuts
for f in desktop.glob("YouTube*"):
    f.unlink()
    print(f"Removed old shortcut: {f.name}")

# Create shortcut using Windows COM
try:
    shell = ctypes.windll('ole32.CoInitialize')(None)
    ole = ctypes.OleDLL('ole32')
    shell = ctypes.windll.shell32.CoCreateInstance(
        "{00021401-0000-0000-C000-000000000046}",
        None,
        1,  # CLSCTX_INPROC_SERVER
        "{000214EE-0000-0000-C000-000000000046}"
    )
    
    shortcut = shell.QueryInterface("{000214F9-0000-0000-C000-000000000046}")
    
    shortcut.SetPath(str(python_exe))
    shortcut.SetArguments(f'"{script_file}"')
    shortcut.SetWorkingDirectory(str(app_dir))
    shortcut.SetDescription("YouTube Audio Ripper - Download audio to FLAC")
    shortcut.SetIconLocation("shell32.dll", 13)
    shortcut.Save(str(shortcut_path), None)
    
    print(f"✅ Created shortcut: {shortcut_path}")
    print(f"   Icon: Music note")
    print(f"   Target: {python_exe}")
    print(f"   Script: {script_file}")
    
except Exception as e:
    print(f"Using fallback method...")
    # Fallback: create a simple .bat file
    bat_content = f"""@echo off
title YouTube Audio Ripper
cd /d "{app_dir}"
"{python_exe}" "{script_file}"
"""
    bat_path = desktop / "YouTube Audio Ripper.bat"
    bat_path.write_text(bat_content)
    print(f"✅ Created batch launcher: {bat_path}")
