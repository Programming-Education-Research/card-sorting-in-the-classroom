import json
from collections import defaultdict
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import IO


def load(responses: IO):
    """Returns the responses from students' first attempt at a given quiz"""
    norm_responses = normalize_responses(json.load(responses)[0])
    by_attempts = fold_responses(norm_responses)
    attempts = {
        username: pivot_questions(attempt)
        for username, attempt in first_attempts(by_attempts).items()
    }
    return by_question(attempts)


def by_question(attempts):
    result = defaultdict(dict)
    for username, user_attempts in attempts.items():
        for question, responses in user_attempts.items():
            result[question][username] = responses
    return result


def pivot_questions(attempts):
    question_to_attempts = defaultdict(list)
    for attempt in attempts:
        for question, response in attempt.items():
            if response != "-":
                question_to_attempts[question].append(response)
    return question_to_attempts


def fold_responses(responses: Sequence[Mapping]) -> Mapping[str, Mapping]:
    usernames_to_attempts = defaultdict(lambda: defaultdict(list))
    for response in responses:
        username = response["username"]
        started_on = response["startedon"]
        student_responses = response["responses"]
        usernames_to_attempts[username][started_on].append(student_responses)
    return usernames_to_attempts


def first_attempts(responses: Mapping[str, Mapping]):
    username_to_first_attempt = {}
    for username, attempts in responses.items():
        first_attempt = min(attempts)
        username_to_first_attempt[username] = attempts[first_attempt]
    return username_to_first_attempt


def normalize_responses(responses):
    return [
        {
            "username": response["username"],
            "startedon": parse_time(response["startedon"]),
            "responses": {
                int(r.strip("response")): v
                for r, v in response.items()
                if r.startswith("response")
            },
        }
        for response in responses
    ]


def parse_time(timestamp: str) -> datetime:
    return datetime.strptime(timestamp, "%d %B %Y  %I:%M %p")