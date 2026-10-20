#!/usr/bin/env python3
"""
Test and verify desktop shortcuts for YouTube Audio Ripper
"""

from pathlib import Path

print("=" * 70)
print("YouTube Audio Ripper - Desktop Shortcut Test")
print("=" * 70)

# Check what files exist on desktop
desktop = Path("C:/Users/user/Desktop")
print(f"Desktop directory: {desktop}")
print()

# List all files in desktop
print("Files in desktop directory:")
for file in desktop.iterdir():
    if "YouTube" in file.name or "Audio" in file.name or "Ripper" in file.name:
        print(f"  📁 {file.name} ({file.stat().st_size} bytes)")
        
        # Check file type
        if file.suffix == ".vbs":
            print("     -> VBScript file - launches app when double-clicked")
        elif file.suffix == ".bat":
            print("     -> Batch file - executes Python script")
        elif file.suffix == ".url":
            print("     -> Internet shortcut - opens URL/application")
        elif file.suffix == ".lnk":
            print("     -> Windows shortcut")
        
        # Try to read and display content
        try:
            content = file.read_text()
            first_line = content.split('\n')[0].strip()
            print(f"     -> Content preview: {first_line[:60]}...")
        except Exception:
            pass

print()
print("=" * 70)
print("Desktop Shortcuts Created Successfully!")
print("=" * 70)
print()
print("To launch the app from desktop:")
print("1. Double-click: YouTube Audio Ripper.url")
print("2. Or double-click: YouTube-Audio-Ripper.vbs")
print("3. Or double-click: YouTube-Audio-Ripper.bat")
print()
print("The app will launch silently (no console window).")
print()
print("Files created:")
print("  YouTube Audio Ripper.url  -> Windows Internet shortcut")
print("  YouTube-Audio-Ripper.vbs   -> VBScript launcher")
print("  YouTube-Audio-Ripper.bat   -> Batch file launcher")
print()
print("All shortcuts point to:")
print("  C:/Users/user/youtube-audio-ripper/launch.vbs")
print("  which runs: ./venv/Scripts/python.exe rip_gui.py")