import json
from pprint import pformat
from typing import Final

import pytest
from approvaltests import verify
from approvaltests.namer import NamerFactory

from questions.cardsort import Cardsort
from ..utils import test

A_CARD_SORT_QUESTION = Cardsort(
    "The card sort question name",
    "The card sort question prompt",
    {"Foo": ["A", "B", "C"], "Bar": [], "Baz": []},
    {"Foo": [], "Bar": ["A", "B"], "Baz": ["C"]},
    False,
)

BOOLEAN_REASONING: Final[Cardsort] = Cardsort(
    name="Boolean Reasoning",
    prompt="""Just because we can write code that runs doesn't mean it's code that works. When we write Boolean expressions, it is usually because we want them to be True in some cases and False in others — however, it is possible to write Boolean expressions that are always True or always False.
Assuming the variables x, y, and z can be any integers, sort the cards into groups based on whether they are always True, always False, or can be either True or False.""",
    preload={
        "Cards": [
            "0 < x and x < 3",
            "x == z or y != z",
            "x < 0 and x > 5",
            "x == y and x != y",
            "x == y or x != y",
            "x < 0 or x > 5", "0 < x or x < 3",
            "x < y and y < z and z < x"
        ],
        "Always True": [],
        "Always False": [],
        "Either True or False": [],
    },
    answer={
        "Cards": [],
        "Always True": [
            "x == y or x != y",
            "0 < x or x < 3"
        ],
        "Always False": [
            "x < 0 and x > 5",
            "x == y and x != y",
            "x < y and y < z and z < x"
        ],
        "Either True or False": [
            "0 < x and x < 3",
            "x == z or y != z",
            "x < 0 or x > 5",
        ],
    },
    is_ordered=True,
)

boolean_reasoning_answers = {
    "Boolean Reasoning-Correct": {
        "Cards": [],
        "Always True": [
            "x == y or x != y",
            "0 < x or x < 3"
        ],
        "Always False": [
            "x < 0 and x > 5",
            "x == y and x != y",
            "x < y and y < z and z < x"
        ],
        "Either True or False": [
            "0 < x and x < 3",
            "x == z or y != z",
            "x < 0 or x > 5",
        ],
    },
    "Boolean Reasoning-Incorrect": {
        "Cards": [],
        "Always True": [
            "x == y or x != y",
            "0 < x or x < 3",
            "x < 0 and x > 5",
        ],
        "Always False": [
            "x == y and x != y",
            "x < y and y < z and z < x"
        ],
        "Either True or False": [
            "0 < x and x < 3",
            "x == z or y != z",
            "x < 0 or x > 5",
        ],
    },
    "Boolean Reasoning-inadmissible Groups": {
        "Cards": [],
        "Always True!!": [
            "x == y or x != y",
            "0 < x or x < 3"
        ],
        "Always False": [
            "x < 0 and x > 5",
            "x == y and x != y",
            "x < y and y < z and z < x"
        ],
        "Either True or False": [
            "0 < x and x < 3",
            "x == z or y != z",
            "x < 0 or x > 5",
        ],
    },
    "Boolean Reasoning-Inadmissible Cards": {
        "Cards": [],
        "Always True": [
            "x == y or x != y",
            "0 < x or x < 3"
        ],
        "Always False": [
            "x < 0 and x > 5",
            "FOO BAR",
            "x < y and y < z and z < x"
        ],
        "Either True or False": [
            "0 < x and x < 3",
            "x == z or y != z",
            "x < 0 or x > 5",
        ],
    },
    "Boolean Reasoning-Not Genuine": {
        "Cards": [
            "0 < x and x < 3",
            "x == z or y != z",
            "x < 0 and x > 5",
            "x == y and x != y",
            "x == y or x != y",
            "x < 0 or x > 5", "0 < x or x < 3",
            "x < y and y < z and z < x"
        ],
        "Always True": [],
        "Always False": [],
        "Either True or False": [],
    },
}

boolean_reasoning_answers = {
    title: json.dumps({"cardsort": [{"groups": [
        {"title": title, "cards": [{"prompt": c} for c in cards]}
        for title, cards in answer.items()
    ]}]})
    for title, answer in boolean_reasoning_answers.items()
}

