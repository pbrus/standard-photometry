"""
Test package of the sphot.columns module.
"""

import pytest
from sphot.columns import Columns


@pytest.fixture
def init_columns():
    return Columns(['2', '3'])


@pytest.mark.parametrize("column, value", [
    ("2", "number"),
    ("454", "number"),
    ("4:8", "range"),
    ("5:13", "range")
])
def test_column_type(init_columns, column, value):
    assert init_columns._column_type(column) == value


@pytest.mark.parametrize("start, end", [
    (15, 15),
    (9, 8),
    (7, 2)
])
def test_validate_range(init_columns, start, end):
    with pytest.raises(ValueError):
        init_columns._validate_range(start, end)


@pytest.mark.parametrize("column, start, end", [
    ("3:5", 3, 5),
    ("12:16", 12, 16),
    ("4:14", 4, 14)
])
def test_split_range(init_columns, column, start, end):
    assert Columns.split_range(column) == (start, end)


@pytest.mark.parametrize("input_list, output_list", [
    (["2", "4", "7:11", "15"], [1, 3, 6, 7, 8, 9, 10, 14]),
    (["1", "2:3", "7", "9:12"], [0, 1, 2, 6, 8, 9, 10, 11]),
    (["101:105"], [100, 101, 102, 103, 104])
])
def test_indexes(input_list, output_list):
    columns = Columns(input_list)
    assert columns.indexes == output_list
