from typing import Optional
import pytest

from .leaf import Term


def test_Leaf_throws_with_invalid_field_param():
    with pytest.raises(
        ValueError, match="field parameter must have valid string value"
    ):
        Term(None, "value")
    with pytest.raises(
        ValueError, match="field parameter must have valid string value"
    ):
        Term("", "value")
