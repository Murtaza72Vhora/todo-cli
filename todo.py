#!/usr/bin/env python3
import argparse
import json
import os
from datetime import datetime
from typing import List, Dict, Any
from rich.console import Console
from rich.table import Table
from rich.text import Text

console = Console()
DATA_FILE = os.path.expanduser("~/.todo_cli.json")

# ---------- storage ----------
def load_tasks() -> List[Dict[str, Any]]:
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_tasks(tasks: List[Dict[str, Any]]) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)

def next_id(tasks: List[Dict[str, Any]]) -> int:
    return max([t["id"] for t in tasks], default=0) + 1

# ---------- operations ----------
def add_task(title: str, priority: int | None, due: str | None) -> Dict[str, Any]:
    tasks = load_tasks()
    task = {
        "id": next_id(tasks),
        "title": title,
        "done": False,
        "priority": priority,
        "due": due,
        "created": datetime.now().isoformat(timespec="seconds"),
    }
    tasks.append(task)
    save_tasks(tasks)
    return task

def complete_task(task_id: int) -> bool:
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = True
            save_tasks(tasks)
            return True
    return False

def delete_task(task_id: int) -> bool:
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t["id"] != task_id]
    if len(new_tasks) != len(tasks):
        save_tasks(new_tasks)
        return True
    return False

def list_tasks(show_all: bool, show_done: bool) -> List[Dict[str, Any]]:
    tasks = load_tasks()
    if not show_all:
        tasks = [t for t in tasks if t["done"] == show_done]
    # sort: undone first, higher priority first, then id
    tasks.sort(key=lambda t: (t["done"], -(t["priority"] or 0), t["id"]))
    return tasks

# ---------- UI ----------
def print_tasks_table(tasks: List[Dict[str, Any]]) -> None:
    if not tasks:
        console.print("[yellow]No tasks to show.[/yellow]")
        return

    table = Table(title="📝 Todo List", show_lines=True)
    table.add_column("ID", style="cyan", justify="right")
    table.add_column("Title", style="magenta")
    table.add_column("Priority", style="bold")
    table.add_column("Due", style="blue")
    table.add_column("Status", style="green")

    for t in tasks:
        # Priority formatting
        pri = t.get("priority")
        if pri is None:
            pri_text = Text("-", style="dim")
        elif pri >= 3:
            pri_text = Text(f"{pri} (High)", style="red bold")
        elif pri == 2:
            pri_text = Text(f"{pri} (Medium)", style="yellow")
        else:
            pri_text = Text(f"{pri} (Low)", style="green")

        # Due date formatting
        due = t.get("due")
        due_text = Text(due or "-", style="dim")
        if due:
            try:
                due_date = datetime.fromisoformat(due)
                today = datetime.now().date()
                if due_date.date() < today:
                    due_text = Text(due, style="red")
                elif due_date.date() == today:
                    due_text = Text(due, style="yellow")
                else:
                    due_text = Text(due, style="blue")
            except ValueError:
                due_text = Text(due, style="dim")

        # Status formatting
        status = Text("✔ Done", style="green") if t["done"] else Text("• Pending", style="red")

        table.add_row(
            str(t["id"]),
            t["title"],
            pri_text,
            due_text,
            status,
        )

    console.print(table)

# ---------- CLI ----------
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="todo",
        description="A tiny, friendly CLI to-do list.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Add a new task")
    p_add.add_argument("title", nargs="+", help="Task title")
    p_add.add_argument("-p", "--priority", type=int, default=None, help="Priority (1=Low, 2=Medium, 3=High)")
    p_add.add_argument("-d", "--due", type=str, default=None, help="Due date (YYYY-MM-DD)")

    p_list = sub.add_parser("list", help="List tasks")
    group = p_list.add_mutually_exclusive_group()
    group.add_argument("--all", action="store_true", help="Show all tasks")
    group.add_argument("--done", action="store_true", help="Show only completed tasks")

    p_done = sub.add_parser("done", help="Mark a task as done")
    p_done.add_argument("id", type=int, help="Task ID")

    p_del = sub.add_parser("delete", help="Delete a task")
    p_del.add_argument("id", type=int, help="Task ID")
    return parser

def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "add":
        title = " ".join(args.title).strip()
        task = add_task(title, args.priority, args.due)
        console.print(f"[green]Added task[/green] #{task['id']}: {task['title']}")
    elif args.command == "list":
        tasks = list_tasks(show_all=args.all, show_done=args.done)
        print_tasks_table(tasks)
    elif args.command == "done":
        ok = complete_task(args.id)
        console.print("[cyan]Marked as done.[/cyan]" if ok else "[red]Task not found.[/red]")
    elif args.command == "delete":
        ok = delete_task(args.id)
        console.print("[red]Deleted.[/red]" if ok else "[red]Task not found.[/red]")

if __name__ == "__main__":
    main()
