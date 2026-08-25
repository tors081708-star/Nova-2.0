"""
Conversation History and Learning Engine module for Nova 2.0.
Logs conversation DB, learning context, and retrieval engine.
"""

import json
import os
import time
from typing import Any, Dict, List


class ConversationHistory:

  def __init__(self, db_path: str = None):
    self.db_path = db_path or os.path.expanduser(
        "~/.nova_conversation_history.json"
    )
    self.history: List[Dict[str, Any]] = []
    self._load()

  def _load(self) -> None:
    if os.path.exists(self.db_path):
      try:
        with open(self.db_path, "r", encoding="utf-8") as f:
          self.history = json.load(f)
      except Exception:
        self.history = []

  def save(self) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(self.db_path)), exist_ok=True)
    with open(self.db_path, "w", encoding="utf-8") as f:
      json.dump(self.history, f, indent=2)

  def add_entry(
      self, role: str, content: str, metadata: Dict[str, Any] = None
  ) -> Dict[str, Any]:
    entry = {
        "timestamp": time.time(),
        "role": role,
        "content": content,
        "metadata": metadata or {},
    }
    self.history.append(entry)
    self.save()
    return entry

  def get_recent(self, limit: int = 10) -> List[Dict[str, Any]]:
    return self.history[-limit:]

  def clear(self) -> None:
    self.history = []
    self.save()
