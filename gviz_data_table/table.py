try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

import sys

from .cell import Cell
from .column import Column


class Table(object):
    """
    Tables are two-dimensional arrays with fixed schemas.

    Columns are ordered dictionaries of id, label and data type.

    Rows are ordered dictionaries mirroring columns.
    """

    __gviz__version = 0.6

    def __init__(self, schema=None, options=None):
        """Sample schema
        ({'id':'name', 'type':'string', 'label':'Name', 'options':{} },
         {'id':'age', 'type':'number',}
        )

        """
        self.rows = []
        self.schema = OrderedDict()
        if schema is not None:
            for col in schema:
                self.add_column(**col)
        self.options = options

    def add_column(self, id, type, label=None, options=None):
        """
        Add a new column

        Columns cannot be added to tables which already contain data.
        """
        if id in self.schema:
            raise ValueError("Duplicate column ids '{0}'".format(id))
        column = Column(id, type, label, options)
        self.schema[column.id] = column
        if len(self.rows):
            raise ValueError("Cannot add columns to tables already containing data")

    @property
    def options(self):
        return self._options

    @options.setter
    def options(self, options):
        """
        Ensure that options are a dictionary
        """
        if options is not None and not isinstance(options, dict):
            raise ValueError("Options must be a dictionary")
        self._options = options

    def _append(self, row):
        """
        Convert incoming data into table cells
        """
        cols = self.schema.values()
        cells = OrderedDict()
        for col, value in zip(cols, row):
            if isinstance(value, tuple):
                cell = Cell(*(col.type,) + value)
            elif isinstance(value, dict):
                value['typ'] = col.type
                cell = Cell(**value)
            else:
                cell = Cell(col.type, value)
            cells[col.id] = cell
        return cells

    def append(self, row):
        """
        Add a row.

        Rows are either sequences of values,
        or sequences of (value, label, options) tuples,
        or sequences of cell dictionaries.
        Dictionaries are the most flexible but also the most verbose.
        Tuples do not have to be complete but will be exhausted in order, i.e.
        you can't have just a value and options.
        """
        if len(row) != len(self.schema):
            raise ValueError("Row length does not match number of columns")
        self.rows.append(self._append(row))

    def extend(self, rows):
        """Add multiple rows of data"""
        for row in rows:
            self.append(row)

    def __iter__(self):
        """Dictionary interface for JSON encoding"""
        rows = [{"c":r.values()} for r in self.rows]
        cols = list(self.schema.values())
        js = ['cols', 'rows', 'p']
        for k, v in zip(js, [cols, rows, self.options]):
            if v is not None:
                yield k, v

    def encode(self):
        """
        Convenience method for encoding tables
        """
        from .encoder import encode
        return encode(self)

    def source(self):
        """
        Convenience method for encoding a table as a static JSON data source.
        This only wraps the table in the API.
        """
        from .encoder import encode
        d = {}
        d['status'] = "OK"
        d['reqId'] = 0
        d['version'] = self.__gviz__version
        d['table'] = self
        return  'google.visualization.Query.setResponse(%s)' % encode(d)
