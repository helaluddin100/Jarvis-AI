"""
AI chat – Ollama (local, free) or Groq (cloud free tier)
"""

import requests
import json

try:
    import config
except ImportError:
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    import config


def chat_with_jarvis(user_message: str, system_prompt: str = None) -> str:
    """Send message to Jarvis AI and return reply. Uses free APIs only."""
    system_prompt = system_prompt or (
        "You are Jarvis, a helpful personal AI assistant. "
        "You can have conversations and help control the user's PC when asked. "
        "Reply briefly and clearly. If the user asks in Bengali, reply in Bengali when appropriate."
    )

    if config.AI_PROVIDER == "ollama":
        return _ollama_chat(user_message, system_prompt)
    if config.AI_PROVIDER == "groq":
        return _groq_chat(user_message, system_prompt)
    return "AI provider not set. Use 'ollama' or 'groq' in config.py"


def _ollama_chat(user_message: str, system_prompt: str) -> str:
    """Ollama local API – 100% free."""
    url = f"{config.OLLAMA_BASE_URL.rstrip('/')}/api/chat"
    payload = {
        "model": config.OLLAMA_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        "stream": False,
    }
    try:
        r = requests.post(url, json=payload, timeout=60)
        r.raise_for_status()
        data = r.json()
        return data.get("message", {}).get("content", "").strip()
    except requests.RequestException as e:
        return f"Ollama error: {e}. Is Ollama running? Try: ollama pull {config.OLLAMA_MODEL}"


def _groq_chat(user_message: str, system_prompt: str) -> str:
    """Groq cloud API – free tier, no card needed."""
    if not config.GROQ_API_KEY:
        return "Groq API key missing. Set GROQ_API_KEY in config.py (get free key: console.groq.com)"
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {config.GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": config.GROQ_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        "max_tokens": 512,
    }
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        r.raise_for_status()
        data = r.json()
        return data["choices"][0]["message"]["content"].strip()
    except requests.RequestException as e:
        return f"Groq error: {e}"
