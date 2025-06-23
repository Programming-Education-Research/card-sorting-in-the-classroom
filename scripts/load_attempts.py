from collections.abc import Mapping, Sequence
from typing import Final

import database.setup
import moodle.responses
from attempts.attempt import Attempt
from questions.cardsort import Cardsort
from questions.question import Question
from questions.refute import Refute
from questions.reverse_trace import ReverseTrace

DB_PATH = "../data/database.db"

question_map: Final[Mapping[
    tuple[str, str, str],
    Sequence[tuple[type[Question], int, str]],
]] = {
    ("CS101", "SS2025", "Lab02"): [(Cardsort, 14, "Math Expressions")],
    ("CS101", "SS2025", "Lab04"): [(Cardsort, 8, "Boolean Reasoning")],
    ("CS101", "SS2025", "Lab17"): [
        (Cardsort, 3, "Dicts"),
        (Cardsort, 4, "Dicts With Errors"),
    ],
    ("CS130", "SS2025", "Lab01"): [
        (Cardsort, 8, "Dicts With Errors"),
        (Cardsort, 9, "Dicts"),
        (Cardsort, 16, "Functional Equivalence"),
    ],
    ("CS130", "SS2025", "Lab03"): [(Cardsort, 5, "Test Case Match")],
    ("CS130", "SS2025", "Lab04"): [(Cardsort, 12, "Identify Exceptions")],
    ("CS101", "S12025", "Lab02"): [(Cardsort, 14, "Math Expressions")],
    ("CS101", "S12025", "Lab04"): [(Cardsort, 8, "Boolean Reasoning")],
    ("CS101", "S12025", "Lab13"): [
        (ReverseTrace, 2, "Flip Even Indices"),
        (Refute, 3, "OR before AND"),
        (Refute, 4, "Index Underflow"),
    ],
    ("CS101", "S12025", "Lab15"): [
        (Refute, 2, ".index On Duplicate"),
        (ReverseTrace, 3, "Sum Pairs"),
    ],
    ("CS101", "S12025", "Lab17"): [
        (Cardsort, 5, "Dicts"),
        (Cardsort, 6, "Dicts With Errors"),
    ],
    ("CS130", "S12025", "Lab01"): [
        (Cardsort, 11, "Dicts With Errors"),
        (Cardsort, 12, "Dicts"),
        (Cardsort, 20, "Functional Equivalence"),
    ],
    ("CS130", "S12025", "Lab03"): [(Cardsort, 5, "Test Case Match")],
    ("CS130", "S12025", "Lab04"): [(Cardsort, 14, "Identify Exceptions")],
    ("CS130", "S12025", "Lab14"): [
        (ReverseTrace, 1, "Flip Even Indices"),
        (Refute, 2, "OR before AND"),
        (Refute, 3, "Index Underflow"),
    ],
    ("CS130", "S12025", "Lab17"): [
        (Refute, 1, ".index On Duplicate"),
        (ReverseTrace, 2, "Sum Pairs"),
    ],
}


def process_one_question(course, semester, lab, q_type, number, name):
    file = course + semester[:2] + "_" + lab
    with open(f"../data/raw/{file}.json", "rb") as f:
        responses = moodle.responses.load(f)
    with database.setup.connection(DB_PATH, (Attempt,)) as con:
        question = q_type.fetch(con, name=name)
    for username, raw in responses[number].items():
        print(file, number, name, username)
        attempts = question.grade_attempts(username, course, semester, raw)
        with database.setup.connection(DB_PATH, (Attempt,)) as con:
            Attempt.persist(con, *attempts)


def main():
    questions = [
        (course, semester, lab, q_type, number, name)
        for (course, semester, lab), questions in question_map.items()
        for (q_type, number, name) in questions
    ]
    for question in questions:
        process_one_question(*question)


if __name__ == "__main__":
    main()
