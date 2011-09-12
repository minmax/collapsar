import sys

if sys.version_info < (2, 7):
    from unittest2 import TestCase
else:
    from unittest import TestCase

from collapsar.const import CONST
from collapsar.exc import ImproperlyConfigured
from collapsar.config.yaml_config import YAMLConfig
from collapsar.config.loaders import StringLoader
from collapsar.config.scheme import Rel

from collapsar.tests.objects import TestObject, SimpleFactory


class BaseYAMLConfigTest(TestCase):
    YAML = ""

    def setUp(self):
        self.config = self.get_config()

    def get_config(self):
        return YAMLConfig(StringLoader(self.YAML))

    def get_description(self, name):
        return self.config.get_descriptions()[name]


class EmptyConfigTest(BaseYAMLConfigTest):
    YAML = """
    objects:
    """

    def runTest(self):
        self.assertEqual({}, self.config.get_descriptions())


class BaseDescriptionTest(BaseYAMLConfigTest):
    YAML = """
    objects:
      name:
        class: collapsar.tests.objects:TestObject
        scope: prototype
        lazy: true
    """

    def runTest(self):
        description = self.get_description('name')

        self.assertEqual(TestObject, description.cls)

        self.assertEqual('prototype', description.scope)

        self.assertEqual(True, description.lazy)


class PropertiesTest(BaseYAMLConfigTest):
    YAML = """
    objects:
      name:
        class: collapsar.tests.objects:TestObject
        properties:
          plain: test test
          typed:
            type: bool
            value: "123"
          simple_rel:
            rel: rel_test
          extra_rel:
            rel:
              name: rel_name
              attr: attr_name
    """

    def runTest(self):
        description = self.get_description('name')

        self.assertEqual('test test', description.properties['plain'])

        self.assertEqual(True, description.properties['typed'])

        self.assertEqual('rel_test', description.properties['simple_rel'].name)

        self.assertEqual('rel_name', description.properties['extra_rel'].name)
        self.assertEqual('attr_name', description.properties['extra_rel'].attr)


class DefaultsTest(BaseYAMLConfigTest):
    YAML = """
    objects:
      defaults:
        class: collapsar.tests.objects:TestObject
    """

    def runTest(self):
        description = self.get_description('defaults')

        self.assertEqual({}, description.properties)
        self.assertEqual(CONST.SCOPE.SINGLETON, description.scope)


class FactoryTest(BaseYAMLConfigTest):
    YAML = """
    objects:
      plain_cls:
        factory: collapsar.tests.objects:SimpleFactory

      with_rel:
        factory:
          rel:
            name: simple_factory
            attr: get_instance
    """

    def plain_cls_test(self):
        descr = self.get_description('plain_cls')
        self.assertEqual(SimpleFactory, descr.factory)

    def with_rel_test(self):
        descr = self.get_description('with_rel')
        self.assertEqual('simple_factory', descr.factory.name)
        self.assertEqual('get_instance', descr.factory.attr)


class InitArgsTest(BaseYAMLConfigTest):
    YAML = """
    objects:
      named:
        class: collapsar.tests.objects:TestObject
        init:
          first: "test"
          second: "test test"
      args:
        class: collapsar.tests.objects:TestObject
        init:
          args*:
           - 1
           - 2
      with_rel:
        class: collapsar.tests.objects:TestObject
        init:
          arg:
            rel: rel_name
    """

    def named_test(self):
        descr = self.get_description('named')

        self.assertEqual('test', descr.init.kwargs['first'])
        self.assertEqual('test test', descr.init.kwargs['second'])

    def args_test(self):
        descr = self.get_description('args')
        self.assertEqual([1, 2], descr.init.args)

    def with_rel_test(self):
        descr = self.get_description('with_rel')
        rel = descr.init.kwargs['arg']
        self.assertTrue(isinstance(rel, Rel))
        self.assertEqual('rel_name', rel.name)


class ErrorWithoutClassTest(TestCase):
    YAML = """
    objects:
      name:
        instantiate: true
    """

    def runTest(self):
        with self.assertRaises(ImproperlyConfigured):
            config = YAMLConfig(StringLoader(self.YAML))
            config.get_descriptions()
