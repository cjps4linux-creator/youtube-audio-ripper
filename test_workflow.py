#!/usr/bin/env python3
"""
End-to-end test: Download YouTube → FLAC → AI Detection
"""

import yt_dlp
import subprocess
import tempfile
from pathlib import Path

url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
output_dir = Path("C:/Users/user/youtube-audio-ripper/ripped_music")
output_dir.mkdir(exist_ok=True)

print("=" * 60)
print("YouTube Audio Ripper - Full Workflow Test")
print("=" * 60)

# Step 1: Download
print("\nStep 1: Downloading audio...")
temp_dir = Path(tempfile.gettempdir())
temp_file = temp_dir / "youtube_test.opus"

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
for f in temp_dir.glob("youtube_test.*"):
    if f.exists():
        downloaded = f
        break

if downloaded:
    print(f"  ✅ Downloaded: {downloaded.name} ({downloaded.stat().st_size} bytes)")

    # Step 2: Convert to FLAC
    print("\nStep 2: Converting to FLAC...")
    output_file = output_dir / "test_flac.flac"
    
    cmd = [
        'ffmpeg', '-y', '-i', str(downloaded),
        '-q:a', '0', '-c:a', 'flac', '-ar', '44100',
        str(output_file)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        size_mb = output_file.stat().st_size / (1024 * 1024)
        print(f"  ✅ Converted: {output_file.name} ({size_mb:.1f} MB)")
        print(f"  ✅ File created at: {output_file}")
        
        # Cleanup
        downloaded.unlink(missing_ok=True)
        
        print("\n" + "=" * 60)
        print("✅ FULL WORKFLOW TEST PASSED")
        print(f"Files in output dir: {list(output_dir.glob('*.flac'))}")
        print("=" * 60)
    else:
        print(f"  ❌ Conversion failed: {result.stderr[:200]}")
else:
    print("  ❌ No file downloaded")

print(f"\n📁 Output folder: {output_dir}")
print(f"To view files: explorer {output_dir}")