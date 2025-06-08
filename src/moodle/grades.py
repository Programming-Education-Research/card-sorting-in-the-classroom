import csv
from collections import defaultdict
from datetime import datetime
from typing import IO

from .utils import join_by


def load(names_to_paths):
    tests = []
    for test_name, filename in names_to_paths.items():
        with open(filename, "r", encoding="utf-8-sig") as f:
            result = load_attempts(f, test_name)
            tests.append(result)
    return join_by("username", *tests)


def load_attempts(grades: IO, name: str):
    attempts = first_attempts(grades)
    attempts = [select_columns(attempt, name) for attempt in attempts]
    return attempts


def select_columns(attempt, name):
    grade_col = next(k for k in attempt.keys() if k.startswith("Grade/"))
    grade = float(attempt[grade_col])
    out_of = float(grade_col.split("/")[1])
    return {
        "username": attempt["Username"],
        name: grade / out_of
    }


def first_attempts(grades: IO):
    reader = csv.DictReader(grades)
    username_to_attempts = defaultdict(list)
    for row in reader:
        if row["Last name"] != "Overall average":
            username_to_attempts[row["Username"]].append(row)
    return [
        # attempts
        min(attempts, key=lambda a: parse_time(a["Started on"]))
        for attempts in username_to_attempts.values()
    ]


def parse_time(timestamp: str) -> datetime:
    return datetime.strptime(timestamp, "%d %B %Y  %I:%M %p")
