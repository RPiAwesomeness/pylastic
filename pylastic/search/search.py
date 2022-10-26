from typing import Any, Dict, Optional, Union

from ..queries import Term
from ..queries.clause import Clause, Compound
from ..queries.leaf import Leaf, Range, Match
from ..queries.leaf.range import Number
from ..queries.leaf.match import MatchQueryType
from ..queries.compound.bool import Bool, Must, Should, Filter, MustNot, Occurrence


class SearchQueryException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class Search:
    def __init__(self, index: str, query: Optional[Clause] = None) -> None:
        if not index:
            raise ValueError("index must have valid string value")
        self.index = index
        self.query = None
        if query is not None:
            self.add_new_clause(query)

    def add_new_clause(self, clause: Clause):
        if self.query is None:
            if isinstance(clause, Must):
                self.query = Bool(must=[clause])
            elif isinstance(clause, Should):
                self.query = Bool(should=[Clause])
            elif isinstance(clause, Filter):
                self.query = Bool(filter=[Clause])
            elif isinstance(clause, MustNot):
                self.query = Bool(must_not=[Clause])
            elif isinstance(clause, (Leaf, Bool)):
                # If no query exists no point in doing other tests, just set the root
                self.query = clause
            else:
                raise TypeError(f"Invalid clause type {type(clause)}")

            return

        if isinstance(self.query, Leaf):
            # A leaf is a valid query on its own but must be a child of a compound query to be combined with anythinge lse
            raise SearchQueryException(
                "root of query is a leaf (one of Term/Match/Range). To add another query clause you must use a compound query clause such as Bool"
            )
        elif not isinstance(self.query, Compound):
            # To use multiple queries a compound statement must be used
            raise SearchQueryException(
                f"root of query with multiple clauses must be of the compound type, currently it is {type(self.query)}"
            )

        self.query.children.append(clause)

    def dump_query(self) -> Union[Dict[str, Any], None]:
        return None if self.query is None else self.query.dump()

    def run(self):
        """Executes the search utilizing the configured queries on the index specified"""
        pass

    def term(self, field: str, value: str) -> "Search":
        self.add_new_clause(Term(field, value))
        return self

    def match(self, field: str, query: MatchQueryType) -> "Search":
        self.add_new_clause(Match(field, query))
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
        self.add_new_clause(Range(field, gt, lt, gte, lte, eq, format))
        return self

    def must(self, query: Occurrence, *queries: Occurrence) -> "Search":
        self.add_new_clause(Bool(must=[query, *queries]))
        return self

    def filter(self, query: Occurrence, *queries: Occurrence) -> "Search":
        self.add_new_clause(Bool(filter=[query, *queries]))
        return self

    def should(self, query: Occurrence, *queries: Occurrence) -> "Search":
        self.add_new_clause(Bool(should=[query, *queries]))
        return self

    def must_not(self, query: Occurrence, *queries: Occurrence) -> "Search":
        self.add_new_clause(Bool(must_not=[query, *queries]))
        return self
