from collapsar.exc import ObjectNotRegistered
from collapsar.const import CONST
from collapsar.config.scheme import Rel
from collapsar.proxy import make_proxy


class ApplicationContext(object):
    def __init__(self, config):
        self.config = config
        self._singletons = {}

    def get_object(self, name):
        if name not in self.config:
            raise ObjectNotRegistered(name)

        descr = self.config[name]

        if descr.lazy:
            return make_proxy(lambda s: self._get_instance(name, descr))
        else:
            return self._get_instance(name, descr)

    def _get_instance(self, name, descr):
        if descr.scope == CONST.SCOPE.SINGLETON:
            if name in self._singletons:
                obj = self._singletons[name]
            else:
                obj = self._create_instance(descr)
                self._singletons[name] = obj
        elif descr.scope == CONST.SCOPE.PROTOTYPE:
            obj = self._create_instance(descr)
        elif descr.scope == CONST.SCOPE.PREINSTANTIATED:
            obj = descr.cls
        else:
            raise NotImplementedError
        return obj

    def _create_instance(self, descr):
        if descr.factory is None:
            obj = descr.cls()
        else:
            if isinstance(descr.factory, Rel):
                factory = self._resolve_rel(descr.factory)
            else:
                factory = descr.factory()
            obj = factory()

        if descr.properties:
            for name, value in descr.properties.iteritems():
                if isinstance(value, Rel):
                    value = self._resolve_rel(value)
                setattr(obj, name, value)
        return obj

    def _resolve_rel(self, rel):
        obj = self.get_object(rel.name)
        if rel.attr is None:
            return obj
        else:
            return getattr(obj, rel.attr)
