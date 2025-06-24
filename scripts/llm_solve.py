from pprint import pprint

import database.setup
import llm.solver
from llm.completion import Completion
from questions.cardsort import Cardsort
from questions.refute import Refute
from questions.reverse_trace import ReverseTrace

from dotenv import load_dotenv

load_dotenv()

with database.setup.connection("data/database.db") as con:
    cardsorts = Cardsort.fetch_all(con)
    refutes = Refute.fetch_all(con)
    reverse_traces = ReverseTrace.fetch_all(con)

pprint(refutes)

with llm.solver.client() as client:
    completions = llm.solver.solve(client, reverse_traces[0], n=1)

pprint(completions)

with database.setup.connection("data/database.db", (Completion,)) as con:
    Completion.persist(con, *completions)
    # pprint(Completion.fetch_all(con))