IDENTIFY_EXCEPTIONS: Final[Cardsort] = Cardsort(
    name="Identify Exceptions",
    prompt="""Put the functions into groups based on the possible exception types they may raise for any given parameters.
Assume the parameter names indicate the type of the parameter:

nums, numbers, and vals refer to lists of ints
num_tuple refers to a tuple of ints
word refers to a string
n_slices, n_people, and n refer to ints""",
    preload={"Cards": [
        "def sum_up_to_n():\n    n = input(\"n: \")\n    return n * (n + 1) / 2",
        "def remove_evens(vals):\n    for i in range(len(vals) - 1, -1, -1):\n        num = vals[i]\n        if num % 2 == 0:\n            vals.pop(num)",
        "def double_tuple(num_tuple):\n    sorted_nums = sorted(num_tuple)\n    return num_tuple + sorted_nums",
        "def pairwise_sums(numbers):\n    result = []\n    for i in range(len(numbers)):\n        pair = numbers[i] + numbers[i + 1]\n        result.append(pair)\n    return result",
        "def mean_of_evens(nums):\n    nums = [e for e in nums if e % 2 == 0]\n    return sum(nums) / len(nums)",
        "def min_divisible_by_3(nums):\n    nums = [e for e in nums if e % 3 == 0]\n    return min(nums)",
        "def remaining_slices(n_slices, n_people):\n    return n_people % n_slices",
        "def vowel_ratio(word):\n    word = word.lower()\n    vowels = 0\n    for vowel in \"aeiou\":\n        vowels += word.count(vowel)\n    return vowels / len(word)",
        "def sum_up_to_n():\n    n = int(input(\"n: \"))\n    return n * (n + 1) / 2"],
        "TypeError": [], "ValueError": [], "IndexError": [],
        "ZeroDivisionError": []},
    answer={"Cards": [], "TypeError": [
        "def sum_up_to_n():\n    n = input(\"n: \")\n    return n * (n + 1) / 2",
        "def double_tuple(num_tuple):\n    sorted_nums = sorted(num_tuple)\n    return num_tuple + sorted_nums"],
            "ValueError": [
                "def min_divisible_by_3(nums):\n    nums = [e for e in nums if e % 3 == 0]\n    return min(nums)",
                "def sum_up_to_n():\n    n = int(input(\"n: \"))\n    return n * (n + 1) / 2"],
            "IndexError": [
                "def remove_evens(vals):\n    for i in range(len(vals) - 1, -1, -1):\n        num = vals[i]\n        if num % 2 == 0:\n            vals.pop(num)",
                "def pairwise_sums(numbers):\n    result = []\n    for i in range(len(numbers)):\n        pair = numbers[i] + numbers[i + 1]\n        result.append(pair)\n    return result"],
            "ZeroDivisionError": [
                "def mean_of_evens(nums):\n    nums = [e for e in nums if e % 2 == 0]\n    return sum(nums) / len(nums)",
                "def remaining_slices(n_slices, n_people):\n    return n_people % n_slices",
                "def vowel_ratio(word):\n    word = word.lower()\n    vowels = 0\n    for vowel in \"aeiou\":\n        vowels += word.count(vowel)\n    return vowels / len(word)"]},
    is_ordered=False,
)

