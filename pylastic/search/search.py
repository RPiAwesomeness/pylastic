from typing import Optional, Union


from ..queries.clause import Clause
from ..queries import Term
from ..queries.leaf.range import Range, Number
from ..queries.leaf.match import Match, MatchQueryType
from ..queries.compound.bool import Bool, Occurrence


class Search:
    @property
    def query(self) -> Clause:
        return self._query

    @query.setter
    def query(self, query: Union[Clause, None]):
        self._query = query

    @query.getter
    def query(self) -> Clause:
        if self._query is None:
            self._query = Clause()

        return self._query

    def __init__(self, index: str, query: Optional[Clause] = None) -> None:
        self.index = index
        self._query = query

    def run(self):
        """Executes the search utilizing the configured queries on the index specified"""
        pass

    def term(self, field: str, value: str) -> "Search":
        self.query.children.append(Term(field, value))
        return self

    def match(self, field: str, query: MatchQueryType) -> "Search":
        self.query.children.append(Match(field, query))
        return self

    def range(
        self,
        field: str,
        gt: Optional[Number] = None,
        lt: Optional[Number] = None,
        gte: Optional[Number] = None,
        lte: Optional[Number] = None,
        eq: Optional[Number] = None,
        format: Optional[str] = None,
    ) -> "Search":
        self.query.children.append(Range(field, gt, lt, gte, lte, eq, format))
        return self

    def must(self, *queries: Occurrence) -> "Search":
        self.query.children.append(Bool(*queries))
        return self

    def filter(self, *queries: Occurrence) -> "Search":
        self.query.children.append(Bool(*queries))
        return self

    def should(self, *queries: Occurrence) -> "Search":
        self.query.children.append(Bool(*queries))
        return self

    def must_not(self, *queries: Occurrence) -> "Search":
        self.query.children.append(Bool(*queries))
        return self
