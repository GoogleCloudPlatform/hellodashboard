import json
import pytest
from gviz_data_table.table import Table

valid_schema = (
    {'id':'age', 'type':int, 'label':'Age'},
    {'id':'name', 'type':str, 'label':'Name'}
)

schema_missing_id = (
    {'type':int},
    {'name':'age', 'type':int}
)

bob = (18, 'Bob')
sally = (20, 'Sally')


def test_conditional():
    import sys
    if sys.version_info < (2, 7):
        with pytest.raises(ImportError):
            from collections import OrderedDict

def test_constructor():
    table = Table()
    assert list(table.schema.keys()) == []
    assert table.rows == []

def test_invalid_options():
    table = Table()
    with pytest.raises(ValueError):
        table.options = 1

    with pytest.raises(ValueError):
        table.options = [1, 2, 3]

def test_options():
    table = Table()
    table.options = dict(bar='baz')
    assert table.options == {'bar':'baz'}

def test_missing_id():
    with pytest.raises(TypeError):
        Table(schema_missing_id)

def test_duplicate_column():
    table = Table(valid_schema)
    with pytest.raises(ValueError):
        table.add_column('age', int)

def test_add_column():
    table = Table()
    table.add_column(**valid_schema[0])
    table.add_column(**valid_schema[1])
    assert table.schema['age'].id == "age"
    assert table.schema['name'].type == str
    with pytest.raises(TypeError):
        table.add_column('height')

def test_add_column_with_existing_data():
    table = Table(valid_schema)
    table.append(bob)
    with pytest.raises(ValueError):
        table.add_column('size', str)

def test_insert_row_no_columns():
    table = Table()
    with pytest.raises(ValueError):
        table.append(('Bob', ))

def test_insert_row():
    table = Table(valid_schema)
    table.append(bob)
    row = table.rows.pop()
    assert row['age'].value == 18
    assert row['name'].value == 'Bob'

def test_with_label():
    table = Table(valid_schema)
    table.append(bob)
    rows = table.rows
    row = rows.pop()
    assert row['name'].label is None

    harry = (17, ('Harry', 'Big Man'))
    table.append(harry)
    row = rows.pop()
    assert row['age'].value == 17
    assert row['name'].value == 'Harry'
    assert row['name'].label == 'Big Man'

def test_cell_options():
    table = Table(valid_schema)

    jack = [17, ('Jack', 'Beanstalk', dict(key='value'))]
    table.append(jack)
    row = table.rows.pop()
    assert row['name'].options == {'key':'value'}

    kate = [26, dict(value='Kate', options={'hair':'long'})]
    table.append(kate)
    row = table.rows.pop()
    assert row['name'].value == 'Kate'
    assert row['name'].label == None
    assert row['name'].options == {'hair':'long'}


def test_insert_rows():
    table = Table(valid_schema)
    table.extend([bob, (20, 'Sally')])
    rows = table.rows
    row = rows.pop()
    assert row['name'].value == 'Sally'

    row = rows.pop()
    assert row['age'].value == 18


def test_invalid_row():
    table = Table(valid_schema)
    with pytest.raises(ValueError):
        table.append([1, 2, 3])


def test_dictionary_interface():
    table = Table(options={'foo':'bar'})
    expected = dict(rows=[], cols=[], p={'foo':'bar'})
    assert dict(table) == expected


def test_encode():
    table = Table()
    expected = {"rows": [], "cols": []}
    result = table.encode()
    assert json.loads(result) == expected


def test_source():
    table = Table()
    google = DummyGoogleObject()
    google.visualization = DummyGoogleObject()
    google.visualization.Query = DummyGoogleObject()
    result = eval(table.source())
    expected = {"status": "OK", "table": {"rows": [], "cols": []}, "reqId": 0, "version": 0.6}
    assert result == expected


class DummyGoogleObject(object):
    """
    Just allows namespaces to mimic the Google API
    """

    def setResponse(self, arg):
        return arg
