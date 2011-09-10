import sys

if sys.version_info < (2, 7):
    from unittest2 import TestCase
else:
    from unittest import TestCase

from collapsar.context import ApplicationContext
from collapsar.config import Description
from collapsar.const import CONST

from collapsar.tests.objects import TestObject, RelTestObject


class ContextTest(TestCase):
    SIMPLE_OBJ_CONF = {
        'obj': Description(cls=TestObject, scope=CONST.SCOPE.SINGLETON),
    }

    def simple_id_test(self):
        obj = self.get_object(self.SIMPLE_OBJ_CONF, 'obj')

        self.assertTrue(isinstance(obj, TestObject))

    def get_object(self, config, name):
        context = ApplicationContext(config)
        return context.get_object(name)


class ScopeTest(TestCase):
    PREINSTANTIATED = TestObject()

    CONFIG = {
        'singleton': Description(cls=TestObject, scope=CONST.SCOPE.SINGLETON),
        'prototype': Description(cls=TestObject, scope=CONST.SCOPE.PROTOTYPE),
        'preinstantiated': Description(
            cls = PREINSTANTIATED,
            scope = CONST.SCOPE.PREINSTANTIATED
        ),
    }

    def setUp(self):
        self.context = ApplicationContext(self.CONFIG)

    def singleton_test(self):
        first, second = self.get_two_objects('singleton')

        self.assertEqual(id(first), id(second), 'Object are not singleton')

    def prototype_test(self):
        first, second = self.get_two_objects('prototype')

        self.assertNotEqual(id(first), id(second), 'Object are not singleton')

    def preinstantiated_test(self):
        obj = self.context.get_object('preinstantiated')

        self.assertEqual(id(self.PREINSTANTIATED), id(obj))

    def get_two_objects(self, name):
        return (
            self.context.get_object(name),
            self.context.get_object(name)
        )
