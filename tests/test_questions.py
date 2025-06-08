from approvaltests import verify

from questions.cardsort import Cardsort
from questions.refute import Refute
from questions.reverse_trace import ReverseTrace
from utils import test

A_REFUTE_QUESTION = Refute(
    "The refute question name",
    "The refute question prompt",
    "Given: foo({[12]}); Then: {[12]}; But: {[12]}",
    "Given: {[given]}; Then: {[then]}; But: {[but]}",
)
A_REVERSE_TRACE_QUESTION = ReverseTrace(
    "The revere trace question name",
    "The reverse trace question prompt",
    "foo = {[12]}",
    "12345",
)
A_CARD_SORT_QUESTION = Cardsort(
    "The card sort question name",
    "The card sort question prompt",
    {"Foo": ["A", "B", "C"], "Bar": [], "Baz": []},
    {"Foo": [], "Bar": ["A", "B"], "Baz": ["C"]},
    False,
)


@test
def refute_questions_give_instructions():
    verify(A_REFUTE_QUESTION.instructions())


@test
def refute_questions_give_questions():
    verify(A_REFUTE_QUESTION.question())


@test
def refute_questions_parse_completions():
    answer = {"given": "foo", "then": "bar", "but": "baz"}
    assert A_REFUTE_QUESTION.json_to_attempt(answer) == answer


@test
def reverse_trace_questions_give_instructions():
    verify(A_REVERSE_TRACE_QUESTION.instructions())


@test
def reverse_trace_questions_give_questions():
    verify(A_REVERSE_TRACE_QUESTION.question())


@test
def reverse_trace_questions_parse_completions():
    answer = "Foo"
    assert A_REVERSE_TRACE_QUESTION.json_to_attempt(answer) == answer

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
