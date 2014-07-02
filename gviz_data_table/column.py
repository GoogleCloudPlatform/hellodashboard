import datetime

try:
    a = basestring
except NameError:
    basestring = str
    unicode = str

valid_types = {str:'string', unicode:'string', int:'number', float:'number',
               bool:'boolean', datetime.date:'date', datetime.datetime:'datetime',
               datetime.time:'timeofday'}


class Column(object):
    """A column is a type definition"""

    __slots__ = ('_id', '_type', '_label', '_options')

    def __init__(self, id, type, label=None, options=None):
        self.id = id
        self.type = type
        self.label = label
        self.options = options

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        if not value in valid_types:
            raise ValueError("{0} Type not supported".format(value))
        self._type = value

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not isinstance(value, basestring):
            raise ValueError("Column ids must be strings")
        self._id = value

    @property
    def label(self):
        return self._label or self.id

    @label.setter
    def label(self, value):
        if value is not None and not isinstance(value, basestring):
            raise ValueError("Labels must be strings")
        self._label = value

    @property
    def options(self):
        return self._options

    @options.setter
    def options(self, value):
        if value is not None and not isinstance(value, dict):
            raise ValueError("Options must be a dictionary")
        self._options = value

    def __iter__(self):
        for key in ['id', 'type', 'label', 'options']:
            value = getattr(self, key, None)
            if value:
                if key == 'type':
                    value = valid_types[value]
                yield key, value
