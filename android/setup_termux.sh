#!/data/data/com.termux/files/usr/bin/bash
# YouTube Audio Ripper - Termux Setup Script
# Run this inside Termux to set up everything automatically

set -e

echo "========================================"
echo " YouTube Audio Ripper - Termux Setup"
echo "========================================"
echo ""

# 1. Update packages
echo "[1/5] Updating Termux packages..."
pkg update -y && pkg upgrade -y

# 2. Install dependencies
echo "[2/5] Installing dependencies..."
pkg install -y python nodejs ffmpeg openssl git

# 3. Verify Python version
echo "[3/5] Checking Python..."
PYTHON_VERSION=$(python --version 2>&1 | grep -oP '\d+\.\d+')
echo "  Python: $PYTHON_VERSION"

# 4. Install yt-dlp
echo "[4/5] Installing yt-dlp..."
pip install --upgrade yt-dlp

# 5. Create directories
echo "[5/5] Creating directories..."
mkdir -p ~/storage/shared/Music
mkdir -p ~/storage/shared/YouTubeAudioRipper
mkdir -p ~/.shortcuts/tasks/yt-ripper

echo ""
echo "========================================"
echo " Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Copy the app files to your phone:"
echo "   Push ripper_server.py, convert_cookies.py, and static/ to:"
echo "   ~/storage/shared/YouTubeAudioRipper/"
echo ""
echo "   From your Windows PC:"
echo "   adb push C:\\Users\\user\\youtube-audio-ripper\\android\\* /sdcard/YouTubeAudioRipper/"
echo "   adb push C:\\Users\\user\\youtube-audio-ripper\\android\\static /sdcard/YouTubeAudioRipper/"
echo ""
echo "2. Optional: Copy cookies.txt if you use auth:"
echo "   adb push C:\\Users\\user\\youtube-audio-ripper\\cookies.txt /sdcard/YouTubeAudioRipper/"
echo ""
echo "3. Install Termux:API from F-Droid for widget support"
echo ""
echo "4. Run the ripper:"
echo "   cd ~/storage/shared/YouTubeAudioRipper"
echo "   python ripper_server.py"
echo ""
echo "5. Open browser to http://localhost:8080"
echo ""
echo "Node.js: $(node --version 2>/dev/null || echo 'not found')"
echo "FFmpeg:  $(ffmpeg -version 2>/dev/null | head -1 || echo 'not found')"
echo "yt-dlp:  $(yt-dlp --version 2>/dev/null || echo 'not found')"
echo ""
echo "Music folder: ~/storage/shared/Music/"
echo "App folder:   ~/storage/shared/YouTubeAudioRipper/"
