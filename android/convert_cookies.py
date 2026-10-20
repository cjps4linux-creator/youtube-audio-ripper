#!/usr/bin/env python3
"""
Convert Brave Android DevTools cookie export to Netscape format
for yt-dlp on Termux/Android.

Usage:
    python convert_cookies.py input.tsv output.txt

Input:  Brave DevTools tab-separated cookie export
Output: Netscape HTTP Cookie File (yt-dlp compatible)
"""

import sys
from datetime import datetime
from pathlib import Path


def convert(input_path: str, output_path: str):
    """Convert Brave DevTools export to Netscape format."""
    p = Path(input_path)
    if not p.exists():
        print(f"Input file not found: {input_path}")
        return False

    lines = p.read_text(encoding="utf-8", errors="replace").strip().splitlines()

    output = ["# Netscape HTTP Cookie File", ""]
    count = 0

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        parts = line.split("\t")
        if len(parts) < 7:
            continue

        # Brave DevTools export columns:
        # 0: Name, 1: Value, 2: Domain, 3: Path, 4: Expires,
        # 5: Size, 6: HttpOnly, 7: HostOnly, 8: Secure, 9: SameSite
        name = parts[0]
        value = parts[1]
        domain = parts[2]
        path = parts[3]
        expires_raw = parts[4]
        http_only = parts[6] if len(parts) > 6 else "FALSE"
        secure = parts[8] if len(parts) > 8 else "FALSE"

        # Convert ISO timestamp to Unix epoch
        try:
            dt = datetime.fromisoformat(expires_raw.replace("Z", "+00:00"))
            expiry = int(dt.timestamp())
        except Exception:
            try:
                expiry = int(float(expires_raw))
            except Exception:
                expiry = 0

        # Domain flag: TRUE if not host-only
        domain_flag = "TRUE" if http_only.upper() != "TRUE" else "FALSE"

        # Secure flag
        secure_flag = "TRUE" if secure.upper() == "TRUE" or secure.upper() == "✓" else "FALSE"

        output.append(f"{domain}\t{domain_flag}\t{path}\t{secure_flag}\t{expiry}\t{name}\t{value}")
        count += 1

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(output) + "\n", encoding="utf-8")
    print(f"Converted {count} cookies -> {output_path}")
    return True


def main():
    if len(sys.argv) < 3:
        print("Usage: python convert_cookies.py <input.tsv> <output.txt>")
        print()
        print("Android/Termux default paths:")
        print("  Input:  ~/storage/shared/Download/cookies.tsv")
        print("  Output: ~/storage/shared/YouTubeAudioRipper/cookies.txt")
        sys.exit(1)

    ok = convert(sys.argv[1], sys.argv[2])
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
