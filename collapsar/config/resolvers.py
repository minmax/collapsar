from importlib import import_module

from collapsar.const import CONST
from collapsar.exc import ImproperlyConfigured
from collapsar.config.scheme import Rel


__all__ = [
    'ClassResolver',
    'PropertiesResolver',
    'ScopeResolver',
    'FactoryResolver',
    'BooleanResolver',
]


class BaseResolver(object):
    def resolve_import(self, source):
        module_name, attr_names = source.split(':', 1)
        obj = import_module(module_name)
        attr_names_list = attr_names.split('.')
        for attr_name in attr_names_list:
            obj = getattr(obj, attr_name)
        return obj

    def resolve_rel(self, source):
        rel_source = source['rel']
        if isinstance(rel_source, dict):
            return Rel(**rel_source)
        else:
            return Rel(rel_source)

    def is_rel_source(self, source):
        return isinstance(source, dict) and 'rel' in source


class ClassResolver(BaseResolver):
    def resolve(self, source):
        return self.resolve_import(source)


class PropertiesResolver(BaseResolver):
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
            if self.is_rel_source(source):
                return self.resolve_rel(source)
            else:
                return self.resolve_plain_obj(source)
        else:
            return source

    def resolve_plain_obj(self, source):
        type_name = source['type']
        value_sourve = source['value']
        return self.get_resolver(type_name)(value_sourve)

    def get_resolver(self, type_name):
        return self.BUILDIN_TYPES[type_name]


class ScopeResolver(BaseResolver):
    SKOPES = frozenset(CONST.SCOPE.values())

    def resolve(self, source):
        if source not in self.SKOPES:
            raise ImproperlyConfigured('invalid scope %s' % source)
        return source


class FactoryResolver(BaseResolver):
    def resolve(self, source):
        if self.is_rel_source(source):
            return self.resolve_rel(source)
        else:
            return self.resolve_import(source)


class BooleanResolver(BaseResolver):
    def resolve(self, source):
        if not isinstance(source, bool):
            raise ImproperlyConfigured('Must be boolean, not %r' % source)
        return source
