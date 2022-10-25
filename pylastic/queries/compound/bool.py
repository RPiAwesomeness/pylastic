from typing import List, Any, Optional, Dict, Union

from ..clause import Clause, Compound


class Bool(Compound):
    children: Dict[str, List[Union[Clause, None]]]

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

        self.children = {
            "must": must,
            "filter": filter,
            "should": should,
            "must_not": must_not,
        }
        if not any(self.children.values()):
            raise ValueError(
                "bool must have at least one query clause of must, filter, should, or must_not"
            )

        super().__init__(**self.children)

    def dump(self) -> Dict[str, Dict[str, Any]]:
        return {
            "bool": {
                name: [clause.dump() for clause in oc] if len(oc) > 1 else oc[0].dump()
                for name, oc in self.children.items()
                if oc is not None
            }
        }


class Must(Bool):
    def __init__(self, query: Clause, *queries: Clause) -> None:
        if not query:
            raise ValueError("must query must have at least 1 clause")
        super().__init__(must=[query, *queries])


class Filter(Bool):
    def __init__(self, query: Clause, *queries: Clause) -> None:
        if not query:
            raise ValueError("filter query must have at least 1 clause")
        super().__init__(filter=[query, *queries])


class Should(Bool):
    def __init__(self, query: Clause, *queries: Clause) -> None:
        if not query:
            raise ValueError("should query must have at least 1 clause")
        super().__init__(should=[query, *queries])


class MustNot(Bool):
    def __init__(self, query: Clause, *queries: Clause) -> None:
        if not query:
            raise ValueError("must_not query must have at least 1 clause")
        super().__init__(must_not=[query, *queries])


Occurrence = Union[Must, Filter, Should, MustNot]
