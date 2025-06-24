import database.setup
import moodle
from grades.grade import Grade
from grades.utils import from_raw

grade_map = {
    ("CS101", "SS2025"): {
        "Test1": "data/raw/CS101SS_Test1.csv",
        "Test2": "data/raw/CS101SS_Test2.csv",
        "Test3": "data/raw/CS101SS_Test3.csv",
        "Exam": "data/raw/CS101SS_Exam.csv",
    },
    ("CS130", "SS2025"): {
        "Test": "data/raw/CS130SS_Test.csv",
        "Exam": "data/raw/CS130SS_Exam.csv",
    },
    # ("CS101", "S12025"): {
    #     "Test1": "data/raw/CS101S1_Test1.csv",
    #     "Test2": "data/raw/CS101S1_Test2.csv",
    #     "Test3": "data/raw/CS101S1_Test3.csv",
    #     "Exam": "data/raw/CS101S1_Exam.csv",
    # }
    ("CS130", "S12025"): {
        "Test": "data/raw/CS130S1_Test.csv",
        "Exam": "data/raw/CS130S1_Exam.csv",
    },
}

with database.setup.connection("../data/database.db", (Grade,)) as con:
    for (course, semester), spec in grade_map.items():
        for score in moodle.grades.load(spec):
            Grade.persist(con, from_raw(course, semester, score))
