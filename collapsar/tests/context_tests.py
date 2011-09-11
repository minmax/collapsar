import sys

if sys.version_info < (2, 7):
    from unittest2 import TestCase
else:
    from unittest import TestCase

from collapsar.context import ApplicationContext
from collapsar.config import Description, Rel
from collapsar.const import CONST

from collapsar.tests.objects import TestObject, RelTestObject


class BaseContextTest(TestCase):
    CONFIG = None

    def setUp(self):
        assert self.CONFIG
        self.context = ApplicationContext(self.CONFIG)

    def get_object(self, name):
        return self.context.get_object(name)


class PropertiesTest(BaseContextTest):
    OBJECT_NAME = 'obj'
    ATTR_VALUE = 123

    CONFIG = {
        OBJECT_NAME: Description(
            cls = TestObject,
            scope = CONST.SCOPE.SINGLETON,
            properties = {
                'attr': ATTR_VALUE,
            }
        )
    }

    def runTest(self):
        obj = self.get_instance()
        self.assertEqual(self.ATTR_VALUE, obj.attr)

    def get_instance(self):
        return self.get_object(self.OBJECT_NAME)


class ScopeTest(BaseContextTest):
    PREINSTANTIATED = TestObject()

    CONFIG = {
        'singleton': Description(cls=TestObject, scope=CONST.SCOPE.SINGLETON),
        'prototype': Description(cls=TestObject, scope=CONST.SCOPE.PROTOTYPE),
        'preinstantiated': Description(
            cls = PREINSTANTIATED,
            scope = CONST.SCOPE.PREINSTANTIATED
        ),
    }

    def singleton_test(self):
        first, second = self.get_two_objects('singleton')

        self.assertEqual(id(first), id(second), 'Object are not singleton')

    def prototype_test(self):
        first, second = self.get_two_objects('prototype')

        self.assertNotEqual(id(first), id(second), 'Object are not singleton')

    def preinstantiated_test(self):
        obj = self.get_object('preinstantiated')

        self.assertEqual(id(self.PREINSTANTIATED), id(obj))

    def get_two_objects(self, name):
        return (
            self.get_object(name),
            self.get_object(name)
        )
