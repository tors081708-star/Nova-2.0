"""
NOVA Mind core module.
Autonomous decision-making, prompt handling, and task/to-do management with local storage.
"""

import json
import os
import uuid
from typing import Any, Dict, List, Optional

from nova.memory.conversation_history import ConversationHistory
from nova.memory.user_profile import UserProfile


class TaskItem:

  def __init__(
      self,
      title: str,
      completed: bool = False,
      task_id: str = None,
      category: str = "general",
      priority: str = "Medium",
      due_date: Optional[str] = None,
  ):
    self.id = task_id or str(uuid.uuid4())
    self.title = title
    self.completed = completed
    self.category = category
    self.priority = priority
    self.due_date = due_date

  def to_dict(self) -> Dict[str, Any]:
    return {
        "id": self.id,
        "title": self.title,
        "completed": self.completed,
        "category": self.category,
        "priority": self.priority,
        "due_date": self.due_date,
    }


class NovaMind:

  def __init__(self, storage_path: str = None):
    self.user_profile = UserProfile.load()
    self.conversation_history = ConversationHistory()
    self.storage_path = storage_path or os.path.expanduser(
        "~/.nova_todo_tasks.json"
    )
    self.tasks: List[TaskItem] = []
    self._load_tasks()

  def _load_tasks(self) -> None:
    if os.path.exists(self.storage_path):
      try:
        with open(self.storage_path, "r", encoding="utf-8") as f:
          data = json.load(f)
          self.tasks = [
              TaskItem(
                  title=item.get("title", ""),
                  completed=item.get("completed", False),
                  task_id=item.get("id"),
                  category=item.get("category", "general"),
                  priority=item.get("priority", "Medium"),
                  due_date=item.get("due_date"),
              )
              for item in data
          ]
      except Exception:
        self.tasks = []

  def _save_tasks(self) -> None:
    os.makedirs(
        os.path.dirname(os.path.abspath(self.storage_path)), exist_ok=True
    )
    with open(self.storage_path, "w", encoding="utf-8") as f:
      json.dump([t.to_dict() for t in self.tasks], f, indent=2)

  def add_task(
      self,
      title: str,
      category: str = "general",
      priority: str = "Medium",
      due_date: Optional[str] = None,
  ) -> TaskItem:
    task = TaskItem(
        title=title, category=category, priority=priority, due_date=due_date
    )
    self.tasks.append(task)
    self._save_tasks()
    return task

  def get_all_tasks(self) -> List[TaskItem]:
    return self.tasks

  def toggle_task(self, task_id: str) -> Optional[TaskItem]:
    for task in self.tasks:
      if task.id == task_id:
        task.completed = not task.completed
        self._save_tasks()
        return task
    return None

  def delete_task(self, task_id: str) -> bool:
    initial_len = len(self.tasks)
    self.tasks = [t for t in self.tasks if t.id != task_id]
    if len(self.tasks) < initial_len:
      self._save_tasks()
      return True
    return False

  def process_query(self, user_input: str) -> Dict[str, Any]:
    """Processes user input, updates history, and makes an autonomous decision."""
    self.conversation_history.add_entry(role="user", content=user_input)

    user_input_lower = user_input.lower().strip()

    if user_input_lower.startswith("add todo ") or user_input_lower.startswith(
        "add task "
    ):
      task_title = (
          user_input[9:].strip()
          if user_input_lower.startswith("add todo ")
          else user_input[9:].strip()
      )
      priority = "High" if "urgent" in user_input_lower else "Medium"
      task = self.add_task(task_title, priority=priority)
      response_text = (
          f"Added task: '{task.title}' [{task.priority} Priority] (ID:"
          f" {task.id[:8]})"
      )
      action = "add_task"
    elif user_input_lower in ["list todo", "list tasks", "show todos", "show tasks"]:
      tasks_str = "\n".join(
          [
              f"[{'X' if t.completed else ' '}] [{t.priority}] {t.id[:8]}:"
              f" {t.title}"
              for t in self.tasks
          ]
      )
      response_text = tasks_str if tasks_str else "No tasks in your to-do list."
      action = "list_tasks"
    else:
      response_text = f"NOVA Mind processed request: '{user_input}'"
      action = "general_query"

    self.conversation_history.add_entry(
        role="assistant",
        content=response_text,
        metadata={"action": action},
    )

    return {
        "response": response_text,
        "action": action,
        "autonomy": self.user_profile.autonomy,
        "tasks_count": len(self.tasks),
    }
