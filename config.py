"""
Jarvis – Configuration (all free APIs)
"""

# AI: "ollama" = local (free), "groq" = cloud free tier
AI_PROVIDER = "ollama"
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "llama3.2"
# Groq: get free API key from https://console.groq.com
GROQ_API_KEY = ""
GROQ_MODEL = "llama-3.1-8b-instant"

# Speech: listen (mic -> text)
# "google" = free online, "whisper" = local (install openai-whisper)
STT_ENGINE = "google"
# বাংলা + ইংরেজি: "bn-BD" = Bengali (Bangladesh), "en-US" = English
# একসাথে চাইলে প্রথমে bn-BD চেষ্টা, না পেলে en-US
STT_LANGUAGE = "bn-BD"
STT_LANGUAGE_FALLBACK = "en-US"
# কত সেকেন্ড কথা শুনবে (লম্বা বাক্যের জন্য বাড়াও)
LISTEN_DURATION_SEC = 6

# Speech: speak (text -> voice)
# "pyttsx3" = offline, "gtts" = Bangla সহ ভালো (অনলাইন ফ্রি)
TTS_ENGINE = "pyttsx3"
TTS_RATE = 150
TTS_VOLUME = 1.0
# বাংলা টেক্সট থাকলে gTTS ব্যবহার করবে (বাংলা উচ্চারণ ভালো)
TTS_USE_GTTS_FOR_BANGLA = True

# Wake word (optional) – বললে জারভিস সক্রিয় হবে
WAKE_WORD = "jarvis"

# ভয়েস সিকিউরিটি – শুধু তোমার ভয়েসে কাজ করবে
# True = অন্য ভয়েসে বললে PC স্লিপে যাবে; False = বন্ধ (সব ভয়েসে কাজ করবে)
VOICE_AUTH_ENABLED = False
VOICE_PROFILE_PATH = "data/voice_profile.npy"
# কত সিমিলার হলে "তোমার ভয়েস" (০–১, বেশি = কড়া)
VOICE_SIMILARITY_THRESHOLD = 0.70
