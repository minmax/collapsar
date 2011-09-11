from collapsar.const import CONST


class Rel(object):
    def __init__(self, name, attr=None):
        self.name = name
        self.attr = attr


class Description(object):
    properties = {}
    scope = CONST.SCOPE.SINGLETON
    factory = None
    lazy = False

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
