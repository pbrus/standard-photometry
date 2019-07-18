"""
Test package of the sphot.data module.
"""
import pytest
from numpy import allclose

from sphot.data import Data


@pytest.fixture
def path_to_data():
    return r'tests/test_data/'


@pytest.fixture
def data1(path_to_data):
    return Data(path_to_data + r'data1.dat', ['1:17'])


@pytest.mark.parametrize("values, index", [
    ([[1.2976, 0.00758024, 3.5527, 0.05925757]], 0),
    ([[2.6743, 0.00411096, 2.411, 0.00783901]], 1),
    ([[7.86600000e-01, 8.10493677e-03, 3.12580000e+00, 2.14009346e-03]], 2),
    ([[0.7866, 0.00810494, 0.4479, 0.00158114]], 3)
])
def test_sets(data1, index, values):
    assert allclose(data1.sets[index].values[2:3], values)
