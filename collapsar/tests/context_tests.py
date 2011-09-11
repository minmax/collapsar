import sys

if sys.version_info < (2, 7):
    from unittest2 import TestCase
else:
    from unittest import TestCase

from collapsar.context import ApplicationContext
from collapsar.config import Description, Rel
from collapsar.const import CONST

from collapsar.tests.objects import TestObject, RelTestObject, SimpleFactory


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


class RelTest(BaseContextTest):
    ROOT_NAME = 'root'
    CONFIG = {
        ROOT_NAME: Description(
            cls = TestObject,
            properties = {
                'simple_rel': Rel('child'),
                'attrib_rel': Rel('child', 'attr'),
            }
        ),
        'child': Description(
            cls = RelTestObject,
            properties = {'attr': 'test'},
        )
    }

    def simple_rel_test(self):
        root = self.get_root()

        self.assertTrue(isinstance(root.simple_rel, RelTestObject))

    def rel_attribute_test(self):
        root = self.get_root()

        self.assertEqual('test', root.attrib_rel)

    def get_root(self):
        return self.get_object(self.ROOT_NAME)


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


class FactoryTest(BaseContextTest):
    CONFIG = {
        'plain': Description(factory=SimpleFactory),
        'simple_rel': Description(factory=Rel('factory')),
        'rel_with_attr': Description(factory=Rel('factory', 'get_instance')),

        'factory': Description(cls=SimpleFactory),
    }

    def plain_factory_class_test(self):
        self.check_object('plain', '__call__')

    def simple_rel_test(self):
        self.check_object('simple_rel', '__call__')

    def rel_with_attr_test(self):
        self.check_object('rel_with_attr', 'get_instance')

    def check_object(self, name, flag):
        obj = self.get_object(name)
        self.assertTrue(isinstance(obj, TestObject))
        self.assertEqual(flag, obj.flag)
