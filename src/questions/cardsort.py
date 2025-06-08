import json
from dataclasses import dataclass
from typing import Self, override, Final

from database.orm import field
from moodle.xml import RawQuestion
from questions.question import Question

CARD_SPEC: Final = {
    "Cards": {
        "type": "array",
        "max_items": 0,
        "items": {"type": "string"},
        "strict": True
    }
}


@dataclass
class Cardsort(Question):
    prompt: str
    preload: field(
        dict[str, list[str]],
        marshal=json.dumps,
        unmarshal=json.loads,
    )
    answer: field(
        dict[str, list[str]],
        marshal=json.dumps,
        unmarshal=json.loads,
    )
    is_ordered: bool

    @classmethod
    @override
    def from_raw(cls, moodle_xml: RawQuestion) -> Self:
        return Cardsort(
            name=moodle_xml["name"],
            prompt=moodle_xml["prompt"],
            preload=parse_groups(moodle_xml["preload"]),
            answer=parse_groups(moodle_xml["answer"]),
            is_ordered=parse_ordering(moodle_xml["preload"]),
        )

    @override
    def json_to_attempt(
          self,
          json_object: dict[str, list[str]]
    ) -> dict[str, list[str]]:
        labelled_cards = {
            f"Card {i}": card
            for i, card in enumerate(self.cards(), start=1)
        }
        return {
            group: [labelled_cards[card] for card in cards]
            for group, cards in json_object.items()
        }

    @override
    def json_schema(self) -> dict[str, object]:
        labels = [f"Card {i}" for i in range(1, len(self.cards()) + 1)]
        groups = {
            group: {
                "type": "array",
                "items": {"type": "string", "enum": labels},
                "strict": True,
            }
            for group in self.preload
            if group.lower() != "cards"
        }
        return {
            "type": "object",
            "properties": groups | CARD_SPEC,
            "required": ["Cards", *groups],
            "additionalProperties": False,
            "strict": True,
        }

    @override
    def instructions(self) -> str:
        return self.prompt

    @override
    def question(self) -> str:
        labelled_cards = {
            card: f"Card {i}\n{card}"
            for i, card in enumerate(self.cards(), start=1)
        }
        groups = {
            group: [labelled_cards[card] for card in cards]
            for group, cards in self.preload.items()
        }
        return json.dumps(groups)

    def cards(self) -> list[str]:
        return [card for group in self.preload.values() for card in group]


def parse_ordering(preload: str) -> bool:
    data = json.loads(preload)
    return data["cardsort"][0]["config"]["groupOrder"]


def parse_groups(data: str) -> dict[str, list[str]]:
    data = json.loads(data)
    groups = data["cardsort"][0]["groups"]
    return {
        group["title"]: [card["prompt"] for card in group["cards"]]
        for group in groups
    }