identify_exceptions_answers = {
    "Identify Exceptions-Correct": {
        "Cards": [],
        "TypeError": [
            "def sum_up_to_n():\n    n = input(\"n: \")\n    return n * (n + 1) / 2",
            "def double_tuple(num_tuple):\n    sorted_nums = sorted(num_tuple)\n    return num_tuple + sorted_nums"],
        "ValueError": [
            "def min_divisible_by_3(nums):\n    nums = [e for e in nums if e % 3 == 0]\n    return min(nums)",
            "def sum_up_to_n():\n    n = int(input(\"n: \"))\n    return n * (n + 1) / 2"],
        "IndexError": [
            "def remove_evens(vals):\n    for i in range(len(vals) - 1, -1, -1):\n        num = vals[i]\n        if num % 2 == 0:\n            vals.pop(num)",
            "def pairwise_sums(numbers):\n    result = []\n    for i in range(len(numbers)):\n        pair = numbers[i] + numbers[i + 1]\n        result.append(pair)\n    return result"],
        "ZeroDivisionError": [
            "def mean_of_evens(nums):\n    nums = [e for e in nums if e % 2 == 0]\n    return sum(nums) / len(nums)",
            "def remaining_slices(n_slices, n_people):\n    return n_people % n_slices",
            "def vowel_ratio(word):\n    word = word.lower()\n    vowels = 0\n    for vowel in \"aeiou\":\n        vowels += word.count(vowel)\n    return vowels / len(word)",
        ]
    },
    "Identify Exceptions-Incorrect": {
        "Cards": [],
        "TypeError": [
            "def sum_up_to_n():\n    n = input(\"n: \")\n    return n * (n + 1) / 2",
            "def double_tuple(num_tuple):\n    sorted_nums = sorted(num_tuple)\n    return num_tuple + sorted_nums"],
        "ValueError": [
            "def min_divisible_by_3(nums):\n    nums = [e for e in nums if e % 3 == 0]\n    return min(nums)",
            "def sum_up_to_n():\n    n = int(input(\"n: \"))\n    return n * (n + 1) / 2"],
        "IndexError": [
            "def remove_evens(vals):\n    for i in range(len(vals) - 1, -1, -1):\n        num = vals[i]\n        if num % 2 == 0:\n            vals.pop(num)",
            "def pairwise_sums(numbers):\n    result = []\n    for i in range(len(numbers)):\n        pair = numbers[i] + numbers[i + 1]\n        result.append(pair)\n    return result",
            "def vowel_ratio(word):\n    word = word.lower()\n    vowels = 0\n    for vowel in \"aeiou\":\n        vowels += word.count(vowel)\n    return vowels / len(word)"],
        "ZeroDivisionError": [
            "def mean_of_evens(nums):\n    nums = [e for e in nums if e % 2 == 0]\n    return sum(nums) / len(nums)",
            "def remaining_slices(n_slices, n_people):\n    return n_people % n_slices"
        ],
    },
    "Identify Exceptions-inadmissible Groups": {
        "Cards": [],
        "TypeError!!": [
            "def sum_up_to_n():\n    n = input(\"n: \")\n    return n * (n + 1) / 2",
            "def double_tuple(num_tuple):\n    sorted_nums = sorted(num_tuple)\n    return num_tuple + sorted_nums"],
        "ValueError": [
            "def min_divisible_by_3(nums):\n    nums = [e for e in nums if e % 3 == 0]\n    return min(nums)",
            "def sum_up_to_n():\n    n = int(input(\"n: \"))\n    return n * (n + 1) / 2"],
        "IndexError": [
            "def remove_evens(vals):\n    for i in range(len(vals) - 1, -1, -1):\n        num = vals[i]\n        if num % 2 == 0:\n            vals.pop(num)",
            "def pairwise_sums(numbers):\n    result = []\n    for i in range(len(numbers)):\n        pair = numbers[i] + numbers[i + 1]\n        result.append(pair)\n    return result"],
        "ZeroDivisionError": [
            "def mean_of_evens(nums):\n    nums = [e for e in nums if e % 2 == 0]\n    return sum(nums) / len(nums)",
            "def remaining_slices(n_slices, n_people):\n    return n_people % n_slices",
            "def vowel_ratio(word):\n    word = word.lower()\n    vowels = 0\n    for vowel in \"aeiou\":\n        vowels += word.count(vowel)\n    return vowels / len(word)",
        ]
    },
    "Identify Exceptions-Inadmissible Cards": {
        "Cards": [],
        "TypeError": [
            "FOO BAR",
            "def double_tuple(num_tuple):\n    sorted_nums = sorted(num_tuple)\n    return num_tuple + sorted_nums"],
        "ValueError": [
            "def min_divisible_by_3(nums):\n    nums = [e for e in nums if e % 3 == 0]\n    return min(nums)",
            "def sum_up_to_n():\n    n = int(input(\"n: \"))\n    return n * (n + 1) / 2"],
        "IndexError": [
            "def remove_evens(vals):\n    for i in range(len(vals) - 1, -1, -1):\n        num = vals[i]\n        if num % 2 == 0:\n            vals.pop(num)",
            "def pairwise_sums(numbers):\n    result = []\n    for i in range(len(numbers)):\n        pair = numbers[i] + numbers[i + 1]\n        result.append(pair)\n    return result"],
        "ZeroDivisionError": [
            "def mean_of_evens(nums):\n    nums = [e for e in nums if e % 2 == 0]\n    return sum(nums) / len(nums)",
            "def remaining_slices(n_slices, n_people):\n    return n_people % n_slices",
            "def vowel_ratio(word):\n    word = word.lower()\n    vowels = 0\n    for vowel in \"aeiou\":\n        vowels += word.count(vowel)\n    return vowels / len(word)",
        ]
    },
    "Identify Exceptions-Not Genuine": {"Cards": [
        "def sum_up_to_n():\n    n = input(\"n: \")\n    return n * (n + 1) / 2",
        "def remove_evens(vals):\n    for i in range(len(vals) - 1, -1, -1):\n        num = vals[i]\n        if num % 2 == 0:\n            vals.pop(num)",
        "def double_tuple(num_tuple):\n    sorted_nums = sorted(num_tuple)\n    return num_tuple + sorted_nums",
        "def pairwise_sums(numbers):\n    result = []\n    for i in range(len(numbers)):\n        pair = numbers[i] + numbers[i + 1]\n        result.append(pair)\n    return result",
        "def mean_of_evens(nums):\n    nums = [e for e in nums if e % 2 == 0]\n    return sum(nums) / len(nums)",
        "def min_divisible_by_3(nums):\n    nums = [e for e in nums if e % 3 == 0]\n    return min(nums)",
        "def remaining_slices(n_slices, n_people):\n    return n_people % n_slices",
        "def vowel_ratio(word):\n    word = word.lower()\n    vowels = 0\n    for vowel in \"aeiou\":\n        vowels += word.count(vowel)\n    return vowels / len(word)",
        "def sum_up_to_n():\n    n = int(input(\"n: \"))\n    return n * (n + 1) / 2"],
        "TypeError": [], "ValueError": [], "IndexError": [],
        "ZeroDivisionError": []},
}

