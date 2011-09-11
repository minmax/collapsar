class CollapsarError(Exception):
    pass


class ImproperlyConfigured(CollapsarError):
    pass


class NotResolved(ImproperlyConfigured):
    pass


class ObjectNotRegistered(CollapsarError):
    pass
