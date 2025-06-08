import re
from dataclasses import dataclass
from typing import Self, override

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
