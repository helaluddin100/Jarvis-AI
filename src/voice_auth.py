"""
ভয়েস ভেরিফিকেশন – শুধু তোমার ভয়েসে কাজ করবে।
অন্য কেউ বললে PC স্লিপে চলে যাবে।
"""

import os
import sys
from pathlib import Path

_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _root not in sys.path:
    sys.path.insert(0, _root)

try:
    import config
except ImportError:
    config = None

# ভয়েস প্রোফাইল সেভ করা পাথ
DEFAULT_PROFILE_PATH = os.path.join(_root, "data", "voice_profile.npy")
# কত উপরে থাকলে "তোমার ভয়েস" ধরা হবে (০ থেকে ১, যত বেশি তত কড়া)
SIMILARITY_THRESHOLD = 0.70


def _get_profile_path() -> str:
    p = getattr(config, "VOICE_PROFILE_PATH", None) if config else None
    if p and not os.path.isabs(p):
        p = os.path.join(_root, p)
    return p or DEFAULT_PROFILE_PATH


def _get_threshold() -> float:
    return getattr(config, "VOICE_SIMILARITY_THRESHOLD", SIMILARITY_THRESHOLD) if config else SIMILARITY_THRESHOLD


def _ensure_resemblyzer():
    try:
        from resemblyzer import preprocess_wav, VoiceEncoder
        return preprocess_wav, VoiceEncoder
    except ImportError:
        print("resemblyzer লাগবে। চালাও: pip install resemblyzer")
        sys.exit(1)


def enroll_voice(samples: int = 3, duration_sec: int = 5) -> bool:
    """
    তোমার ভয়েস রেকর্ড করে প্রোফাইল বানাবে।
    samples = কতবার বলতে হবে (২–৩ ভালো)
    """
    preprocess_wav, VoiceEncoder = _ensure_resemblyzer()
    import speech_recognition as sr
    import numpy as np

    profile_dir = os.path.dirname(_get_profile_path())
    os.makedirs(profile_dir, exist_ok=True)

    r = sr.Recognizer()
    encoder = VoiceEncoder()
    wavs = []

    print("ভয়েস এনরোলমেন্ট। প্রতিবার একই বাক্য বলুন, যেমন: আমি জারভিসের মালিক")
    for i in range(samples):
        print(f"\n[{i+1}/{samples}] এখন বলুন...")
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.record(source, duration=duration_sec)
        wav_bytes = audio.get_wav_data()
        tmp_path = os.path.join(profile_dir, f"_enroll_{i}.wav")
        with open(tmp_path, "wb") as f:
            f.write(wav_bytes)
        try:
            wav = preprocess_wav(Path(tmp_path))
            wavs.append(wav)
        finally:
            try:
                os.unlink(tmp_path)
            except Exception:
                pass

    if len(wavs) < 1:
        print("কোনো স্যাম্পল রেকর্ড হয়নি।")
        return False

    embed = encoder.embed_speaker(wavs)
    profile_path = _get_profile_path()
    np.save(profile_path, embed)
    print(f"\nভয়েস প্রোফাইল সেভ হয়েছে: {profile_path}")
    return True


def verify_voice(audio_wav_path: str) -> bool:
    """
    রেকর্ড করা অডিও তোমার ভয়েস কিনা চেক করে।
    True = তুমি, False = অপরিচিত → PC স্লিপ
    """
    if not os.path.isfile(audio_wav_path):
        return False
    profile_path = _get_profile_path()
    if not os.path.isfile(profile_path):
        # এনরোল হয়নি – প্রথমবার সব allow (অথবা False করে ব্লক)
        return True  # enrollment না করলে সব allow করি; user কে enroll করতে বলব
    preprocess_wav, VoiceEncoder = _ensure_resemblyzer()
    import numpy as np

    try:
        encoder = VoiceEncoder()
        profile = np.load(profile_path)
        wav = preprocess_wav(Path(audio_wav_path))
        if len(wav) < 16000:  # 1 sec minimum
            return False
        embed = encoder.embed_utterance(wav)
        sim = float(np.inner(profile, embed))
        threshold = _get_threshold()
        return sim >= threshold
    except Exception as e:
        print("Verify error:", e)
        return False


def is_enrolled() -> bool:
    return os.path.isfile(_get_profile_path())
