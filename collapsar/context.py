from collapsar.exc import ObjectNotRegistered, CollapsarError
from collapsar.const import CONST
from collapsar.config.scheme import Rel
from collapsar.proxy import make_proxy


class ScopeAlreadyExists(CollapsarError):
    pass


class ObjectFactory(object):
    def __init__(self, descr):
        self.descr = descr

    def create_instance(self, context):
        if self.descr.lazy:
            return make_proxy(lambda s: self._create_instance(context))
        else:
            return self._create_instance(context)

    def _create_instance(self, context):
        if self.descr.factory is None:
            obj = self.descr.cls()
        else:
            if isinstance(self.descr.factory, Rel):
                factory = self._resolve_rel(context, self.descr.factory)
            else:
                factory = self.descr.factory()
            obj = factory()

        if self.descr.properties:
            for name, value in self.descr.properties.iteritems():
                if isinstance(value, Rel):
                    value = self._resolve_rel(context, value)
                setattr(obj, name, value)
        return obj

    def _resolve_rel(self, context, rel):
        obj = context.get_object(rel.name)
        if rel.attr is None:
            return obj
        else:
            return getattr(obj, rel.attr)


class PreinstantiatedFactory(object):
    def __init__(self, descr):
        self.descr = descr

    def create_instance(self, context):
        return self.descr.cls


class BaseScope(object):
    factory = ObjectFactory

    def __init__(self):
        self.factories = {}

    def set_context(self, context):
        self.context = context

    def add_descr(self, name, descr):
        factory = self.factory(descr)
        self.factories[name] = factory

    def get_object(self, name):
        return self.create_instance(name)

    def create_instance(self, name):
        factory = self.factories[name]
        return factory.create_instance(self.context)


class PrototypeScope(BaseScope):
    pass


class SingletonScope(BaseScope):
    def __init__(self):
        super(SingletonScope, self).__init__()
        self.instances = {}

    def get_object(self, name):
        if name in self.instances:
            obj = self.instances[name]
        else:
            obj = self.create_instance(name)
            self.instances[name] = obj
        return obj


class PreinstantiatedScope(BaseScope):
    factory = PreinstantiatedFactory


class ApplicationContext(object):
    DEFAULT_SCOPES = {
        CONST.SCOPE.PROTOTYPE: PrototypeScope,
        CONST.SCOPE.SINGLETON: SingletonScope,
        CONST.SCOPE.PREINSTANTIATED: PreinstantiatedScope,
    }

    def __init__(self, config, initialize=True):
        self.config = config
        self.scopes = {}

        for scope_name, scope_cls in self.DEFAULT_SCOPES.iteritems():
            self.add_scope(scope_name, scope_cls())

        if initialize:
            self.configure()

    def add_scope(self, name, scope, replace=False):
        if name in self.scopes and not replace:
            raise ScopeAlreadyExists('Scope %s already exists' % name)
        self.scopes[name] = scope
        scope.set_context(self)

    def configure(self):
        for name, descr in self.config.iteritems():
            scope = self.scopes[descr.scope]
            scope.add_descr(name, descr)

    def get_object(self, name):
        if name not in self.config:
            raise ObjectNotRegistered(name)

        descr = self.config[name]

        scope = self.scopes[descr.scope]

        return scope.get_object(name)
