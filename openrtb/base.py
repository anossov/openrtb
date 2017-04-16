import six
import codecs
import sys

print(sys.version)


class InvalidConstant(Exception):
    pass


class ValidationError(Exception):
    pass


identity = lambda x: x


class Field(object):
    def __init__(self, datatype, required=False, default=None):
        self.datatype = datatype
        self.required = required
        self.default = default if not callable(default) else default()
        self.name = None
        self.object = None

        if hasattr(self.datatype, 'deserialize'):
            self.deserialize = self.datatype.deserialize

    def deserialize(self, raw_data):
        try:
            v = self.datatype(raw_data)
        except (ValueError, TypeError):
            raise ValidationError('{}.{} should be convertible to {}, got {}'.format(
                self.object,
                self.name,
                self.datatype,
                type(raw_data)
            ))

        return v

if six.PY2:
    def String(value):
        if isinstance(value, six.text_type):
            return value
        elif isinstance(value, six.binary_type):
            return value.decode('utf-8', errors='ignore')
        else:
            value = str(value)

        return six.u(value)

elif six.PY3:
    def String(value):
        if not isinstance(value, str):
            value = str(value)

        try:
            return codecs.decode(six.b(value), 'utf-8', errors="ignore")
        except UnicodeEncodeError:
            return value

else:
    assert False, "Your python version is not supported, sorry"


class ObjectMeta(type):
    def __new__(mcs, name, bases, attrs):
        module = attrs.pop('__module__')
        new_class = super(ObjectMeta, mcs).__new__(mcs, name, bases, {'__module__': module})
        new_class._fields = {}
        new_class._required = []
        new_class._deserializers = {}
        for k, v in list(attrs.items()):
            if isinstance(v, Field):
                v.name = k
                v.object = new_class
                new_class._fields[k] = v
                if hasattr(v.datatype, 'deserialize'):
                    new_class._deserializers[k] = v.datatype.deserialize
                else:
                    new_class._deserializers[k] = v.deserialize
                if v.required:
                    new_class._required.append(v.name)
                setattr(new_class, k, v.default)
            else:
                setattr(new_class, k, v)

        return new_class


@six.add_metaclass(ObjectMeta)
class Object(object):
    _fields = {}

    def __init__(self, **kwargs):
        for fname in self._required:
            if fname not in kwargs:
                raise ValidationError('{}.{} is required'.format(self.__class__.__name__, fname))

        for k, v in kwargs.items():
            setattr(self, k, v)

    def __getattr__(self, k):
        return None

    @classmethod
    def deserialize(cls, raw_data):
        data = {}
        deserializers = cls._deserializers
        for k, v in raw_data.items():
            if v is not None:
                data[k] = deserializers.get(k, identity)(v)
        return cls(**data)

    def serialize_value(self, value):
        if hasattr(value, 'serialize'):
            return value.serialize()
        elif isinstance(value, list):
            return [self.serialize_value(v) for v in value]
        else:
            return value

    def serialize(self):
        return {k: self.serialize_value(v) for k, v in self.__dict__.items() if v is not None}


class Array(object):
    def __init__(self, datatype):
        self.datatype = datatype

        if hasattr(self.datatype, 'deserialize'):
            self._deserialize = self.datatype.deserialize
        else:
            self._deserialize = self.datatype

    def __call__(self, data):
        if data is None:
            return []
        return [self._deserialize(datum) for datum in data]

    def __str__(self):
        return 'Array of {}'.format(self.datatype)


class EnumMeta(type):
    def __new__(mcs, name, bases, params):
        params['values'] = {}
        new_class = super(EnumMeta, mcs).__new__(mcs, name, bases, params)

        for k, v in list(params.items()):
            if isinstance(v, int):
                new_class.values[v] = k
                setattr(new_class, k, new_class(v))

        return new_class


@six.add_metaclass(EnumMeta)
class Enum(object):
    values = {}

    def __init__(self, value=None):
        if isinstance(value, self.__class__):
            value = value.value

        self.value = int(value)
        self.name = self.values.get(self.value, None)

    def __int__(self):
        return self.value

    def __str__(self):
        if self.name is None:
            return '<Unknown value: {}>'.format(self.value)
        return self.name

    def __eq__(self, other):
        if other is None:
            return False
        if isinstance(other, self.__class__):
            return self.value == other.value
        if isinstance(other, int):
            return self.value == other

        raise TypeError('Comparing {} to {}'.format(self.__class__, type(other)))

    def __hash__(self):
        return hash(self.value)

    def serialize(self):
        return self.value
