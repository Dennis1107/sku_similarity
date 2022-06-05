# run with python -m pytest
import pytest
from sku_similarity.sku_similarity_input import input_checker_functions as icf


@pytest.mark.parametrize("input", ["sku-123", 123, int(1)])
def test_return_string(input):
    # Setup
    # Exercise
    actual = icf.return_string(input)
    # Verify
    assert type(actual) is str


@pytest.mark.parametrize("input", ["sku-123  ", " sk u- 12 3"])
def test_return_string(input):
    # Setup
    result = "sku-123"
    # Exercise
    actual = icf.remove_whitespace(input)
    # Verify
    assert result == actual


# More to come :)
