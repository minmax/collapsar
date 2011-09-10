class CollapsarError(Exception):
    pass


class ImproperlyConfigured(CollapsarError):
    pass


class ObjectNotRegistered(CollapsarError):
    pass
