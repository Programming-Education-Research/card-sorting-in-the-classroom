from grades.grade import Grade


def from_raw(course, semester, data: dict[str, str | float]):
    return Grade(
        username=data["username"],
        course=course,
        semester=semester,
        grade=calculate_average(data),
        sat_exam="Exam" in data,
    )


def calculate_average(data):
    marks = [v for k, v in data.items() if k.startswith("Test") or k == "Exam"]
    return sum(marks) / len(marks) if marks else 0
