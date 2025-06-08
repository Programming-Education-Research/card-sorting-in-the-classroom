from moodle.xml import RawQuestion
from questions.cardsort import Cardsort
from questions.question import Question
from questions.refute import Refute
from questions.reverse_trace import ReverseTrace


def from_raw(raw: RawQuestion) -> Question:
    match raw["type"]:
        case "python_refute":
            return Refute.from_raw(raw)
        # I have no idea why, but the production Moodle instance suffixes a 1
        case "python3_html_gapfiller-1":
            return ReverseTrace.from_raw(raw)
        case "cardsort":
            return Cardsort.from_raw(raw)
        case _:
            raise RuntimeError(f"Unrecognised question type: `{raw['type']}`")
