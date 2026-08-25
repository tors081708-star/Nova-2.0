"""
Unit and integration tests for NOVA 2.0 modules.
"""

import unittest
import os
import tempfile
from nova.memory.user_profile import UserProfile
from nova.memory.conversation_history import ConversationHistory
from nova.voice.voice_interface import VoiceInterface
from nova.agents.core.nova_mind import NovaMind

class TestNovaModules(unittest.TestCase):

    def test_user_profile(self):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            path = f.name
        profile = UserProfile(name="Alice", config_path=path)
        profile.save()

        loaded = UserProfile.load(config_path=path)
        self.assertEqual(loaded.name, "Alice")
        os.remove(path)

    def test_conversation_history(self):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            path = f.name
        history = ConversationHistory(db_path=path)
        history.add_entry("user", "Hello")
        self.assertEqual(len(history.get_recent()), 1)
        os.remove(path)

    def test_nova_mind_todo(self):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            path = f.name
        mind = NovaMind(storage_path=path)
        task = mind.add_task("Buy milk")
        self.assertEqual(len(mind.get_all_tasks()), 1)
        self.assertEqual(task.title, "Buy milk")

        toggled = mind.toggle_task(task.id)
        self.assertTrue(toggled.completed)

        deleted = mind.delete_task(task.id)
        self.assertTrue(deleted)
        self.assertEqual(len(mind.get_all_tasks()), 0)
        os.remove(path)

if __name__ == "__main__":
    unittest.main()
