from collapsar.factories import ObjectFactory, PreinstantiatedFactory


__all__ = [
    'PrototypeScope',
    'SingletonScope',
    'PreinstantiatedScope',
]


class BaseScope(object):
    factory = ObjectFactory

    def __init__(self):
        self.factories = {}
        self.context = None

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
