from abc import ABC, abstractmethod
from typing import Any, Optional, Dict, List


class Clause(ABC):
    def __init__(self, **kwargs) -> None:
        super().__init__()

        for key, arg in kwargs.items():
            setattr(self, key, arg)

    @abstractmethod
    def dump(self) -> Dict[str, Any]:
        ...

    @property
    @abstractmethod
    def __name__(self) -> str:
        return "Clause"

    # TODO: Implement overloaded operator support? (eg. Clause() & Clause()/Clause() | Clause()/Clause() and Clause())


class Leaf(Clause):
    def __init__(self, field: str, value: Optional[Any] = None, **kwargs: Any):
        super().__init__(**kwargs)

        self.field = field
        self.field_val = value
        self.params = kwargs

    def dump(self) -> Dict[str, Any]:
        ret = {self.field: self.field_val}
        ret.update(**self.params)
        return ret


class Compound(Clause):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
