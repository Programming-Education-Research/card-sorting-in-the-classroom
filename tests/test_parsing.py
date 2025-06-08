from pprint import pformat

from approvaltests import verify

import moodle
from questions.utils import from_raw
from utils import test


@test
def refute_and_reverse_trace_questions_can_be_parsed():
    with open("./data/questions.xml", "rb") as f:
        questions = [from_raw(q) for q in moodle.xml.parse(f)]
    verify(pformat(questions, width=240))
