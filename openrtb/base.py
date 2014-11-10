class InvalidConstant(Exception):
    pass


class ValidationError(Exception):
    pass


identity = lambda x: x


class Field(object):
    def __init__(self, datatype, required=False, default=None):
        self.datatype = datatype
        self.required = required
        self.default = default
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


def String(value):
    if isinstance(value, unicode):
        return value
    if isinstance(value, str):
        return value.decode('utf-8', errors='ignore')

    return unicode(value)


class ObjectMeta(type):
    def __new__(mcs, name, bases, attrs):
        module = attrs.pop('__module__')
        new_class = super(ObjectMeta, mcs).__new__(mcs, name, bases, {'__module__': module})
        new_class._fields = {}
        new_class._required = []
        new_class._deserializers = {}
        for k, v in attrs.items():
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


class Object(object):
    __metaclass__ = ObjectMeta
    _fields = {}

    def __init__(self, **kwargs):
        for fname in self._required:
            if fname not in kwargs:
                raise ValidationError('{}.{} is required'.format(self.__class__.__name__, fname))

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def __getattr__(self, k):
        return None

    @classmethod
    def deserialize(cls, raw_data):
        data = {}
        deserializers = cls._deserializers
        for k, v in raw_data.iteritems():
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
        return {k: self.serialize_value(v) for k, v in self.__dict__.iteritems() if v is not None}


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

        for k, v in params.items():
            if isinstance(v, int):
                new_class.values[v] = k
                setattr(new_class, k, new_class(v))

        return new_class


class Enum(object):
    __metaclass__ = EnumMeta

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
