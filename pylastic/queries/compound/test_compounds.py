from typing import Dict, List, Any
import pytest

from .. import Term
from ..clause import Clause

from .bool import Must, Filter, Occurrence, Should, MustNot


@pytest.mark.parametrize(
    "cls,clauses,expected",
    [
        (
            Must,
            [Term("fieldName", "value")],
            {"must": {"term": {"fieldName": "value"}}},
        ),
        (
            Filter,
            [Term("fieldName", "value")],
            {"filter": {"term": {"fieldName": "value"}}},
        ),
        (
            Should,
            [Term("fieldName", "value")],
            {"should": {"term": {"fieldName": "value"}}},
        ),
        (
            MustNot,
            [Term("fieldName", "value")],
            {"must_not": {"term": {"fieldName": "value"}}},
        ),
        (
            Must,
            [Term("fieldName", "value"), Term("fieldName2", "value2")],
            {
                "must": [
                    {"term": {"fieldName": "value"}},
                    {"term": {"fieldName2": "value2"}},
                ]
            },
        ),
    ],
)
def test_dump_bool_clauses(
    cls: Occurrence,
    clauses: List[Clause],
    expected: Dict[str, Dict[str, Any]],
):
    instance = cls(*clauses)
    dumped = instance.dump()
    assert "bool" in dumped
    assert dumped["bool"] == expected
