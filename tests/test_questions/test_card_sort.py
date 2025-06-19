from approvaltests import verify

from questions.cardsort import Cardsort
from ..utils import test

A_CARD_SORT_QUESTION = Cardsort(
    "The card sort question name",
    "The card sort question prompt",
    {"Foo": ["A", "B", "C"], "Bar": [], "Baz": []},
    {"Foo": [], "Bar": ["A", "B"], "Baz": ["C"]},
    False,
)


@test
def card_sort_questions_give_instructions():
    verify(A_CARD_SORT_QUESTION.instructions())


@test
def card_sort_questions_give_questions():
    verify(A_CARD_SORT_QUESTION.question())


@test
def card_sort_questions_parse_completions():
    answer = {"Foo": [], "Bar": ["Card 1", "Card 2"], "Baz": ["Card 3"]}
    expected = {"Foo": [], "Bar": ["A", "B"], "Baz": ["C"]}
    assert A_CARD_SORT_QUESTION.json_to_attempt(answer) == expected

