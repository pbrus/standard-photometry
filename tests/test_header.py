"""
Test package of the sphot.header module.
"""

import pytest
from sphot.header import Header


@pytest.fixture
def path_to_data():
    return r'test_data/'


@pytest.mark.parametrize("columns", [
    ['1', '3', '5:12'],
    ['1', '2', '3', '4', '5', '6', '7'],
    ['5:8', '10:13', '20:33']
])
def test_check_column_numbers(path_to_data, columns):
    with pytest.raises(ValueError):
        Header(path_to_data + r'/header.dat', columns)
