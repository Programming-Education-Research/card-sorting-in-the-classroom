from approvaltests import verify

from questions.reverse_trace import ReverseTrace
from ..utils import test


A_REVERSE_TRACE_QUESTION = ReverseTrace(
    "The revere trace question name",
    "The reverse trace question prompt",
    "foo = {[12]}",
    "12345",
)

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

