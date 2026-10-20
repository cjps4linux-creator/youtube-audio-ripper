#!/usr/bin/env python3
"""
Test: Download public video and convert to FLAC
"""

import yt_dlp
import subprocess
import tempfile
from pathlib import Path

# Test with Rickroll (public video)
url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
temp_dir = Path(tempfile.gettempdir())
output_dir = Path("C:/Users/user/youtube-audio-ripper/ripped_music")
output_dir.mkdir(exist_ok=True)

print("=" * 60)
print("YouTube Audio Ripper - Test")
print("=" * 60)

# Step 1: Download
print("\n[1/3] Downloading audio...")
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'opus',
        'preferredquality': '192',
    }],
    'outtmpl': str(temp_dir / "test_audio.%(ext)s"),
    'quiet': True,
    'no_warnings': True,
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(url, download=True)
    title = info.get('title', 'Unknown')
    print(f"✅ Downloaded: {title}")

# Find downloaded file
downloaded_file = None
for f in temp_dir.glob("test_audio.*"):
    if f.exists():
        downloaded_file = f
        break

if not downloaded_file:
    print("❌ No downloaded file found")
    exit(1)

print(f"✅ File: {downloaded_file} - Size: {downloaded_file.stat().st_size} bytes")

# Step 2: Convert to FLAC
print("\n[2/3] Converting to FLAC...")
output_file = output_dir / "001.flac"

cmd = [
    'ffmpeg', '-y', '-i', str(downloaded_file),
    '-q:a', '0', '-c:a', 'flac', '-ar', '44100',
    str(output_file)
]

result = subprocess.run(cmd, capture_output=True, text=True)

if result.returncode != 0:
    print(f"❌ Conversion failed: {result.stderr}")
    exit(1)

print(f"✅ Converted to FLAC: {output_file}")
print(f"   Size: {output_file.stat().st_size} bytes")

# Step 3: Cleanup
downloaded_file.unlink(missing_ok=True)
print("\n[3/3] Cleanup complete")

print("\n" + "=" * 60)
print("✅ TEST PASSED - YouTube audio ripper is working!")
print(f"   Output: {output_file}")
print("=" * 60)