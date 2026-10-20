#!/usr/bin/env python3
"""
Quick test to isolate download issue
"""

import yt_dlp
import os
import tempfile
from pathlib import Path

def test_download():
    # Create temp file path
    temp_file = os.path.join(tempfile.gettempdir(), "test_download_opus.%(ext)s")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': temp_file,
        'quiet': True,
        'no_warnings': True,
    }
    
    print("Testing download...")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            print("Starting download...")
            ydl.download(['https://www.youtube.com/watch?v=dQw4w9WgXcQ'])
            print("✅ Download completed successfully")
            
            # Check for downloaded files
            temp_dir = Path(tempfile.gettempdir())
            for f in temp_dir.glob("test_download_opus.*"):
                size = f.stat().st_size
                print(f"✅ File: {f} - Size: {size} bytes")
                if size > 1000000:  # At least 1MB
                    print("✅ File size looks reasonable")
                else:
                    print("⚠️ File size is small")
                return True
            print("❌ No downloaded file found")
            return False
        except Exception as e:
            print(f"❌ Download failed: {e}")
            return False

if __name__ == "__main__":
    success = test_download()
    if success:
        print("\n🎉 Download test passed - YouTube download is working")
    else:
        print("\n💥 Download test failed - check network connection")
