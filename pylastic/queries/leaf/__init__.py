from typing import Any, Dict, Optional


from ..compound.bool import Bool
from ..clause import Clause


class Leaf(Clause):
    def __init__(self, field: str, value: Optional[Any] = None, **kwargs: Any):
        if not field:
            raise ValueError("field parameter must have valid string value")

        super().__init__(**kwargs)

        self.field = field
        self._field_val = value
        self._params = kwargs

    def dump(self) -> Dict[str, Any]:
        if self._field_val:
            return {self.field: self._field_val}
        return {self.field: self._params}

    def __and__(self, rhs: Clause) -> Bool:
        return Bool(must=[self, rhs])


from .match import Match
from .range import Range
from .term import Term

__all__ = ["Match", "Range", "Term"]
