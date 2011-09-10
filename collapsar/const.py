from itertools import ifilter


__all__ = [
    'CONST',
]


class Struct(object):
    @classmethod
    def values(cls):
        return [getattr(cls, name) for name in cls._get_public_attrs()]

    @classmethod
    def _get_public_attrs(cls):
        return ifilter(cls._is_public_attr, dir(cls))

    @classmethod
    def _is_public_attr(cls, attr_name):
        return attr_name != 'values' and not attr_name.startswith('_')


class CONST(Struct):
    class SCOPE(Struct):
        PROTOTYPE = 'prototype'
        SINGLETON = 'singleton'
        PREINSTANTIATED = 'preinstantiated'
