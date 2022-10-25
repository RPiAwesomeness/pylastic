from abc import ABC, abstractmethod
from typing import Any, Dict, List


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
        ...

    # TODO: Implement overloaded operator support? (eg. Clause() & Clause()/Clause() | Clause()/Clause() and Clause())


class Compound(Clause):
    children: List[Clause]

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
