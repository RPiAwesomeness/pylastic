from typing import Any, Dict
from ..leaf import Leaf


class Term(Leaf):
    def __init__(self, field: str, value: str) -> None:
        if value is None:
            raise ValueError("value parameter must not be None")
        super().__init__(field, value)

    def dump(self) -> Dict[str, Any]:
        return {"term": super().dump()}
