from importlib import import_module

from collapsar.const import CONST
from collapsar.exc import ImproperlyConfigured


class NoDefault(object):
    def __call__(self):
        return self
NoDefault = NoDefault()


class ObjectFactory(object):
    def __init__(self, instantiate=True):
        self.instantiate = instantiate

    def get_instance(self, cls):
        if self.instantiate:
            return cls()
        else:
            return cls


class Rel(object):
    def __init__(self, name, attr=None):
        self.name = name
        self.attr = attr


class Description(object):
    properties = {}
    scope = CONST.SCOPE.SINGLETON

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class FSLoader(object):
    def __init__(self, file_name):
        self.file_name = file_name

    def get_source(self):
        with open(self.file_name, 'rb') as file:
            return file.read()


class StringLoader(object):
    def __init__(self, source):
        self.source = source

    def get_source(self):
        return self.source


class ClassResolver(object):
    def resolve(self, source):
        module_name, attr_names = source.split(':', 1)
        obj = import_module(module_name)
        attr_names_list = attr_names.split('.')
        for attr_name in attr_names_list:
            obj = getattr(obj, attr_name)
        return obj


class ProxyResolver(object):
    def resolve(self, source):
        return source


class PropertiesResolver(object):
    BUILDIN_TYPES = {
        'int': int,
        'long': long,
        'string': str,
        'unicode': unicode,
        'bool': bool,
        'set': set,
        'frozenset': frozenset,
        'dict': dict,
    }

    def __init__(self):
        resolvers = {}
        resolvers.update(self.BUILDIN_TYPES)
        self.resolvers = resolvers

    def resolve(self, source):
        result = {}
        for name, value in source.iteritems():
            result[name] = self.resolve_property(value)
        return result

    def resolve_property(self, source):
        if isinstance(source, dict):
            if 'rel' in source:
                rel_source = source['rel']
                if isinstance(rel_source, dict):
                    return Rel(**rel_source)
                else:
                    return Rel(rel_source)
            else:
                type_name = source['type']
                value_sourve = source['value']
                return self.get_resolver(type_name)(value_sourve)
        else:
            return source

    def get_resolver(self, type_name):
        return self.BUILDIN_TYPES[type_name]


class ScopeResolver(object):
    SKOPES = frozenset(CONST.SCOPE.values())

    def resolve(self, source):
        if source not in self.SKOPES:
            raise ImproperlyConfigured('invalid scope %s' % source)
        return source


class YAMLConfig(object):
    RESOLVERS = {
        'class': (ClassResolver, NoDefault),
        'properties': (PropertiesResolver, Description.properties),
        'scope': (ScopeResolver, Description.scope),
    }

    NAMES_MAP = {
        'class': 'cls',
    }

    RESOLVER_INDEX = 0
    DEFAULT_INDEX = 1

    def __init__(self, loader):
        self.loader = loader
        self._source = None

    def get_descriptions(self):
        data = self.parse()
        objects = data['objects']
        if objects is None:
            return {}
        result = {}
        for name, obj_data in objects.iteritems():
            result[name] = self.create_description(name, obj_data)
        return result

    def parse(self):
        if self._source is None:
            import yaml
            source = self.loader.get_source()
            self._source = yaml.load(source)
        return self._source

    def create_description(self, name, object_data):
        descr = Description()

        for attr in self.RESOLVERS:
            value = self.resolve_attr(object_data, attr)
            self.set_descr_attr(descr, attr, value)

        assert not self.get_not_processed(object_data), \
            'Not supported options %s' % self.get_not_processed(object_data)

        return descr

    def resolve_attr(self, object_data, attr):
        if attr not in object_data:
            if self.has_default(attr):
                return self.get_default(attr)
            else:
                raise ImproperlyConfigured('No %s key' % attr)
        else:
            return self.resolve_source(attr, object_data[attr])

    def has_default(self, attr):
        return self.get_default(attr) is not NoDefault

    def get_default(self, attr):
        return self.RESOLVERS[attr][self.DEFAULT_INDEX]

    def resolve_source(self, attr, source):
        resolver_cls = self.RESOLVERS[attr][self.RESOLVER_INDEX]
        return resolver_cls().resolve(source)

    def set_descr_attr(self, descr, attr, value):
        name = self.NAMES_MAP.get(attr, attr)
        setattr(descr, name, value)

    def get_not_processed(self, object_data):
        return set(object_data) - set(self.RESOLVERS)
