#!/data/data/com.termux/files/usr/bin/bash
# Termux Widget Launcher - YouTube Audio Ripper
# Place this at: ~/.shortcuts/tasks/yt-ripper/script.sh

# Kill any existing instance
pkill -f "ripper_server.py" 2>/dev/null || true

# Start the server in background
cd ~/storage/shared/YouTubeAudioRipper
nohup python ripper_server.py > /dev/null 2>&1 &

# Give it a moment to start
sleep 2

# Open in browser
termux-open-url http://localhost:8080
