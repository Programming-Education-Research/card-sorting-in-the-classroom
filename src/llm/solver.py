import json
import os
from collections.abc import Generator
from contextlib import contextmanager
from datetime import datetime

from openai import OpenAI
from ratelimit import limits

__all__ = ("solve", "client")

from llm.completion import Completion
from llm.types import ResponseFormat
from questions.question import Question


def full_schema(schema_part) -> ResponseFormat:
    return {
        "type": "json_schema",
        "json_schema": {
            "name": "question",
            "schema": {
                "type": "object",
                "properties": {
                    "explanation": {"type": "string"},
                    "answer": schema_part,
                },
                "required": ["explanation", "answer"],
                "additionalProperties": False,
                "strict": True,
            },
            "strict": True,
        },
    }


@contextmanager
def client() -> Generator[OpenAI]:
    yield OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def instruction(prompt: str) -> str:
    return f"{prompt}\n\nShow working for each step."


# One call a second — OpenAI's rate limits are weird. I can't figure them out
@limits(calls=1, period=1)
def generate_responses(*, n, client, prompt, schema, question, model):
    messages = [
        {"role": "system", "content": instruction(prompt)},
        {"role": "user", "content": question},
    ]
    completion = client.chat.completions.create(
        model=model, messages=messages, response_format=schema, n=n,
    )
    return [json.loads(choice.message.content) for choice in completion.choices]


def solve(
      client: OpenAI,
      question: Question,
      *,
      n: int,
      model: str = "gpt-4o",
) -> list[Completion]:
    now = datetime.now()
    responses = generate_responses(
        n=n,
        client=client,
        prompt=instruction(question.instructions()),
        schema=full_schema(question.json_schema()),
        question=question.question(),
        model=model,
    )
    result = []
    for response in responses:
        grade = question.grade_completion(
            question.json_to_attempt(response["answer"]),
        )
        result.append(
            Completion(
                name=question.name,
                model=model,
                date=now,
                explanation=response["explanation"],
                attempt=question.json_to_attempt(response["answer"]),
                grade=grade.grade,
                is_admissible=grade.is_admissible,
                is_genuine=grade.is_genuine,
                extra_data=grade.extra_data,
            )
        )
    return result
