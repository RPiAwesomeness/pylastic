from typing import Dict, List, Any
import pytest

from .. import Term, Match
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
            {"should": [{"term": {"fieldName": "value"}}]},
        ),
        (
            MustNot,
            [Term("fieldName", "value")],
            {"must_not": {"term": {"fieldName": "value"}}},
        ),
        (
            Should,
            [Term("fieldName", "value"), Term("fieldName2", "value2")],
            {
                "should": [
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
    assert dumped == expected


def test_bool_AND():
    clause = Term("left_field", "left_value") & Match("right_field", "right_value")
    assert clause.dump() == {
        "bool": {
            "must": {
                "term": {"left_field": "left_value"},
                "match": {"right_field": {"query": "right_value"}},
            }
        }
    }


def test_bool_OR():
    clause = Term("left_field", "left_value") | Term("right_field", "right_value")
    assert clause.dump() == {
        "bool": {
            "should": [
                {"term": {"left_field": "left_value"}},
                {"term": {"right_field": "right_value"}},
            ]
        }
    }
