def make_proxy(factory):
    class ProxyMeta(BaseProxyMeta):
        GET_INSTANCE = factory

    class Proxy(BaseProxy):
        __metaclass__ = ProxyMeta
        GET_INSTANCE = factory

    return Proxy()


class BaseProxyMeta(type):
    GET_INSTANCE = None

    def __instancecheck__(cls, instance):
        get_instance = type.__getattribute__('GET_INSTANCE')
        instance = get_instance()
        return isinstance(instance, type(instance))

    def __subclasscheck__(cls, subclass):
        get_instance = type.__getattribute__('GET_INSTANCE')
        instance = get_instance()
        return issubclass(subclass, type(instance))

    def __getattribute__(cls, name):
        get_instance = type.__getattribute__('GET_INSTANCE')
        instance = get_instance()
        return getattr(instance.__class__.__class__, name)


class BaseProxy(object):
    GET_INSTANCE = None

    def __getattribute__(self, name):
        get_instance = object.__getattribute__(self, 'GET_INSTANCE')
        instance = get_instance()
        return getattr(instance, name)

    def __setattr__(self, name, value):
        get_instance = object.__getattribute__(self, 'GET_INSTANCE')
        instance = get_instance()
        setattr(instance, name, value)

    def __delattr__(self, name):
        get_instance = object.__getattribute__(self, 'GET_INSTANCE')
        instance = get_instance()
        delattr(instance, name)
