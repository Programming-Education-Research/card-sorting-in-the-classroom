from typing import TypedDict, Required, Optional, Literal


class JSONSchema(TypedDict, total=False):
    name: Required[str]
    description: str
    schema: dict[str, object]
    strict: Optional[bool]


class ResponseFormat(TypedDict, total=False):
    json_schema: Required[JSONSchema]
    type: Required[Literal["json_schema"]]
