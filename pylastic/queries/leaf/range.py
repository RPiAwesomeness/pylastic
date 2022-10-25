from typing import Any, Dict, Optional, Union

from . import Leaf

Number = Union[int, float, complex]


class Range(Leaf):
    class Params:
        def __init__(
            self,
            gt: Optional[Number] = None,
            lt: Optional[Number] = None,
            gte: Optional[Number] = None,
            lte: Optional[Number] = None,
            eq: Optional[Number] = None,
            format: Optional[str] = None,
        ):
            self.gt = gt
            self.lt = lt
            self.gte = gte
            self.lte = lte
            self.eq = eq
            self.format = format

        def any(self):
            return any([self.gt, self.lt, self.gte, self.lte, self.eq, self.format])

        def dump(self) -> Dict[str, Optional[Union[str, Number]]]:
            ret = dict()
            if self.gt is not None:
                ret["gt"] = self.gt
            if self.lt is not None:
                ret["lt"] = self.lt
            if self.gte is not None:
                ret["gte"] = self.gte
            if self.lte is not None:
                ret["lte"] = self.lte
            if self.eq is not None:
                ret["eq"] = self.eq
            if self.format is not None:
                ret["format"] = self.format

            return ret

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
        fields = {"gt": gt, "lt": lt, "gte": gte, "lte": lte, "eq": eq}
        self.params = Range.Params(format=format, **fields)
        if not any(fields.values()):
            raise ValueError(
                "Range query must have at least one of gt, lt, gte, lte, eq"
            )

        super().__init__(field)

    def dump(self) -> Dict[str, Any]:
        return {"range": {self.field: self.params.dump()}}
