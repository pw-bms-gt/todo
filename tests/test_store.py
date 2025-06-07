from todo_manager.todo import Todo, TodoStore


def test_add_and_list(tmp_path, monkeypatch):
    path = tmp_path / "todos.json"
    monkeypatch.setattr("todo_manager.todo.DATA_FILE", path)

    store = TodoStore()
    store.add(Todo(title="Task 1"))
    store.add(Todo(title="Task 2"))

    todos = store.list_all()
    assert len(todos) == 2
    assert todos[0].title == "Task 1"
    assert todos[1].title == "Task 2"


def test_add_subtask(tmp_path, monkeypatch):
    path = tmp_path / "todos.json"
    monkeypatch.setattr("todo_manager.todo.DATA_FILE", path)

    store = TodoStore()
    store.add(Todo(title="Parent"))
    store.add_subtask(1, Todo(title="Child"))

    parent = store.get(1)
    assert parent is not None
    assert len(parent.subtasks) == 1
    assert parent.subtasks[0].title == "Child"
