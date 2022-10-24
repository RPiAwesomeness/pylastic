from ..clause import Leaf


class Term(Leaf):
    def __init__(self, field: str, value: str) -> None:
        super().__init__(field, value)

    def dump(self):
        return {"term": super().dump()}
