from dataclasses import dataclass

from database.orm import SimpleOrm

@dataclass
class Grade(SimpleOrm):
    username: str
    grade: float
    sat_exam: bool
