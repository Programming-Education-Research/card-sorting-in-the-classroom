from approvaltests import verify

from questions.refute import Refute
from ..utils import test

A_REFUTE_QUESTION = Refute(
    "The refute question name",
    "The refute question prompt",
    "Given: foo({[12]}); Then: {[12]}; But: {[12]}",
    "Given: {[given]}; Then: {[then]}; But: {[but]}",
)

DOT_INDEX = Refute(
    name='.index On Duplicate',
    prompt='A classmate has written the following function:\n'
           '\n'
           'def with_index(data):\n'
           '    result = []\n'
           '    for value in data:\n'
           '        pair = (data.index(value), value)\n'
           '        result.append(pair)\n'
           '    return result\n'
           '\n'
           'They claim the function takes a list of data and returns a '
           'list of tuples where each tuple contains the index of each '
           'value from the parameter list and the value itself: (index, '
           'value). For example:\n'
           '\n'
           'with_index(["a", "b", "c"])\n'
           '\n'
           'Returns:\n'
           '\n'
           '[(0, "a"), (1, "b"), (2, "c")]\n'
           '\n'
           'There is a bug in their code – write a test case that reveals '
           'the bug.',
    preload='Calling with_index({[28]})\n'
            'Should return: {[56]}\n'
            'But the above function actually returns: {[56]}',
    test='def buggy(data):\n'
         '    result = []\n'
         '    for value in data:\n'
         '        pair = (data.index(value), value)\n'
         '        result.append(pair)\n'
         '    return result\n'
         '\n'
         'def correct(data):\n'
         '    result = []\n'
         '    for i in range(len(data)):\n'
         '        pair = (i, data[i])\n'
         '        result.append(pair)\n'
         '    return result\n'
         '\n'
         'assert correct({[given]}) == {[then]}\n'
         'assert buggy({[given]}) == {[but]}'
),


@test
def refute_questions_give_instructions():
    verify(A_REFUTE_QUESTION.instructions())


@test
def refute_questions_give_questions():
    verify(A_REFUTE_QUESTION.question())


@test
def refute_questions_parse_completions():
    answer = {"given": "foo", "then": "bar", "but": "baz"}
    assert A_REFUTE_QUESTION.json_to_attempt(answer) == ["foo", "bar", "baz"]
