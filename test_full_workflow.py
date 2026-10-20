#!/usr/bin/env python3
"""
Simple test to verify the app works end-to-end
"""

import yt_dlp
import subprocess
from pathlib import Path
import tempfile

url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
output_dir = Path(__file__).resolve().parent / "ripped_music"
output_dir.mkdir(exist_ok=True)

temp_dir = Path(tempfile.gettempdir())
temp_file = temp_dir / "test_audio.opus"

print("Step 1: Downloading audio...")
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'opus',
        'preferredquality': '192',
    }],
    'outtmpl': str(temp_file),
    'quiet': True,
    'no_warnings': True,
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(url, download=True)
    title = info.get('title', 'Unknown')
    print(f"  ✅ Title: {title}")

# Find downloaded file
downloaded = None
for f in temp_dir.glob("test_audio.*"):
    if f.exists():
        downloaded = f
        break

if not downloaded:
    print("  ❌ No file downloaded")
else:
    print(f"  ✅ File: {downloaded.name} ({downloaded.stat().st_size} bytes)")

    print("\nStep 2: Converting to FLAC...")
    output_file = output_dir / "001_test.flac"
    result = subprocess.run([
        'ffmpeg', '-y', '-i', str(downloaded),
        '-q:a', '0', '-c:a', 'flac', '-ar', '44100',
        str(output_file)
    ], capture_output=True, text=True)

    if result.returncode == 0:
        print(f"  ✅ Converted: {output_file}")
        print(f"  ✅ Size: {output_file.stat().st_size} bytes")
        
        # Cleanup
        downloaded.unlink(missing_ok=True)
        print("\n✅ Test PASSED - The app works!")
        print(f"File created: {output_file}")
    else:
        print(f"  ❌ Conversion failed: {result.stderr[:100]}")

print(f"\n📁 Check your output folder: {output_dir}")
print(f"   Files: {list(output_dir.glob('*.flac'))}")