import json
from dataclasses import dataclass
from datetime import datetime

from database.orm import SimpleOrm, field


@dataclass
class Completion(SimpleOrm):
    name: str
    model: str
    date: datetime
    explanation: str
    attempt: field(object, marshal=json.dumps, unmarshal=json.loads)
