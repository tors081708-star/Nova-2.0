"""
User Profile module for Nova 2.0.
Manages personality, preferences, timezone, style, voice, and autonomy settings.
"""

import json
import os
from typing import Any, Dict


class UserProfile:

  def __init__(
      self,
      name: str = "Developer",
      timezone: str = "UTC",
      style: str = "Concise and helpful",
      voice: str = "en-US-Standard",
      autonomy: str = "autonomous",
      config_path: str = None,
  ):
    self.name = name
    self.timezone = timezone
    self.style = style
    self.voice = voice
    self.autonomy = autonomy
    self.config_path = config_path or os.path.expanduser(
        "~/.nova_user_profile.json"
    )

  def to_dict(self) -> Dict[str, Any]:
    return {
        "name": self.name,
        "timezone": self.timezone,
        "style": self.style,
        "voice": self.voice,
        "autonomy": self.autonomy,
    }

  def save(self) -> None:
    os.makedirs(
        os.path.dirname(os.path.abspath(self.config_path)), exist_ok=True
    )
    with open(self.config_path, "w", encoding="utf-8") as f:
      json.dump(self.to_dict(), f, indent=2)

  @classmethod
  def load(cls, config_path: str = None) -> "UserProfile":
    path = config_path or os.path.expanduser("~/.nova_user_profile.json")
    if os.path.exists(path):
      try:
        with open(path, "r", encoding="utf-8") as f:
          data = json.load(f)
        return cls(config_path=path, **data)
      except Exception:
        pass
    return cls(config_path=path)
