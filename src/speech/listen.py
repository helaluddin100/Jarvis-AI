"""
Speech-to-Text – Google (free) or Whisper (local free)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

try:
    import config
except ImportError:
    config = None

def listen_from_mic(return_audio_path: bool = False):
    """
    Listen from microphone, return text.
    return_audio_path=True হলে (text, wav_path) দেবে – ভয়েস ভেরিফিকেশনের জন্য।
    """
    engine = getattr(config, "STT_ENGINE", "google") if config else "google"
    if engine == "google":
        return _listen_google(return_audio_path)
    if engine == "whisper":
        return _listen_whisper(return_audio_path)
    return ("", None) if return_audio_path else ""


def _listen_google(return_audio_path: bool = False):
    """Google Speech Recognition – free. Bangla + English supported."""
    import tempfile
    try:
        import speech_recognition as sr
        r = sr.Recognizer()
        duration = getattr(config, "LISTEN_DURATION_SEC", 6) if config else 6
        lang = getattr(config, "STT_LANGUAGE", "bn-BD") if config else "bn-BD"
        fallback = getattr(config, "STT_LANGUAGE_FALLBACK", "en-US") if config else "en-US"
        with sr.Microphone() as source:
            print("Listening... (বলুন বা speak now)")
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.record(source, duration=duration)
        wav_path = None
        if return_audio_path:
            wav_bytes = audio.get_wav_data()
            fd, wav_path = tempfile.mkstemp(suffix=".wav")
            os.close(fd)
            with open(wav_path, "wb") as f:
                f.write(wav_bytes)
        # প্রথমে বাংলা, না পেলে ইংরেজি
        text = None
        try:
            text = r.recognize_google(audio, language=lang)
        except Exception:
            try:
                text = r.recognize_google(audio, language=fallback)
            except Exception:
                pass
        result = (text or "").strip()
        if return_audio_path:
            return result, wav_path
        return result
    except Exception as e:
        print("Listen error:", e)
        return ("", None) if return_audio_path else ""


def _listen_whisper(return_audio_path: bool = False):
    """Whisper local – 100% free. Requires: pip install openai-whisper."""
    try:
        import whisper
        import speech_recognition as sr
        model = whisper.load_model("base")
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening... (Whisper)")
            audio = r.record(source, duration=5)
        # Fallback to google for now
        return _listen_google(return_audio_path)
    except ImportError:
        return _listen_google(return_audio_path)
