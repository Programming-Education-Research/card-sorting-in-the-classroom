from collections.abc import Generator
from contextlib import contextmanager
from sqlite3 import Cursor, Row, Connection


def dict_factory(cur: Cursor, row: Row):
    fields = [column[0] for column in cur.description]
    return {key: value for key, value in zip(fields, row)}


@contextmanager
def cursor(con: Connection) -> Generator[Cursor]:
    cur = con.cursor()
    try:
        cur.row_factory = dict_factory
        yield cur
    finally:
        cur.close()
