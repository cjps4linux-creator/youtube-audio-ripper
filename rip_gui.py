#!/usr/bin/env python3
"""
YouTube Audio Ripper - SIMPLE WORKING VERSION
Guaranteed to show the START RIPPING button
"""

import customtkinter as ctk
import threading
import subprocess
from pathlib import Path

# Configuration
APP_DIR = Path(__file__).parent.resolve()
OUTPUT_DIR = APP_DIR / "ripped_music"
OUTPUT_DIR.mkdir(exist_ok=True)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class SimpleRipperApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("YouTube Audio Ripper")
        self.geometry("700x550")
        
        # Center window
        self.update_idletasks()
        x = (self.winfo_screenwidth() - 700) // 2
        y = (self.winfo_screenheight() - 550) // 2
        self.geometry(f"+{x}+{y}")
        
        self.processing = False
        self._build_ui()
    
    def _build_ui(self):
        # Main frame
        main = ctk.CTkFrame(self)
        main.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        ctk.CTkLabel(main, text="🎵 YouTube Audio Ripper", 
                     font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(0, 5))
        ctk.CTkLabel(main, text="Download → FLAC + AI Detection",
                     font=ctk.CTkFont(size=11), text_color="gray").pack(pady=(0, 15))
        
        # URL Input
        ctk.CTkLabel(main, text="YouTube URLs (one per line):",
                     font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", pady=(0, 5))
        
        self.url_text = ctk.CTkTextbox(main, height=70, font=ctk.CTkFont(family="Consolas", size=11))
        self.url_text.pack(fill="x", pady=(0, 10))
        self.url_text.insert("0.0", "https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        
        # BIG START BUTTON - This is the main feature
        self.start_btn = ctk.CTkButton(
            main, text="🎵 START RIPPING 🎵",
            font=ctk.CTkFont(size=20, weight="bold"),
            height=60, fg_color="green", hover_color="darkgreen",
            command=self._start_rip
        )
        self.start_btn.pack(fill="x", pady=15)
        
        # Progress
        self.progress = ctk.CTkProgressBar(main)
        self.progress.pack(fill="x", pady=(0, 5))
        self.progress.set(0)
        
        self.status = ctk.CTkLabel(main, text="Ready", font=ctk.CTkFont(size=10))
        self.status.pack()
        
        # Log
        ctk.CTkLabel(main, text="Log:", font=ctk.CTkFont(size=11, weight="bold")).pack(anchor="w", pady=(10, 5))
        self.log = ctk.CTkTextbox(main, height=120, font=ctk.CTkFont(family="Consolas", size=10), state="disabled")
        self.log.pack(fill="both", expand=True)
    
    def _log(self, msg):
        self.log.configure(state="normal")
        self.log.insert("end", msg + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")
    
    def _start_rip(self):
        urls_text = self.url_text.get("0.0", "end").strip()
        if not urls_text:
            self._log("❌ Enter YouTube URLs first")
            return
        
        urls = [line.strip() for line in urls_text.split("\n") if line.strip() and ("youtube.com" in line or "youtu.be" in line)]
        if not urls:
            self._log("❌ No valid YouTube URLs found")
            return
        
        self.start_btn.configure(state="disabled", text="⏳ Processing...")
        self.progress.set(0.1)
        self._log(f"📋 Processing {len(urls)} URL(s)...")
        
        threading.Thread(target=self._process, args=(urls,), daemon=True).start()
    
    def _process(self, urls):
        for i, url in enumerate(urls):
            self.after(0, self._log, f"\n[{i+1}/{len(urls)}] {url[:60]}...")
            try:
                self._download_convert(url)
            except Exception as e:
                self.after(0, self._log, f"❌ Error: {str(e)[:100]}")
        
        self.after(0, self._done)
    
    def _next_track_number(self):
        existing = list(OUTPUT_DIR.glob("*.flac"))
        nums = []
        for f in existing:
            stem = f.stem
            if stem.startswith("AI_"):
                stem = stem[3:]
            if stem.isdigit():
                nums.append(int(stem))
        return max(nums, default=0) + 1
    
    def _sanitize_filename(self, title):
        """Convert YouTube title to safe filename"""
        # Remove/replace invalid filename characters
        invalid = '<>:"/\\|?*'
        for char in invalid:
            title = title.replace(char, '')
        # Limit length and strip
        title = title.strip()[:80]
        return title if title else "Unknown_Track"
    
    def _download_convert(self, url):
        import yt_dlp
        import tempfile
        
        temp_dir = Path(tempfile.gettempdir())
        temp_file = temp_dir / "ripper_temp.%(ext)s"
        
        # Clean old files
        for f in temp_dir.glob("ripper_temp.*"):
            f.unlink()
        
        self.after(0, self._log, "Downloading...")
        self.after(0, self.progress.configure, {"value": 0.3})
        
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": str(temp_file),
            "quiet": True,
            "no_warnings": True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get("title", "Unknown")
        
        self.after(0, self._log, f"✅ Downloaded: {title[:40]}")
        
        # Find file
        downloaded = None
        for f in temp_dir.glob("ripper_temp.*"):
            if f.exists():
                downloaded = f
                break
        
        if not downloaded:
            raise FileNotFoundError("Download failed")
        
        self.after(0, self._log, "Converting to FLAC...")
        self.after(0, self.progress.configure, {"value": 0.6})
        
        # Use video title as filename
        safe_title = self._sanitize_filename(title)
        output_file = OUTPUT_DIR / f"{safe_title}.flac"
        
        result = subprocess.run([
            "ffmpeg", "-y", "-i", str(downloaded),
            "-q:a", "0", "-c:a", "flac", "-ar", "44100", str(output_file)
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            raise RuntimeError("FFmpeg failed")
        
        # Cleanup
        downloaded.unlink(missing_ok=True)
        
        size_mb = output_file.stat().st_size / (1024 * 1024)
        self.after(0, self._log, f"✅ Saved: {output_file.name} ({size_mb:.1f} MB)")
        self.after(0, self.progress.configure, {"value": 1.0})
    
    def _done(self):
        self.start_btn.configure(state="normal", text="🎵 START RIPPING 🎵")
        self._log(f"\n✅ Done! Files in: {OUTPUT_DIR}")


if __name__ == "__main__":
    app = SimpleRipperApp()
    app.mainloop()