from collections.abc import Mapping, Sequence
from typing import Final

from questions.cardsort import Cardsort
from questions.question import Question
from questions.refute import Refute
from questions.reverse_trace import ReverseTrace

question_map: Final[Mapping[str, Sequence[tuple[type[Question], int, str]]]] = {
    "CS101SS_Lab02": [(Cardsort, 14, "Math Expressions")],
    "CS101SS_Lab04": [(Cardsort, 8, "Boolean Reasoning")],
    "CS101SS_Lab17": [
        (Cardsort, 3, "Dicts"),
        (Cardsort, 4, "Dicts With Errors"),
    ],
    "CS130SS_Lab01": [
        (Cardsort, 8, "Dicts With Errors"),
        (Cardsort, 9, "Dicts"),
        (Cardsort, 16, "Functional Equivalence"),
    ],
    "CS130SS_Lab03": [(Cardsort, 5, "Test Case Match")],
    "CS130SS_Lab04": [(Cardsort, 12, "Identify Exceptions")],

    "CS101S1_Lab02": [(Cardsort, 14, "Math Expressions")],
    "CS101S1_Lab04": [(Cardsort, 8, "Boolean Reasoning")],
    "CS101S1_Lab13": [
        (ReverseTrace, 2, "Flip Even Indices"),
        (Refute, 3, "OR before AND"),
        (Refute, 4, "Index Underflow"),
    ],
    "CS101S1_Lab15": [
        (Refute, 2, ".index On Duplicate"),
        (ReverseTrace, 3, "Sum Pairs"),
    ],
    "CS101S1_Lab17": [
        (Cardsort, 3, "Dicts"),
        (Cardsort, 4, "Dicts With Errors"),
    ],
    "CS130S1_Lab01": [
        (Cardsort, 8, "Dicts With Errors"),
        (Cardsort, 9, "Dicts"),
        (Cardsort, 16, "Functional Equivalence"),
    ],
    "CS130S1_Lab03": [(Cardsort, 5, "Test Case Match")],
    "CS130S1_Lab04": [(Cardsort, 12, "Identify Exceptions")],
    "CS130S1_Lab14": [
        (ReverseTrace, 1, "Flip Even Indices"),
        (Refute, 2, "OR before AND"),
        (Refute, 3, "Index Underflow"),
    ],
    "CS130S1_Lab17": [
        (Refute, 1, ".index On Duplicate"),
        (ReverseTrace, 2, "Sum Pairs"),
    ],
}

