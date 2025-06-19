import json
import re
from dataclasses import dataclass
from typing import Self, override

import container.runner
from attempts.attempt import Attempt
from moodle.xml import RawQuestion
from questions.question import Question


@dataclass
class Refute(Question):
    prompt: str
    preload: str
    test: str

    @classmethod
    @override
    def from_raw(cls, moodle_xml: RawQuestion) -> Self:
        return Refute(
            name=moodle_xml["name"],
            prompt=moodle_xml["prompt"],
            preload=moodle_xml["globalextra"],
            test=moodle_xml["tests"][0]["code"],
        )

    @override
    def json_to_attempt(self, json_object: object) -> object:
        return json_object

    @override
    def json_schema(self) -> dict[str, object]:
        return {
            "type": "object",
            "properties": {
                "given": {"type": "string", "strict": True, },
                "then": {"type": "string", "strict": True, },
                "but": {"type": "string", "strict": True, },
            },
            "required": ["given", "then", "but"],
            "strict": True,
        }

    @override
    def instructions(self) -> str:
        return self.prompt

    @override
    def question(self) -> str:
        parts = re.split(r"\{\s*\[\s*\d+\s*\]\s*\}", self.preload)
        return "???".join(parts)

    @override
    def grade_attempts(
          self,
          username: str,
          course: str,
          semester: str,
          raw_attempts: list[str],
    ) -> list[Attempt]:
        attempts = [loads_or_default(a, ["", "", ""]) for a in raw_attempts]
        filled = [zip_values(self.test, *attempt) for attempt in attempts]
        results = container.runner.run_batch(filled)
        return [
            Attempt(
                question=self.name,
                username=username,
                course=course,
                semester=semester,
                idx=i,
                attempt=attempt,
                grade=grade_result(attempt, result),
                is_admissible=is_admissible(result),
                is_genuine=attempt != ["", "", ""],
                extra_data={},
            )
            for i, (attempt, result) in enumerate(zip(attempts, results))
        ]


def zip_values(template, given, then, but):
    return (
        template
        .replace("{[given]}", given)
        .replace("{[then]}", then)
        .replace("{[but]}", but)
    )


def grade_result(attempt, result) -> float:
    if result.status == 0 and attempt[1].strip() != attempt[2].strip():
        return 1
    else:
        return 0


def is_admissible(result) -> bool:
    return result.status == 0 or "AssertionError" in result.stderr


def loads_or_default(data, default=""):
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        return default
