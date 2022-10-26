from abc import abstractmethod
import functools
from itertools import groupby
from typing import List, Any, Optional, Dict, Union

from ..clause import Clause, Compound


def validate_queries(func):
    @functools.wraps(func)
    def wrapper(self, query: Clause, *queries: Clause):
        if not query:
            raise ValueError("must query must have at least 1 clause")
        # Only one of each query occurrence can be present
        for q_type, group in groupby([query, *queries], lambda q: q.name()):
            group_len = len(list(group))
            if group_len > 1:
                raise ValueError(
                    f"Must query can only have one of each occurrence, have {group_len} of {q_type}"
                )

        func(self, query, *queries)

    return wrapper


class BoolOccurrence(Clause):
    @validate_queries
    def __init__(self, query: Clause, *queries: Clause) -> None:
        super().__init__()
        self.clauses = [query, *queries]

    def __iter__(self):
        yield self.name(), {
            name: contents for clause in self.clauses for name, contents in clause
        }


class Must(BoolOccurrence):
    """Elasticsearch must clause - equivalent to AND"""

    def name(self) -> str:
        return "must"


class Filter(BoolOccurrence):
    def name(self) -> str:
        return "filter"


class Should(BoolOccurrence):
    """Elasticsearch should clause - equivalent to OR"""

    def __init__(self, query: Clause, *queries: Clause) -> None:
        if not query:
            raise ValueError("should query must have at least 1 clause")
        self.clauses = [query, *queries]

    def __iter__(self):
        yield self.name(), [clause.dump() for clause in self.clauses]

    def dump(self) -> Dict[str, List[Clause]]:
        return {self.name(): [clause.dump() for clause in self.clauses]}

    def name(self) -> str:
        return "should"


class MustNot(BoolOccurrence):
    """Elasticsearch must_not clause - equivalent to NOR"""

    def name(self) -> str:
        return "must_not"


class Bool(Compound):
    must: Union[Must, None]
    filter: Union[Filter, None]
    should: Union[Should, None]
    must_not: Union[MustNot, None]

    def __init__(
        self,
        must: Optional[List[Clause]] = None,
        filter: Optional[List[Clause]] = None,
        should: Optional[List[Clause]] = None,
        must_not: Optional[List[Clause]] = None,
    ) -> None:
        if must is not None and not isinstance(must, list):
            raise TypeError("must parameter must be a list")
        if filter is not None and not isinstance(filter, list):
            raise TypeError("filter parameter must be a list")
        if should is not None and not isinstance(should, list):
            raise TypeError("should parameter must be a list")
        if must_not is not None and not isinstance(must_not, list):
            raise TypeError("must_not parameter must be a list")

        self.must = Must(*must) if must else None
        self.filter = Filter(*filter) if filter else None
        self.should = Should(*should) if should else None
        self.must_not = MustNot(*must_not) if must_not else None

        if not any(vars(self)):
            raise ValueError(
                "bool must have at least one query clause of must, filter, should, or must_not"
            )

        super().__init__()

    def dump(self) -> Dict[str, Dict[str, Any]]:
        return {
            self.name(): {
                name: clause
                for occurrence in vars(self).values()
                if occurrence is not None
                for name, clause in occurrence
            }
        }

    def name(self) -> str:
        return "bool"


Occurrence = Union[Must, Filter, Should, MustNot]
