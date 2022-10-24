from typing import Dict, List, Any
import pytest

from .. import Term
from ..clause import Clause

from .bool import Bool, Must, Filter, Occurrence, Should, MustNot


@pytest.mark.parametrize(
    "cls,expected_err",
    [
        (
            Bool,
            "bool must have at least one query clause of must, filter, should, or must_not",
        ),
        (Must, "must query must have at least 1 clause"),
        (Filter, "filter query must have at least 1 clause"),
        (Should, "should query must have at least 1 clause"),
        (MustNot, "must_not query must have at least 1 clause"),
    ],
)
def test_no_clause_params_raises(cls: Bool, expected_err: str):
    with pytest.raises(ValueError, match=expected_err) as ex_info:
        instance = cls()


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
