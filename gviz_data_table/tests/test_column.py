import pytest
from gviz_data_table.column import Column

minimal_schema = dict(id='age', type=int)
valid_schema = {'id':'age', 'type':int, 'label':'Age', 'options':{}}


def test_conditional():
    import sys
    if sys.version_info > (3, 0):
        with pytest.raises(NameError):
            s = basestring
            s = unicode

def test_constructor():
    col = Column(**minimal_schema)
    assert col.id == 'age'
    assert col.type == int

    schema = minimal_schema.copy()
    schema['options'] = dict(width=100)
    col = Column(**schema)
    assert col.options == {'width': 100}

    col = Column(**valid_schema)
    assert col.id == 'age'
    assert col.type == int
    assert col.label == 'Age'
    assert col.options == {}

def test_validate_id():
    col = Column(**minimal_schema.copy())
    with pytest.raises(ValueError):
        col.id = 1

def test_validate_type():
    col = Column(**minimal_schema.copy())
    with pytest.raises(ValueError):
        col.type = dict

def test_validate_label():
    col = Column(**minimal_schema.copy())
    with pytest.raises(ValueError):
        col.label = 4

def test_invalid_options():
    col = Column(**minimal_schema.copy())
    assert col.options is None
    with pytest.raises(ValueError):
        col.options = "Age"

def test_dictionary_interface():
    col = Column(**minimal_schema.copy())
    assert dict(col) == {'id':'age', 'type':'number', 'label':'age'}

    schema = valid_schema.copy()
    col = Column(**schema)
    assert dict(col) == {'id':'age', 'type':'number', 'label':'Age'}

    schema['options'] = {'style':'bold', 'width':100, 'color':'red'}
    col = Column(**schema)
    assert dict(col) == {'id':'age', 'type':'number', 'label':'Age',
                         'options':{'style':'bold', 'width':100, 'color':'red'}
                         }
