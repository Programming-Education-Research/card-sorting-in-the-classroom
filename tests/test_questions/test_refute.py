from approvaltests import verify

from questions.refute import Refute
from ..utils import test


A_REFUTE_QUESTION = Refute(
    "The refute question name",
    "The refute question prompt",
    "Given: foo({[12]}); Then: {[12]}; But: {[12]}",
    "Given: {[given]}; Then: {[then]}; But: {[but]}",
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

