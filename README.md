# Todo Manager

A simple command-line tool to manage project tasks with subtasks, daily and weekly views.

## Features

- Organise todos across multiple projects
- Create subtasks for each todo
- Assign deadlines (due dates) and assignees
- List all todos or filter by daily and weekly deadlines
- Mark tasks as completed

## Usage

```bash
python -m todo_manager add "Write documentation" --project docs --due 2025-01-01
python -m todo_manager list
python -m todo_manager daily
python -m todo_manager weekly
```

Todos are stored in `data/todos.json`.
