#!/usr/bin/env python3
"""
Create desktop shortcut for YouTube Audio Ripper
"""

from pathlib import Path

def create_windows_shortcut(target_path, shortcut_path, description="YouTube Audio Ripper"):
    """
    Create a Windows .lnk file for the target
    """
    # Windows .lnk file format structure
    
    # Header constants
    LINK_VERSION = b'\x01\x00\x00\x00'
    LINK_FLAGS = b'\x01\x00\x00\x00'
    CREATED_TIME = b'\x00\x00\x00\x00\x00\x00\x00\x00'
    ACCESSED_TIME = b'\x00\x00\x00\x00\x00\x00\x00\x00'
    WRITE_TIME = b'\x00\x00\x00\x00\x00\x00\x00\x00'
    ICON_INDEX = b'\x00\x00\x00\x00'
    HOTKEY = b'\x00\x00'
    RESERVED1 = b'\x00\x00\x00\x00'
    RESERVED2 = b'\x00\x00\x00\x00'
    RESERVED3 = b'\x00\x00\x00\x00'
    
    # Build the shell item data block for the target
    # This is a simplified version - for full compatibility, use a proper .lnk library
    
    # Simple approach: create a .url shortcut instead (more reliable)
    url_content = f"""[InternetShortcut]
URL=file:///{target_path}
IconFile={target_path}
IconIndex=0
"""
    
    return url_content

# Create desktop shortcut
desktop_path = Path("C:/Users/user/Desktop")
app_path = Path("C:/Users/user/youtube-audio-ripper/launch.vbs")
shortcut_name = "YouTube Audio Ripper"

# Method 1: Create a .url shortcut (works everywhere)
url_path = desktop_path / f"{shortcut_name}.url"
try:
    url_content = f"""[InternetShortcut]
URL=file:///{app_path}
"""
    url_path.write_text(url_content)
    print(f"✅ Created: {url_path}")
except Exception as e:
    print(f"❌ Failed to create .url: {e}")

# Method 2: Update existing files
print(f"\nDesktop shortcuts created in: {desktop_path}")
print("Files available:")
for file in desktop_path.glob("YouTube*"):
    print(f"  📁 {file.name}")