from typing import IO

from moodle import responses


def load(f: IO, rating_num: int, comment_num: int):
    data = responses.load(f)
    ratings = {u: a[-1] if a else None for u, a in data[rating_num].items()}
    comments = {u: a[-1] if a else None for u, a in data[comment_num].items()}
    return join(ratings, comments)


def join(ratings, comments):
    return {
        username: {
            "rating": ratings.get(username),
            "comment": comments.get(username)
        }
        for username in set(ratings).union(comments)
    }
