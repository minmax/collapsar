import yaml

from collapsar.exc import NotResolved, MustBeOnlyOneOption
from collapsar.config.scheme import Description
from collapsar.config.resolvers import *


class NoDefault(object):
    pass


class Options(object):
    replacement = None

    def __init__(self, default=NoDefault, replacement=None, only_me=False):
        self.default = default
        self.replacement = replacement
        self.only_me = only_me

    def has_default(self):
        return self.default is not NoDefault


class YAMLConfig(object):
    RESOLVERS = {
        'class': (ClassResolver, Options(replacement='factory')),
        'factory': (
            FactoryResolver,
            Options(replacement='class', only_me=True)
        ),
        'properties': (PropertiesResolver, Options(Description.properties)),
        'scope': (ScopeResolver, Options(Description.scope)),
        'lazy': (BooleanResolver, Options(Description.lazy)),
        'init': (InitArgsResolver, Options(Description.init)),
    }

    NAMES_MAP = {
        'class': 'cls',
    }

    RESOLVER_INDEX = 0
    OPTIONS_INDEX = 1

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
        options = self.get_options(attr)
        if attr in object_data:
            if options.only_me:
                self.check_only_me_option(object_data, attr)

            return self.resolve_source(attr, object_data[attr])
        else:
            if options.has_default():
                return options.default
            else:
                raise NotResolved('No %s key' % attr)

    def check_only_me_option(self, object_data, attr):
        if self.get_not_processed(object_data, attr):
            raise MustBeOnlyOneOption(attr)

    def has_replacement(self, object_data, attr):
        options = self.get_options(attr)
        if options.replacement is None:
            return False
        if options.replacement in object_data:
            return True
        else:
            return self.has_default(options.replacement)

    def has_default(self, attr):
        return self.get_options(attr).has_default()

    def get_options(self, attr):
        return self.RESOLVERS[attr][self.OPTIONS_INDEX]

    def resolve_source(self, attr, source):
        resolver_cls = self.RESOLVERS[attr][self.RESOLVER_INDEX]
        return resolver_cls().resolve(source)

    def set_descr_attr(self, descr, attr, value):
        name = self.NAMES_MAP.get(attr, attr)
        setattr(descr, name, value)

    def get_not_processed(self, object_data, *keys):
        if not keys:
            keys = self.RESOLVERS
        return set(object_data) - set(keys)
