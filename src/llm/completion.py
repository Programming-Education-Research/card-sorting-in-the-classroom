import json
from dataclasses import dataclass
from datetime import datetime
from types import MappingProxyType

from database.orm import SimpleOrm, field


@dataclass
class Completion(SimpleOrm):
    name: str
    model: str
    date: field(datetime, unmarshal=datetime.fromisoformat)
    explanation: str
    attempt: field(object, marshal=json.dumps, unmarshal=json.loads)
    grade: float
    is_admissible: bool
    is_genuine: bool
    extra_data: field(
        dict[str, object] | None,
        marshal=json.dumps,
        unmarshal=json.loads,
    ) = MappingProxyType({})
