import six


class ValidationError(Exception):
    pass


def get_deserializer(datatype):
    if hasattr(datatype, 'deserialize'):
        return datatype.deserialize

    def deserialize(raw_data):
        try:
            return datatype(raw_data)
        except (ValueError, TypeError):
            raise ValidationError('should be convertible to {}, got {} instead'
                                  .format(datatype, type(raw_data)))
    return deserialize


class Field(object):

    def __init__(self, datatype, required=False, default=None):
        self.deserialize = get_deserializer(datatype)
        self.required = required
        self.default = default


def String(value, encoding='utf-8', errors='ignore'):
    if isinstance(value, six.text_type):
        return value
    if isinstance(value, six.binary_type):
        return value.decode(encoding=encoding, errors=errors)
    return six.text_type(value)


def serialize(value):
    if hasattr(value, 'serialize'):
        return value.serialize()
    if isinstance(value, list):
        return list(six.moves.map(serialize, value))
    return value


class ObjectMeta(type):

    def __init__(cls, name, bases, attrs):
        super(ObjectMeta, cls).__init__(name, bases, attrs)
        named_fields = [item for item in six.iteritems(attrs)
                        if isinstance(item[1], Field)]
        cls._deserializers = {name: field.deserialize for name, field in named_fields}
        cls._defaults = {name: field.default for name, field in named_fields}
        cls._required = {name for name, field in named_fields if field.required}


@six.add_metaclass(ObjectMeta)
class Object(object):

    def __init__(self, **kwargs):
        if not self._required.issubset(kwargs):
            missing = next(name for name in self._required if name not in kwargs)
            raise ValidationError('{}.{} is required'
                                  .format(self.__class__.__name__,  missing))
        self.__dict__.update(self._defaults, **kwargs)

    def __getattr__(self, k):
        return None

    @classmethod
    def deserialize(cls, raw_data):
        data = {}
        get_deserializer = cls._deserializers.get
        for k, v in six.iteritems(raw_data):
            if v is not None:
                deserialize = get_deserializer(k)
                data[k] = deserialize(v) if deserialize is not None else v
        return cls(**data)

    def serialize(self):
        return {k: serialize(v)
                for k, v in six.iteritems(self.__dict__)
                if v is not None}


class Array(object):

    def __init__(self, datatype):
        self._deserialize_element = get_deserializer(datatype)

    def deserialize(self, raw_data):
        return list(six.moves.map(self._deserialize_element, (raw_data or ())))

    # for backwards compatibility
    __call__ = deserialize


class EnumMeta(type):
    def __new__(mcs, name, bases, params):
        params['values'] = {}
        new_class = super(EnumMeta, mcs).__new__(mcs, name, bases, params)

        for k, v in six.iteritems(params):
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
