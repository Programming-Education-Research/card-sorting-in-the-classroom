import abc
from collections.abc import Callable
from dataclasses import dataclass
from sqlite3 import Connection
from typing import Self, Annotated, get_origin, get_args

from database.utils import cursor

PRIMITIVES = (bool, int, float, str)


@dataclass
class Field:
    type: type
    name: str
    sql_type: str = None
    primary: bool = False
    marshal: Callable[[object], object] = lambda e: e
    unmarshal: Callable[[object], object] = lambda e: e

    def replacement(self):
        return f":{self.name}"


@dataclass
class Config:
    primary: bool = False
    sql_type: str = None
    marshal: Callable[[object], object] = lambda e: e
    unmarshal: Callable[[object], object] = lambda e: e


def field[T](
      type: T,
      *,
      primary: bool = False,
      sql_type: str = None,
      marshal: Callable = lambda e: e,
      unmarshal: Callable = lambda e: e,
) -> T:
    return Annotated[type, Config(primary, sql_type, marshal, unmarshal)]


class SimpleOrm(abc.ABC):
    # Would it have been simpler with an out-of-the-box ORM?
    # Possibly. Probably, even. Almost certainly.
    # But where is the fun in that?

    @classmethod
    def _fields(cls):
        fields = []
        for resolved_cls in cls.__mro__:
            fields.append([])
            if resolved_cls is SimpleOrm:
                break
            for name, annotation in resolved_cls.__annotations__.items():
                if get_origin(annotation) is Annotated:
                    annotation, config = get_args(annotation)
                    f = Field(
                        type=annotation,
                        name=name,
                        sql_type=normalize_type(annotation, config.sql_type),
                        primary=config.primary,
                        marshal=config.marshal,
                        unmarshal=config.unmarshal,
                    )
                else:
                    f = Field(annotation, name)
                fields[-1].append(f)
        yield from [f for group in reversed(fields) for f in group]

    @classmethod
    def _field_declarations(cls):
        result = ", ".join(f"{f.name} {f.sql_type}" for f in cls._fields())
        primary = [f.name for f in cls._fields() if f.primary]
        if primary:
            primary = ", ".join(primary)
            result += ", " + f"PRIMARY KEY ({primary})"
        return result

    @classmethod
    def _marshal(cls, value):
        result = {}
        for field in cls._fields():
            result[field.name] = field.marshal(getattr(value, field.name))
        return result

    @classmethod
    def _unmarshal(cls, value):
        result = {}
        for f in cls._fields():
            result[f.name] = f.unmarshal(value[f.name])
        return cls(**result)

    @classmethod
    def table_name(cls) -> str:
        return cls.__name__

    @classmethod
    def create_table(cls, con: Connection) -> None:
        con.execute(
            f"CREATE TABLE IF NOT EXISTS {cls.table_name()} "
            f"({cls._field_declarations()})",
        )

    @classmethod
    def drop_table(cls, con: Connection) -> None:
        con.execute(f"DROP TABLE IF EXISTS {cls.table_name()}")

    @classmethod
    def persist(cls, con: Connection, *values: Self) -> None:
        con.executemany(
            f"""INSERT OR REPLACE INTO {cls.table_name()} VALUES (
                {", ".join(f.replacement() for f in cls._fields())}
            )""",
            [cls._marshal(value) for value in values],
        )

    @classmethod
    def fetch(cls, con: Connection, name: str):
        with cursor(con) as cur:
            cur.execute(
                f"SELECT * FROM {cls.table_name()} WHERE name = ?",
                (name,),
            )
            return cls._unmarshal(cur.fetchone())

    @classmethod
    def fetch_all(cls, con: Connection):
        with cursor(con) as cur:
            cur.execute(f"SELECT * FROM {cls.table_name()}")
            return [cls._unmarshal(row) for row in cur.fetchall()]


def normalize_type(cls, override):
    if override is not None:
        return override
    elif cls == int:
        return "INTEGER"
    elif cls == float:
        return "REAL"
    else:
        return "TEXT"
