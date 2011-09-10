from collapsar.exc import CollapsarError
from collapsar.const import CONST


class ApplicationContext(object):
    def __init__(self, config):
        self.config = config
        self._singletons = {}

    def get_object(self, name):
        if name not in self.config:
            raise CollapsarError

        descr = self.config[name]

        if descr.scope == CONST.SCOPE.SINGLETON:
            if name in self._singletons:
                obj = self._singletons[name]
            else:
                obj = descr.cls()
                self._singletons[name] = obj
        else:
            obj = descr.cls()

        return obj
