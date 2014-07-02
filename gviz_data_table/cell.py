

class Cell(object):
    """
    Cells have values which must conform to their types. They can also have labels

    Cell attributes (python:javascript) mapping

    {'value':'v, 'label':'f', 'options':'p'}
    """

    __slots__ = ['type', '_value', 'label', '_options']

    def __init__(self, typ, value, label=None, options=None):
        self.type = typ
        self.label = label
        self.value = value
        self.options = options

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self.validate(value)
        self._value = value

    def validate(self, value):
        """
        Check that a value conforms to the column type. Or is None.
        """
        if value is None:
            return
        if not isinstance(value, self.type):
            raise ValueError(
                "{0} expected, {1} received".format(self.type, type(value))
            )

    @property
    def options(self):
        return self._options

    @options.setter
    def options(self, value):
        if value is not None and not isinstance(value, dict):
            raise ValueError("Options must be a dictionary")
        self._options = value

    def __iter__(self):
        """Dictionary interface for JSON encoding"""
        python = ['value', 'label', 'options']
        js = ['v', 'f', 'p']
        for key, attr in zip(js, python):
            value = getattr(self, attr)
            if value:
                yield key, value
