class CollapsarError(Exception):
    pass


class ImproperlyConfigured(CollapsarError):
    pass


class MustBeOnlyOneOption(ImproperlyConfigured):
    pass


class NotResolved(ImproperlyConfigured):
    pass


class ObjectNotRegistered(CollapsarError):
    pass
