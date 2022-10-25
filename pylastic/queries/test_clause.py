from typing import Optional
import pytest

from .leaf import Leaf


def test_Leaf_throws_with_invalid_field_param():
    with pytest.raises(
        ValueError, match="field parameter must have valid string value"
    ):
        Leaf(None)
    with pytest.raises(
        ValueError, match="field parameter must have valid string value"
    ):
        Leaf("")
