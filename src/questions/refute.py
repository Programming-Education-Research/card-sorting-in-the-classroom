import re
from dataclasses import dataclass
from typing import Self, override

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
