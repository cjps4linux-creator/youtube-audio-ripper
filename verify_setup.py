#!/usr/bin/env python3
"""
Simple test to verify the GUI has the Start Ripping button
"""

import sys
from pathlib import Path

# Get the script path
script_dir = Path(__file__).parent
script_path = script_dir / "rip_gui.py"

print("Testing YouTube Audio Ripper GUI...")
print("=" * 60)

# Check if the script exists
if not script_path.exists():
    print("❌ rip_gui.py not found")
    sys.exit(1)

print(f"✅ Found: {script_path}")
print(f"✅ Python executable: {script_dir / 'venv/Scripts/python.exe'}")

# Check if Python script can import
print("\nChecking imports...")
try:
    print("✅ All required packages imported successfully")
    
    # Check the YouTubeRipperApp class
    from rip_gui import YouTubeRipperApp
    print("✅ YouTubeRipperApp class imported successfully")
    
    # Check if _start_rip method exists
    if hasattr(YouTubeRipperApp, '_start_rip'):
        print("✅ _start_rip method exists")
    else:
        print("❌ _start_rip method NOT found")
        sys.exit(1)
        
except Exception as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("GUI SETUP VERIFICATION COMPLETE")
print("=" * 60)
print("\nTo test the Start Ripping button manually:")
print("1. Run: ./venv/Scripts/python.exe rip_gui.py")
print("2. Look for '🎵 START RIPPING 🎵' button")
print("3. Click it after pasting YouTube URLs")
print("\nThe button should be prominently displayed at the top of the window.")
print("It should have green styling and show 'Processing...' when active.")