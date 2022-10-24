from typing import Optional, Union

from ..clause import Leaf

Number = Union[int, float, complex]


class Range(Leaf):
    gt: Optional[Number]
    lt: Optional[Number]
    gte: Optional[Number]
    lte: Optional[Number]
    eq: Optional[Number]
    format: Optional[str]

    def __init__(
        self,
        field: str,
        gt: Optional[Number] = None,
        lt: Optional[Number] = None,
        gte: Optional[Number] = None,
        lte: Optional[Number] = None,
        eq: Optional[Number] = None,
        format: Optional[str] = None,
    ) -> None:
        fields = {
            gt: gt,
            lt: lt,
            gte: gte,
            lte: lte,
            eq: eq,
        }
        if not any(fields.values()):
            raise ValueError(
                "Range query must have at least one of gt, lt, gte, lte, eq"
            )

        super().__init__(field, **fields)
