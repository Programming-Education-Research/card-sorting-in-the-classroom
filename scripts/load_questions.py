from collections.abc import Mapping
from typing import Final

import database
import moodle
from questions.cardsort import Cardsort
from questions.question import Question
from questions.refute import Refute
from questions.reverse_trace import ReverseTrace
from questions.utils import from_raw

TABLES: Final[tuple[type[Question], ...]] = (Cardsort, Refute, ReverseTrace)

name_map: Final[Mapping[str, str]] = {
    "Card Sort — Math Expressions": "Math Expressions",
    "Card Sort — Boolean Reasoning": "Boolean Reasoning",
    "Card Sort — Dict Result Match": "Dicts",
    "Card Sort — Dict Result and Error Match": "Dicts With Errors",
    "Card Sort — Functional Equivalence": "Functional Equivalence",
    "Card Sort — Test Case Match": "Test Case Match",
    "Card Sort — Identify Possible Exceptions": "Identify Exceptions",
    "Reverse Trace: flip evens in list": "Flip Even Indices",
    "refute: bring umbrella": "OR before AND",
    "refute: no pairs over 5": "Index Underflow",
    "Refute — With Index": ".index On Duplicate",
    "Reverse Trace — Gobble List": "Sum Pairs",
    "Card Sort — Ranges": "Ranges",
}

questions = {}

with open("../data/raw/CS101_questions.xml", "rb") as f:
    for question in moodle.xml.parse(f):
        question = from_raw(question)
        question.name = name_map[question.name]
        questions[question.name] = question

with open("../data/raw/CS130_questions.xml", "rb") as f:
    for question in moodle.xml.parse(f):
        question = from_raw(question)
        question.name = name_map[question.name]
        questions[question.name] = question

with database.setup.connection("../data/database.db", TABLES) as con:
    for question in questions.values():
        type(question).persist(con, question)
