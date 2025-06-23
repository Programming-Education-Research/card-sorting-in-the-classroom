import json
from dataclasses import dataclass
from typing import Self, override, Final

import cardy

from attempts.attempt import Attempt
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

    @override
    def grade_completion(self, attempt):
        return Attempt(
            question=self.name,
            username="LLM",
            course="BeepBoop",
            semester="Online",
            idx=0,
            attempt=attempt,
            grade=1 - norm_distance(self.answer, attempt, self.is_ordered),
            is_admissible=is_admissible(self.answer, attempt),
            is_genuine=(
                  norm_distance(self.preload, attempt, self.is_ordered) != 0
            ),
            extra_data={"all_moved": len(attempt.get("Cards", set())) == 0},
        )

    @override
    def grade_attempts(
          self,
          username: str,
          course: str,
          semester: str,
          raw_attempts: list[str],
    ) -> list[Attempt]:
        attempts = [parse_groups(a) for a in raw_attempts]
        return [
            Attempt(
                question=self.name,
                username=username,
                course=course,
                semester=semester,
                idx=i,
                attempt=attempt,
                grade=1 - norm_distance(self.answer, attempt, self.is_ordered),
                is_admissible=is_admissible(self.answer, attempt),
                is_genuine=(
                      norm_distance(self.preload, attempt, self.is_ordered) != 0
                ),
                extra_data={"all_moved": len(attempt.get("Cards", set())) == 0},
            )
            for i, attempt in enumerate(attempts)
        ]

    def cards(self) -> list[str]:
        return [card for group in self.preload.values() for card in group]


def parse_ordering(preload: str) -> bool:
    data = json.loads(preload)
    return data["cardsort"][0]["config"]["groupOrder"]


def parse_groups(data: str) -> dict[str, list[str]]:
    data = loads_or_default(data)
    groups = data["cardsort"][0]["groups"]
    return {
        group["title"]: [card["prompt"] for card in group["cards"]]
        for group in groups
    }


def norm_distance(
      probe: dict[str, list[str]],
      sort: dict[str, list[str]],
      is_ordered: bool,
) -> float:
    if is_ordered:
        probe = {group: set(cards) for group, cards in probe.items()}
        sort = {group: set(cards) for group, cards in sort.items()}
        cards = len([c for g in probe.values() for c in g])
        return sum(
            len(probe[group] - sort.get(group, set()))
            for group in probe
        ) / cards
    else:
        return cardy.norm_distance(
            [set(g) for g in probe.values()],
            [set(g) for g in sort.values()],
            num_groups=len(probe)
        )


def is_admissible(answer, sort):
    return (
          set(answer) == set(sort)
          and set(c for g in answer.values() for c in g)
          == set(c for g in sort.values() for c in g)
    )


def loads_or_default(data):
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        return {"cardsort": [{"groups": []}]}
