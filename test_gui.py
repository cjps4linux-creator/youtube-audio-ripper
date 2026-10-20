#!/usr/bin/env python3
"""
Quick test of YouTube Audio Ripper GUI
"""

import customtkinter as ctk
from pathlib import Path

# Configure appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Create main window
app = ctk.CTk()
app.title("YouTube Audio Ripper - Test")
app.geometry("700x600")

# Simple test button
btn = ctk.CTkButton(app, text="🧪 Test Button", font=ctk.CTkFont(size=14, weight="bold"))
btn.pack(expand=True, fill="both", padx=20, pady=20)

print("GUI initialized - check if window appears")
app.mainloop()
