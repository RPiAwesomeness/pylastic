from typing import Dict, Optional, Union

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
            ret = {key: value for key, value in vars(self).items() if value is not None}
            print(ret)
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
        self.params = Range.Params(gt=gt, lt=lt, gte=gte, lte=lte, eq=eq, format=format)
        if not self.params.any():
            raise ValueError(
                "Range query must have at least one of gt, lt, gte, lte, eq"
            )

        super().__init__(field, **self.params.dump())

    def name(self) -> str:
        return "range"
