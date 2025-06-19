import json
import re
from dataclasses import dataclass
from typing import Self, override

import container.runner
from attempts.attempt import Attempt
from moodle.xml import RawQuestion
from questions.question import Question


@dataclass
class ReverseTrace(Question):
    prompt: str
    preload: str
    expect: str

    @classmethod
    @override
    def from_raw(cls, moodle_xml: RawQuestion) -> Self:
        return ReverseTrace(
            name=moodle_xml["name"],
            prompt=moodle_xml["prompt"],
            preload=moodle_xml["globalextra"],
            expect=moodle_xml["tests"][0]["stdout"],
        )

    @override
    def json_to_attempt(self, json_object: object) -> object:
        return json_object

    @override
    def json_schema(self) -> dict[str, object]:
        return {"type": "string", "strict": True}

    @override
    def instructions(self) -> str:
        return self.prompt

    @override
    def question(self) -> str:
        return re.sub(r"\{\s*\[\s*\d+\s*\]\s*\}", "???", self.preload)

    @override
    def grade_attempts(
          self,
          username: str,
          course: str,
          semester: str,
          raw_attempts: list[str],
    ) -> list[Attempt]:
        attempts = [loads_or_default(a, [""]) for a in raw_attempts]
        filled = [fill_input(self.preload, *attempt) for attempt in attempts]
        results = container.runner.run_batch(filled)
        return [
            Attempt(
                question=self.name,
                username=username,
                course=course,
                semester=semester,
                idx=i,
                attempt=attempt,
                grade=grade_result(result, self.expect),
                is_admissible=is_admissible(result),
                is_genuine=attempt != ["", "", ""],
                extra_data={},
            )
            for i, (attempt, result) in enumerate(zip(attempts, results))
        ]


def fill_input(preload, value):
    return re.sub(r"\{\[.*?\]\}", value, preload)



def grade_result(result, expect):
    return 1 if result.stdout.rstrip() == expect.rstrip() else 0


def is_admissible(result):
    return result.status == 0

def loads_or_default(data, default=""):
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        return default
