import abc
from dataclasses import dataclass
from typing import Self

from attempts.attempt import Attempt
from database.orm import SimpleOrm, field
from moodle.xml import RawQuestion


@dataclass
class Question(SimpleOrm, abc.ABC):
    name: field(str, primary=True)

    @classmethod
    @abc.abstractmethod
    def from_raw(cls, moodle_xml: RawQuestion) -> Self:
        """Parses a MoodleXML question"""

    @abc.abstractmethod
    def json_to_attempt(self, json_object: object) -> object:
        """Parses a JSON object (as defined by `json_schema`) to an attempt"""

    @abc.abstractmethod
    def json_schema(self) -> dict[str, object]:
        """Returns the JSON Schema format for this question"""

    @abc.abstractmethod
    def instructions(self) -> str:
        """
        Returns the "prompt" or instructions for the question without showing
        the actual question itself.
        """

    @abc.abstractmethod
    def question(self) -> str:
        """Returns this question as a textual format without the prompt"""

    @abc.abstractmethod
    def grade_attempts(
          self,
          username: str,
          course: str,
          semester: str,
          raw_attempts: list[str],
    ) -> list[Attempt]:
        """Parses and grades raw attempt data from Moodle"""

    @abc.abstractmethod
    def grade_completion(self, attempt) -> Attempt:
        ...
