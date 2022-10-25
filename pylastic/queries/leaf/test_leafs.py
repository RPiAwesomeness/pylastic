from typing import Any, Dict, Optional
import pytest


from .match import Match
from .range import Range
from .term import Term


def test_Term_dumps():
    term = Term("field", "value")
    assert term.dump() == {"term": {"field": "value"}}


def test_Term_raises_with_None_value():
    with pytest.raises(ValueError, match="value parameter must not be None"):
        Term("field", None)


def test_Range_dumps():
    rng = Range("field", gt=1)
    assert rng.dump() == {"range": {"field": {"gt": 1}}}


def test_Range_raises_with_no_range_param():
    with pytest.raises(
        ValueError, match="Range query must have at least one of gt, lt, gte, lte, eq"
    ) as ex:
        rng = Range("field")


def test_Match_dumps():
    match = Match("field", "testMatch")
    assert match.dump() == {"match": {"field": {"query": "testMatch"}}}


def test_Match_raises_with_None_query():
    with pytest.raises(ValueError, match="query parameter must not be None"):
        match = Match("field", None)
