"""
Test package of the sphot.header module.
"""

import pytest
from sphot.header import Header


@pytest.fixture
def path_to_data():
    return r'tests/test_data/'


@pytest.fixture
def labels():
    labels = [
        'index',
        'U_ins', 'U_ierr', 'U_std', 'U_serr',
        'B_ins', 'B_ierr', 'B_std', 'B_serr',
        'V_ins', 'V_ierr', 'V_std', 'V_serr',
        'I_ins', 'I_ierr', 'I_std', 'I_serr'
    ]
    return labels


@pytest.fixture
def header(path_to_data):
    return Header(path_to_data + r'header.dat', ['1:17'])


@pytest.mark.parametrize("columns", [
    ['1', '3', '5:12'],
    ['1', '2', '3', '4', '5', '6', '7'],
    ['5:8', '10:13', '20:33']
])
def test_check_column_numbers(path_to_data, columns):
    with pytest.raises(ValueError):
        Header(path_to_data + r'header.dat', columns)


def test_get_passband_labels(header):
    passband_labels = ['U', 'B', 'V', 'I']
    assert header._get_passband_labels() == passband_labels


def test_get_passband_column_labels(header, labels):
    assert header._get_passband_column_labels() == labels


def test_labels(header, labels):
    assert header.labels == labels


def test_identifier(header):
    assert header.identifier == "index"
