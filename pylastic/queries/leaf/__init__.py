from typing import Any, Optional


from ..compound.bool import Bool
from ..clause import Clause


class Leaf(Clause):
    def __init__(self, field: str, value: Optional[Any] = None, **kwargs: Any):
        if not field:
            raise ValueError("field parameter must have valid string value")

        super().__init__(**kwargs)

        self.field_name = field
        self._field_val = value
        self._params = kwargs

    def dump(self):
        return dict(self)

    def __and__(self, rhs: Clause) -> Bool:
        return Bool(must=[self, rhs])

    def __or__(self, rhs: Clause) -> Bool:
        return Bool(should=[self, rhs])

    def __iter__(self):
        yield self.name(), {
            self.field_name: self._field_val if self._field_val else self._params
        }


from .match import Match
from .range import Range
from .term import Term

__all__ = ["Match", "Range", "Term"]
