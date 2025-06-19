import json
from dataclasses import dataclass
from types import MappingProxyType

from database.orm import SimpleOrm, field


@dataclass
class Attempt(SimpleOrm):
    question: field(str, primary=True)
    username: field(str, primary=True)
    course: field(str, primary=True)
    semester: field(str, primary=True)
    idx: field(int, primary=True)
    attempt: field(
        object,
        marshal=json.dumps,
        unmarshal=json.loads,
    )
    grade: float
    is_admissible: bool
    is_genuine: bool
    extra_data: field(
        dict[str, object] | None,
        marshal=json.dumps,
        unmarshal=json.loads,
    ) = MappingProxyType({})
