from abc import ABC, abstractmethod
from typing import Any, Dict, List


class Clause(ABC):
    def __init__(self, **kwargs) -> None:
        super().__init__()

        for key, arg in kwargs.items():
            setattr(self, key, arg)

    def __iter__(self):
        yield self.name(), {
            key: value for key, value in vars(self).items() if not key.startswith("_")
        }

    def dump(self) -> Dict[str, Any]:
        """Dumps a dict with the clause's name and attributes"""
        return dict(self)

    @abstractmethod
    def name(self) -> str:
        ...

    # TODO: Implement overloaded operator support? (eg. Clause() & Clause()/Clause() | Clause()/Clause() and Clause())


class Compound(Clause):
    children: List[Clause]

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
