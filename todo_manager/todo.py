from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from datetime import date
from pathlib import Path
from typing import List, Optional


DATA_FILE = Path(__file__).resolve().parent.parent / 'data' / 'todos.json'


def _load_data() -> List[dict]:
    if DATA_FILE.exists():
        with DATA_FILE.open('r', encoding='utf-8') as fh:
            try:
                return json.load(fh)
            except json.JSONDecodeError:
                return []
    return []


def _save_data(data: List[dict]) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with DATA_FILE.open('w', encoding='utf-8') as fh:
        json.dump(data, fh, indent=2)


@dataclass
class Todo:
    title: str
    project: Optional[str] = None
    description: str = ""
    due: Optional[str] = None  # ISO formatted date string
    assignees: List[str] = field(default_factory=list)
    subtasks: List["Todo"] = field(default_factory=list)
    completed: bool = False
    id: int = field(default=0)

    def to_dict(self) -> dict:
        data = asdict(self)
        data['subtasks'] = [t.to_dict() for t in self.subtasks]
        return data

    @staticmethod
    def from_dict(data: dict) -> "Todo":
        subtasks = [Todo.from_dict(t) for t in data.get('subtasks', [])]
        data = {k: v for k, v in data.items() if k != 'subtasks'}
        todo = Todo(**data)
        todo.subtasks = subtasks
        return todo


class TodoStore:
    def __init__(self) -> None:
        self.todos: List[Todo] = [Todo.from_dict(d) for d in _load_data()]
        self._next_id = max([t.id for t in self.todos], default=0) + 1

    def add(self, todo: Todo) -> None:
        todo.id = self._next_id
        self._next_id += 1
        self.todos.append(todo)
        self.save()

    def save(self) -> None:
        _save_data([t.to_dict() for t in self.todos])

    def list_all(self) -> List[Todo]:
        return list(self.todos)

    def get(self, todo_id: int) -> Optional[Todo]:
        for todo in self.todos:
            if todo.id == todo_id:
                return todo
        return None

    def mark_complete(self, todo_id: int) -> bool:
        todo = self.get(todo_id)
        if todo:
            todo.completed = True
            self.save()
            return True
        return False

    def add_subtask(self, parent_id: int, subtask: Todo) -> bool:
        parent = self.get(parent_id)
        if parent:
            subtask.id = self._next_id
            self._next_id += 1
            parent.subtasks.append(subtask)
            self.save()
            return True
        return False

    def filter_by_due_range(self, start: date, end: date) -> List[Todo]:
        result = []
        for todo in self.todos:
            if todo.due:
                try:
                    due_date = date.fromisoformat(todo.due)
                except ValueError:
                    continue
                if start <= due_date <= end:
                    result.append(todo)
        return result
