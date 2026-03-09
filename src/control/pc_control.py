"""
PC control – run commands, open apps (all free, no API)
"""
from __future__ import annotations

import subprocess
import sys
import platform
import re

IS_MAC = platform.system() == "Darwin"


def sleep_pc() -> None:
    """PC কে স্লিপ মোডে পাঠাও (অপরিচিত ভয়েস হলে)।"""
    if IS_MAC:
        subprocess.run(["pmset", "sleepnow"], check=False, timeout=5)
    else:
        # Linux
        subprocess.run(["systemctl", "suspend"], check=False, timeout=5)


def execute_command(cmd: str) -> tuple[bool, str]:
    """Run a shell command safely. Returns (success, output)."""
    if not cmd or not cmd.strip():
        return False, "Empty command"
    try:
        result = subprocess.run(
            cmd.strip(),
            shell=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
        out = (result.stdout or "").strip() or (result.stderr or "").strip()
        return result.returncode == 0, out or "Done"
    except subprocess.TimeoutExpired:
        return False, "Command timed out"
    except Exception as e:
        return False, str(e)


def handle_control_intent(text: str) -> str | None:
    """
    Parse simple voice commands and run PC control.
    Returns reply string if we handled it, else None (so AI can reply).
    """
    t = text.lower().strip()

    # Open app (macOS)
    if IS_MAC:
        if "open" in t and ("browser" in t or "chrome" in t or "safari" in t):
            ok, out = execute_command("open -a Safari")
            return "Opening Safari." if ok else out
        if "open" in t and "terminal" in t:
            ok, out = execute_command("open -a Terminal")
            return "Opening Terminal." if ok else out
        if "open" in t and "finder" in t:
            ok, out = execute_command("open -a Finder")
            return "Opening Finder." if ok else out

    # Volume (macOS: osascript)
    if "volume" in t or "sound" in t:
        if "mute" in t or "silent" in t:
            if IS_MAC:
                execute_command("osascript -e 'set volume output muted true'")
            return "Muted."
        if "unmute" in t:
            if IS_MAC:
                execute_command("osascript -e 'set volume output muted false'")
            return "Unmuted."

    # Generic: "run command ..." or "execute ..."
    if t.startswith("run command") or t.startswith("execute"):
        cmd = re.sub(r"^(run command|execute)\s+", "", t, flags=re.I).strip()
        if cmd:
            ok, out = execute_command(cmd)
            return out if out else ("Done." if ok else "Failed.")
    return None
