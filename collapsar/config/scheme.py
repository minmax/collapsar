from collapsar.const import CONST


class Rel(object):
    def __init__(self, name, attr=None):
        self.name = name
        self.attr = attr


class InitArgs(object):
    def __init__(self, args=None, kwargs=None):
        if args is None:
            args = []
        self.args = args
        if kwargs is None:
            kwargs = {}
        self.kwargs = kwargs


class Description(object):
    properties = {}
    scope = CONST.SCOPE.SINGLETON
    factory = None
    lazy = False
    init = InitArgs()

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
