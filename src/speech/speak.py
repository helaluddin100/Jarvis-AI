"""
Text-to-Speech – pyttsx3 (offline) + gTTS for Bangla (free)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

try:
    import config
except ImportError:
    config = None


def _has_bangla(text: str) -> bool:
    """Check if text contains Bengali script."""
    for c in text:
        if "\u0980" <= c <= "\u09FF":
            return True
    return False


def speak_text(text: str) -> None:
    """Speak text – Bangla থাকলে gTTS (ভালো উচ্চারণ), নাহলে pyttsx3."""
    if not text:
        return
    use_gtts_bangla = getattr(config, "TTS_USE_GTTS_FOR_BANGLA", True) if config else True
    if use_gtts_bangla and _has_bangla(text):
        try:
            from gtts import gTTS
            import tempfile
            import subprocess
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                tmp = f.name
            tts = gTTS(text=text, lang="bn", slow=False)
            tts.save(tmp)
            # macOS: afplay দিয়ে চালাও
            subprocess.run(["afplay", tmp], check=True, timeout=30)
            try:
                os.unlink(tmp)
            except Exception:
                pass
            return
        except Exception as e:
            print("gTTS error (fallback to pyttsx3):", e)
    try:
        import pyttsx3
        engine = pyttsx3.init()
        if config:
            engine.setProperty("rate", getattr(config, "TTS_RATE", 150))
            engine.setProperty("volume", getattr(config, "TTS_VOLUME", 1.0))
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print("Speak error:", e)
