#!/usr/bin/env python3
"""
Jarvis – Personal AI Assistant
কথা বলা + লোকাল PC কন্ট্রোল (সব ফ্রি API)
"""

import sys

def main():
    print("Jarvis – Personal AI Assistant")
    print("Loading... (config from config.py)")
    try:
        from src.voice_agent import run_jarvis
        run_jarvis()
    except ImportError as e:
        print("Module not ready:", e)
        print("Run: pip install -r requirements.txt")
        print("Then ensure Ollama is running: ollama pull llama3.2")
        sys.exit(1)

if __name__ == "__main__":
    main()
