import pytest

from ..queries import Term, Match
from .search import Search


def test_Search_throws_with_invalid_index():
    with pytest.raises(ValueError, match="index must have valid string value"):
        s = Search("")
    with pytest.raises(ValueError, match="index must have valid string value"):
        s = Search(None)


def test_Search_empty():
    s = Search("index")
    assert s.dump_query() == None


def test_Search_constructor_clause():
    s = Search("index", Term("field", "value"))
    assert s.dump_query() == {"term": {"field": "value"}}


def test_Search_method_clause():
    s = Search("index").term("field", "value")
    assert s.dump_query() == {"term": {"field": "value"}}


def test_Search_constructor_match():
    s = Search("index", Match("matchField", "matchValue"))
    assert s.dump_query() == {"match": {"matchField": {"query": "matchValue"}}}


def test_Search_method_must_with_clause():
    s = Search("index").must(Match("matchField", "matchValue"))
    assert s.dump_query() == {
        "bool": {"must": {"match": {"matchField": {"query": "matchValue"}}}}
    }


def test_Search_method_clauses():
    s = Search("index").should(
        Match("matchField", "matchValue"), Match("matchField2", "matchValue2")
    )
    assert s.dump_query() == {
        "bool": {
            "should": [
                {"match": {"matchField": {"query": "matchValue"}}},
                {"match": {"matchField2": {"query": "matchValue2"}}},
            ]
        }
    }


def test_Search_method_clauses_different():
    s = Search("index").must(
        Match("matchField", "matchValue"), Term("termField", "termValue")
    )
    assert s.dump_query() == {
        "bool": {
            "must": {
                "match": {"matchField": {"query": "matchValue"}},
                "term": {"termField": "termValue"},
            }
        }
    }
