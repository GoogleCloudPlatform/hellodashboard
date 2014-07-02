import pytest
from gviz_data_table.cell import Cell


def test_valid_data():
    c = Cell(int, 1)
    assert c.value == 1
    assert c.type == int

    c = Cell(str, 'a')
    assert c.value == 'a'
    assert c.type == str

def test_empty_cell():
    c = Cell(int, None)
    assert c.value is None

def test_invalid_data():
    c = Cell(int, 1)
    with pytest.raises(ValueError):
        c.validate("a")

def test_label():
    c = Cell(int, 1)
    assert c.label is None
    c = Cell(int, 1, "Birthday")
    assert c.label == "Birthday"

def test_invalid_options():
    c = Cell(int, 1)
    with pytest.raises(ValueError):
        c.options = 1
    with pytest.raises(ValueError):
        c.options = [1, 2, 3]

def test_options():
    c = Cell(int, 1)
    c.options = dict(foo='bar')
    assert c.options == {'foo':'bar'}

def test_dictionary_interface():
    c = Cell(int, 1, "Number", {'foo':'bar'})
    expected = dict(v=1, f="Number", p={'foo':'bar'})
    assert dict(c) == expected
