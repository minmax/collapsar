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
                obj = descr.cls()
                self._singletons[name] = obj
        elif descr.scope == CONST.SCOPE.PROTOTYPE:
            obj = descr.cls()
        elif descr.scope == CONST.SCOPE.PREINSTANTIATED:
            obj = descr.cls
        else:
            raise NotImplementedError

        return obj
