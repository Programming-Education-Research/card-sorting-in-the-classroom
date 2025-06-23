import sqlite3
from collections.abc import Iterable
from contextlib import contextmanager
from os import PathLike
from pathlib import Path
from sqlite3 import Connection
from typing import Final, Sequence, Generator

from database.orm import SimpleOrm

TABLES: Final[Path] = Path(__file__).parent / "tables.sql"
COMPUTED_TABLES: Final[Path] = Path(__file__).parent / "computed.sql"

FUNCTIONS: Final[Sequence] = [
]
AGGREGATES: Final[Sequence] = [
]


@contextmanager
def connection(
      path: str | PathLike[str],
      tables: Iterable[SimpleOrm] = (),
) -> Generator[Connection]:
    con = sqlite3.connect(path)
    try:
        con.execute("PRAGMA foreign_keys = 1")
        for name, nargs, func in FUNCTIONS:
            con.create_function(name, nargs, func, deterministic=True)
        for name, nargs, func in AGGREGATES:
            con.create_aggregate(name, nargs, func)
        con.executescript(TABLES.read_text())
        for table in tables:
            table.create_table(con)
        yield con
    finally:
        con.executescript(COMPUTED_TABLES.read_text())
        con.close()
