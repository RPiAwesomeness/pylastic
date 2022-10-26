from typing import Any, Dict, Union
from datetime import date, datetime

from . import Leaf

Number = Union[int, float, complex]
MatchQueryType = Union[str, Number, bool, date, datetime]


class Match(Leaf):
    def __init__(self, field: str, query: MatchQueryType) -> None:
        if query is None:
            raise ValueError("query parameter must not be None")

        super().__init__(field, query=query)

    def name(self) -> str:
        return "match"
