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
    def __init__(self, *query: Clause) -> None:
        if not query:
            raise ValueError("must query must have at least 1 clause")
        super().__init__(must=query)


class Filter(Bool):
    def __init__(self, *query: Clause) -> None:
        if not query:
            raise ValueError("filter query must have at least 1 clause")
        super().__init__(filter=query)


class Should(Bool):
    def __init__(self, *query: Clause) -> None:
        if not query:
            raise ValueError("should query must have at least 1 clause")
        super().__init__(should=query)


class MustNot(Bool):
    def __init__(self, *query: Clause) -> None:
        if not query:
            raise ValueError("must_not query must have at least 1 clause")
        super().__init__(must_not=query)


Occurrence = Union[Must, Filter, Should, MustNot]
