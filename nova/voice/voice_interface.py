"""
Voice Interface module for Nova 2.0.
Speech-to-text (Whisper fallback) and text-to-speech (pyttsx3 fallback).
"""

import sys

try:
  import pyttsx3
except ImportError:
  pyttsx3 = None

try:
  import whisper
except ImportError:
  whisper = None


class VoiceInterface:

  def __init__(self, enabled: bool = True):
    self.enabled = enabled
    self.tts_engine = None
    if pyttsx3 and self.enabled:
      try:
        self.tts_engine = pyttsx3.init()
      except Exception:
        self.tts_engine = None

  def speak(self, text: str) -> None:
    """Converts text to speech if TTS engine is available."""
    print(f"[NOVA Voice Output]: {text}")
    if self.tts_engine:
      try:
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
      except Exception as e:
        print(f"[Voice TTS Warning]: {e}", file=sys.stderr)

  def listen(self, audio_file_path: str = None) -> str:
    """Converts speech to text using Whisper if available, or accepts textual input."""
    if audio_file_path and whisper:
      try:
        model = whisper.load_model("base")
        result = model.transcribe(audio_file_path)
        return result.get("text", "")
      except Exception as e:
        print(f"[Voice STT Error]: {e}", file=sys.stderr)
        return ""
    return ""
