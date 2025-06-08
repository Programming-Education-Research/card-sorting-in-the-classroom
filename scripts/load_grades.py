from typing import Final

import database.setup
import moodle
from grades.grade import Grade
from grades.utils import from_raw

TABLES: Final[tuple[type[Grade], ...]] = (Grade,)

cs101ss = {
    "Test1": "../data/raw/CS101SS_Test1.csv",
    "Test2": "../data/raw/CS101SS_Test2.csv",
    "Test3": "../data/raw/CS101SS_Test3.csv",
    "Exam": "../data/raw/CS101SS_Exam.csv",
}
cs130ss = {
    "Test": "../data/raw/CS130SS_Test.csv",
    "Exam": "../data/raw/CS130SS_Exam.csv",
}
# cs101s1 = {
#     "Test1": "../data/raw/CS101S1_Test1.csv",
#     "Test2": "../data/raw/CS101S1_Test2.csv",
#     "Test3": "../data/raw/CS101S1_Test3.csv",
#     "Exam": "../data/raw/CS101S1_Exam.csv",
# }
# cs130s1 = {
#     "Test": "../data/raw/CS130S1_Test.csv",
#     "Exam": "../data/raw/CS130S1_Exam.csv",
# }

with database.setup.connection("../data/database.db", TABLES) as con:
    for spec in cs101ss, cs130ss:
        scores = [from_raw(score) for score in moodle.grades.load(spec)]
        for score in scores:
            Grade.persist(con, score)
