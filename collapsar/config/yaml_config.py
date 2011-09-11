import yaml

from collapsar.exc import NotResolved
from collapsar.config.scheme import Description
from collapsar.config.resolvers import *


class NoDefault(object):
    replacement = None

    def __init__(self, replacement=None):
        self.replacement = replacement


class YAMLConfig(object):
    RESOLVERS = {
        'class': (ClassResolver, NoDefault('factory')),
        'factory': (FactoryResolver, NoDefault('class')),
        'properties': (PropertiesResolver, Description.properties),
        'scope': (ScopeResolver, Description.scope),
    }

    NAMES_MAP = {
        'class': 'cls',
    }

    RESOLVER_INDEX = 0
    DEFAULT_INDEX = 1

    OBJECTS_KEY = 'objects'

    def __init__(self, loader):
        self.loader = loader
        self._source = None

    def get_descriptions(self):
        data = self.parse()
        objects = data[self.OBJECTS_KEY]
        if objects is None:
            return {}
        result = {}
        for name, obj_data in objects.iteritems():
            result[name] = self.create_description(name, obj_data)
        return result

    def parse(self):
        if self._source is None:
            source = self.loader.get_source()
            self._source = yaml.load(source)
        return self._source

    def create_description(self, name, object_data):
        descr = Description()

        for attr in self.RESOLVERS:
            try:
                value = self.resolve_attr(object_data, attr)
            except NotResolved:
                if not self.has_replacement(object_data, attr):
                    raise
            else:
                self.set_descr_attr(descr, attr, value)

        assert not self.get_not_processed(object_data), \
            'Not supported options %s' % self.get_not_processed(object_data)

        return descr

    def resolve_attr(self, object_data, attr):
        if attr not in object_data:
            if self.has_default(attr):
                return self.get_default(attr)
            else:
                raise NotResolved('No %s key' % attr)
        else:
            return self.resolve_source(attr, object_data[attr])

    def has_replacement(self, object_data, attr):
        default = self.get_default(attr)
        if not isinstance(default, NoDefault):
            return False
        if default.replacement is None:
            return False
        if default.replacement in object_data:
            return True
        else:
            return self.has_default(default.replacement)

    def has_default(self, attr):
        default = self.get_default(attr)
        return not (default is NoDefault or isinstance(default, NoDefault))

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
