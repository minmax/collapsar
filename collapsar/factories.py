from collapsar.proxy import make_proxy
from collapsar.config.scheme import Rel


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
