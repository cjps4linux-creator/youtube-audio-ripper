#!/usr/bin/env python3
"""
Quick fix: Create a simplified launcher that works reliably
"""

import sys
from pathlib import Path

# Add app directory to path
APP_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(APP_DIR))

print("Starting YouTube Audio Ripper...")

try:
    # Import and run the main app
    from rip_gui import YouTubeRipperApp
    print("✅ Import successful")
    
    # Create and run the app
    app = YouTubeRipperApp()
    print("✅ App initialized")
    print("Starting main loop...")
    
    app.mainloop()
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    
    input("\nPress Enter to exit...")