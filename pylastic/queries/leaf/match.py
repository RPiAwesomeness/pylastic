from typing import Union
from datetime import date, datetime

from ..clause import Leaf

Number = Union[int, float, complex]
MatchQueryType = Union[str, Number, bool, date, datetime]

class Match(Leaf):
    def __init__(self, field: str, query: MatchQueryType) -> None:
        super().__init__(field, query=query)