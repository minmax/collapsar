from collapsar.exc import ObjectNotRegistered
from collapsar.const import CONST


class ApplicationContext(object):
    def __init__(self, config):
        self.config = config
        self._singletons = {}

    def get_object(self, name):
        if name not in self.config:
            raise ObjectNotRegistered(name)

        descr = self.config[name]

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
        obj = descr.cls()
        if descr.properties:
            for name, value in descr.properties.iteritems():
                setattr(obj, name, value)
        return obj
