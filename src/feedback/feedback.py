from dataclasses import dataclass

from database.orm import SimpleOrm, field


@dataclass
class Feedback(SimpleOrm):
    question: field(str, primary=True)
    username: field(str, primary=True)
    course: field(str, primary=True)
    semester: field(str, primary=True)
    rating: int
    comments: str

    @classmethod
    def from_raw(cls, question, username, course, semester, raw_feedback):
        return Feedback(
            question=question,
            username=username,
            course=course,
            semester=semester,
            rating=rating_as_number(raw_feedback["rating"]),
            comments=raw_feedback["comment"],
        )


def rating_as_number(rating):
    return int(rating[0]) if rating is not None else None