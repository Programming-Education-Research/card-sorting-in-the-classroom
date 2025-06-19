from dataclasses import dataclass

from database.orm import SimpleOrm

@dataclass
class Grade(SimpleOrm):
    username: str
    course: str
    semester: str
    grade: float
    sat_exam: bool
