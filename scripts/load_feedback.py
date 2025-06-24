from collections.abc import Mapping, Sequence
from typing import Final

import database.setup
import moodle.feedback
from feedback.feedback import Feedback

DB_PATH = "data/database.db"

question_map: Final[Mapping[
    tuple[str, str, str],
    Sequence[tuple[str, int, int]],
]] = {
    ("CS101", "SS2025", "Lab02"): [("Math Expressions", 15, 16)],
    ("CS101", "SS2025", "Lab04"): [("Boolean Reasoning", 9, 10)],
    ("CS101", "SS2025", "Lab17"): [
        ("Dicts", 5, 6),
        ("Dicts With Errors", 5, 6),
    ],
    ("CS130", "SS2025", "Lab01"): [
        ("Dicts With Errors", 10, 11),
        ("Dicts", 10, 11),
        ("Functional Equivalence", 17, 18),
    ],
    ("CS130", "SS2025", "Lab03"): [("Test Case Match", 6, 7)],
    ("CS130", "SS2025", "Lab04"): [("Identify Exceptions", 13, 14)],
    ("CS101", "S12025", "Lab02"): [("Math Expressions", 15, 16)],
    ("CS101", "S12025", "Lab04"): [("Boolean Reasoning", 9, 10)],
    ("CS101", "S12025", "Lab17"): [
        ("Dicts", 7, 8),
        ("Dicts With Errors", 7, 8),
    ],
    ("CS130", "S12025", "Lab01"): [
        ("Dicts With Errors", 13, 14),
        ("Dicts", 13, 14),
        ("Functional Equivalence", 21, 22),
    ],
    ("CS130", "S12025", "Lab03"): [("Test Case Match", 6, 7)],
    ("CS130", "S12025", "Lab04"): [("Identify Exceptions", 15, 16)],
}

for (course, semester, lab), questions in question_map.items():
    for name, rating_num, comment_num in questions:
        file = course + semester[:2] + "_" + lab
        with open(f"data/raw/{file}.json", "rb") as f:
            raw_feedback = moodle.feedback.load(f, rating_num, comment_num)
        result = [
            Feedback.from_raw(name, username, course, semester, raw_rating)
            for username, raw_rating in raw_feedback.items()
        ]
        with database.setup.connection(DB_PATH, (Feedback,)) as con:
            Feedback.persist(con, *result)
