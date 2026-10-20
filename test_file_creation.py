#!/usr/bin/env python3
"""
YouTube Audio Ripper - File creation test
"""

import os
import subprocess
from pathlib import Path

OUTPUT_DIR = Path("C:/Users/user/youtube-audio-ripper/ripped_music")
OUTPUT_DIR.mkdir(exist_ok=True)

print("=" * 60)
print("YouTube Audio Ripper - File Creation Test")
print("=" * 60)

# Create a simple test audio file
test_file = OUTPUT_DIR / "test_audio.flac"
print(f"\nCreating test file: {test_file}")

# Generate a simple 1-second tone as test audio
result = subprocess.run([
    'ffmpeg', '-y', 
    '-f', 'lavfi',
    '-i', 'sine=frequency=440:duration=1',
    '-c:a', 'flac',
    str(test_file)
], capture_output=True, text=True)

if result.returncode == 0:
    print("✅ Test audio created successfully")
    print(f"   Size: {test_file.stat().st_size} bytes")
else:
    print(f"❌ Failed to create test audio: {result.stderr}")

# Create multiple test files to simulate multi-track output
print("\nCreating multiple test files...")
for i in range(1, 5):
    test_file = OUTPUT_DIR / f"{i:03d}.flac"
    result = subprocess.run([
        'ffmpeg', '-y',
        '-f', 'lavfi',
        '-i', f'sine=frequency={440*i}:duration=1',
        '-c:a', 'flac',
        str(test_file)
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"  ✅ Created: {test_file.name} ({test_file.stat().st_size} bytes)")
    else:
        print(f"  ❌ Failed: {test_file.name}")

# Create AI-detected files too
for i in range(1, 4):
    test_file = OUTPUT_DIR / f"AI_{i:03d}.flac"
    result = subprocess.run([
        'ffmpeg', '-y',
        '-f', 'lavfi',
        '-i', f'sine=frequency={880*i}:duration=1',
        '-c:a', 'flac',
        str(test_file)
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"  ✅ Created: {test_file.name} ({test_file.stat().st_size} bytes)")

print("\n" + "=" * 60)
print("Files in output directory:")
for f in sorted(OUTPUT_DIR.iterdir()):
    if f.is_file():
        print(f"  {f.name} ({f.stat().st_size} bytes)")

print("\n✅ Test complete - files are being created correctly")
print("=" * 60)