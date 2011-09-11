from collapsar.exc import ObjectNotRegistered, CollapsarError
from collapsar.const import CONST
from collapsar.scopes import *


class ScopeAlreadyExists(CollapsarError):
    pass


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
