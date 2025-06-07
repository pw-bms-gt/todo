from __future__ import annotations

import argparse
from datetime import date, timedelta
from typing import List

from .todo import Todo, TodoStore


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Todo manager")
    sub = parser.add_subparsers(dest="command", required=True)

    add_p = sub.add_parser("add", help="Add a new todo")
    add_p.add_argument("title", help="Title of the todo")
    add_p.add_argument("--project")
    add_p.add_argument("--description", default="")
    add_p.add_argument("--due", help="Due date in YYYY-MM-DD format")
    add_p.add_argument("--assignees", nargs="*", default=[])
    add_p.add_argument("--parent", type=int, help="ID of parent todo for subtask")

    sub.add_parser("list", help="List all todos")

    sub.add_parser("daily", help="List todos due today")
    sub.add_parser("weekly", help="List todos due this week")

    complete_p = sub.add_parser("complete", help="Mark todo as completed")
    complete_p.add_argument("id", type=int)

    return parser


def print_todos(todos: List[Todo]) -> None:
    for todo in todos:
        status = "[x]" if todo.completed else "[ ]"
        line = f"{status} {todo.id}: {todo.title}"
        if todo.project:
            line += f" (project: {todo.project})"
        if todo.due:
            line += f" due {todo.due}"
        if todo.assignees:
            line += f" assignees: {', '.join(todo.assignees)}"
        print(line)
        for sub in todo.subtasks:
            sub_status = "[x]" if sub.completed else "[ ]"
            print(f"    {sub_status} {sub.id}: {sub.title}")


def main(argv: List[str] | None = None) -> None:
    parser = create_parser()
    args = parser.parse_args(argv)
    store = TodoStore()

    if args.command == "add":
        todo = Todo(
            title=args.title,
            project=args.project,
            description=args.description,
            due=args.due,
            assignees=args.assignees,
        )
        if args.parent:
            if not store.add_subtask(args.parent, todo):
                parser.error(f"Parent todo with id {args.parent} not found")
        else:
            store.add(todo)
        return

    if args.command == "list":
        print_todos(store.list_all())
        return

    if args.command == "complete":
        if not store.mark_complete(args.id):
            parser.error(f"Todo with id {args.id} not found")
        return

    today = date.today()
    if args.command == "daily":
        todos = store.filter_by_due_range(today, today)
        print_todos(todos)
        return

    if args.command == "weekly":
        end = today + timedelta(days=7)
        todos = store.filter_by_due_range(today, end)
        print_todos(todos)
        return


if __name__ == "__main__":
    main()
