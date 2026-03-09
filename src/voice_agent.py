"""
Jarvis voice agent – ভয়েসে বলো, ভয়েসে জবাব পাবে (বাংলা সমর্থন)
"""

import sys
import os
_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _root not in sys.path:
    sys.path.insert(0, _root)

try:
    import config
except ImportError:
    config = None

from src.ai.chat import chat_with_jarvis
from src.speech.listen import listen_from_mic
from src.speech.speak import speak_text
from src.control.pc_control import handle_control_intent, sleep_pc

# ভয়েসে বন্ধ করতে বললে exit (বাংলা + ইংরেজি)
EXIT_PHRASES = (
    "quit", "exit", "bye", "stop", "বন্ধ করো", "বন্ধ কর", "থামো", "থাম",
    "exit কর", "কুইট", "বাই", "স্টপ"
)


def _should_exit(text: str) -> bool:
    if not text:
        return False
    t = text.strip().lower()
    return t in EXIT_PHRASES or any(t == p for p in EXIT_PHRASES)


def run_jarvis(voice_only: bool = True):
    """Main loop: মাইক থেকে শোনো → ভয়েস ভেরিফাই → কন্ট্রোল বা AI → কণ্ঠে জবাব।"""
    voice_auth = getattr(config, "VOICE_AUTH_ENABLED", False) if config else False
    if voice_auth:
        from src.voice_auth import is_enrolled
        if not is_enrolled():
            print("ভয়েস প্রোফাইল নেই। প্রথমে এনরোল করুন:")
            print("  python -m src.voice_enroll")
            print("তারপর আবার main.py চালান।\n")
            return

    if voice_only:
        print("Jarvis ভয়েস মোড। শুধু তোমার ভয়েসে কাজ করবে।")
        print("অন্য কেউ বললে PC স্লিপে যাবে।")
        print("বন্ধ করতে বলুন: বন্ধ করো / quit / exit\n")
    else:
        print("Jarvis ready. Type below or use voice. 'quit' to exit.\n")

    while True:
        try:
            if voice_only:
                out = listen_from_mic(return_audio_path=voice_auth)
                if voice_auth and isinstance(out, tuple):
                    user_input, wav_path = out
                else:
                    user_input, wav_path = (out if isinstance(out, str) else "", None)
                if wav_path:
                    try:
                        from src.voice_auth import verify_voice
                        if not verify_voice(wav_path):
                            print("অপরিচিত ভয়েস। PC স্লিপে যাচ্ছে...")
                            sleep_pc()
                            continue
                    finally:
                        try:
                            os.unlink(wav_path)
                        except Exception:
                            pass
                if not user_input:
                    print("কিছু শোনা যায়নি, আবার বলুন...")
                    continue
                print("You (ভয়েস):", user_input)
            else:
                user_input = input("You: ").strip()
                if not user_input:
                    continue

            if _should_exit(user_input):
                speak_text("বাই, ভালো থাকুন।")
                break

            # 1) PC কন্ট্রোল চেষ্টা করো
            reply = handle_control_intent(user_input)
            if reply is None:
                # 2) না হলে AI কে জিজ্ঞেস করো
                reply = chat_with_jarvis(user_input)

            print("Jarvis:", reply)
            speak_text(reply)
        except KeyboardInterrupt:
            print("\nবাই।")
            speak_text("বাই।")
            break
        except Exception as e:
            print("Error:", e)
            speak_text("একটু সমস্যা হয়েছে, আবার বলুন।")


if __name__ == "__main__":
    # ভয়েস-অনলি: True = শুধু মাইক, False = টাইপ বা ভয়েস দুটোই
    run_jarvis(voice_only=True)