identify_exceptions_answers = {
    title: json.dumps({"cardsort": [{"groups": [
        {"title": title, "cards": [{"prompt": c} for c in cards]}
        for title, cards in answer.items()
    ]}]})
    for title, answer in identify_exceptions_answers.items()
}


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


@test
@pytest.mark.parametrize(
    ("title", "answer"),
    boolean_reasoning_answers.items()
)
def card_sort_grades_answers_for_ordered_sorts(title, answer):
    verify(
        pformat(
            BOOLEAN_REASONING.grade_attempts("foo123", "CS1", "SX", [answer]),
            width=240,
        ),
        options=NamerFactory.with_parameters(title),
    )


@test
@pytest.mark.parametrize(
    ("title", "answer"),
    identify_exceptions_answers.items()
)
def card_sort_grades_answers_for_unordered_sorts(title, answer):
    verify(
        pformat(
            IDENTIFY_EXCEPTIONS.grade_attempts("foo123", "CS1", "SX", [answer]),
            width=240,
        ),
        options=NamerFactory.with_parameters(title),
    )


@test
def card_sort_parses_corrupted_raw_attempts():
    data = [
        "{'Cardsort': ['Groups': [{}]]",
        boolean_reasoning_answers["Boolean Reasoning-Correct"],
    ]
    verify(
        pformat(
            BOOLEAN_REASONING.grade_attempts("foo123", "CS1", "SX", data),
            width=240,
        ),
    )


@test
@pytest.mark.parametrize("question", (BOOLEAN_REASONING, IDENTIFY_EXCEPTIONS))
def card_sorts_give_prompts(question):
    verify(
        question.instructions(),
        options=NamerFactory.with_parameters(question.name),
    )
