"""
ভয়েস এনরোলমেন্ট – প্রথমবার চালাও, তোমার ভয়েস সেভ হবে।
তারপর শুধু তোমার ভয়েসেই জারভিস কাজ করবে।
"""

import sys
import os

_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _root not in sys.path:
    sys.path.insert(0, _root)

from src.voice_auth import enroll_voice

if __name__ == "__main__":
    print("=" * 50)
    print("Jarvis – ভয়েস এনরোলমেন্ট")
    print("=" * 50)
    ok = enroll_voice(samples=3, duration_sec=5)
    if ok:
        print("\nসফল! এখন python main.py চালিয়ে জারভিস ব্যবহার করুন।")
        print("শুধু তোমার ভয়েসেই কাজ করবে। অন্য কেউ বললে PC স্লিপে যাবে।")
    else:
        sys.exit(1)
