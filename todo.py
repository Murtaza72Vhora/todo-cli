#!/usr/bin/env python3
import argparse
import json
import os
from datetime import datetime
from typing import List, Dict, Any

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
        print("No tasks to show.")
        return
    rows = []
    rows.append(["ID", "Title", "Pri", "Due", "Status"])
    for t in tasks:
        rows.append([
            str(t["id"]),
            t["title"],
            str(t["priority"] or ""),
            t["due"] or "",
            "✔" if t["done"] else "•",
        ])
    # column widths
    widths = [max(len(row[i]) for row in rows) for i in range(len(rows[0]))]
    # print
    def fmt(row):
        return "  ".join(cell.ljust(widths[i]) for i, cell in enumerate(row))
    print(fmt(rows[0]))
    print(fmt(["─"*w for w in widths]))
    for row in rows[1:]:
        print(fmt(row))

# ---------- CLI ----------
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="todo",
        description="A tiny, friendly CLI to-do list.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Add a new task")
    p_add.add_argument("title", nargs="+", help="Task title")
    p_add.add_argument("-p", "--priority", type=int, default=None, help="Priority number (higher = more important)")
    p_add.add_argument("-d", "--due", type=str, default=None, help="Due date (any text, e.g. 2025-09-01)")
    
    p_list = sub.add_parser("list", help="List tasks")
    group = p_list.add_mutually_exclusive_group()
    group.add_argument("--all", action="store_true", help="Show all tasks")
    group.add_argument("--done", action="store_true", help="Show only completed tasks")
    # default (no flags) shows only undone
    
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
        print(f"Added #{task['id']}: {task['title']}")
    elif args.command == "list":
        tasks = list_tasks(show_all=args.all, show_done=args.done)
        print_tasks_table(tasks)
    elif args.command == "done":
        ok = complete_task(args.id)
        print("Marked as done." if ok else "Task not found.")
    elif args.command == "delete":
        ok = delete_task(args.id)
        print("Deleted." if ok else "Task not found.")

if __name__ == "__main__":
    main()
