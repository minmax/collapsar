import sys

if sys.version_info < (2, 7):
    from unittest2 import TestCase
else:
    from unittest import TestCase

from collapsar.const import CONST
from collapsar.config import YAMLConfig, StringLoader, ImproperlyConfigured

from collapsar.tests.objects import TestObject


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
        properties:
          attr: test test
          simple_rel:
            rel: rel_test
          extra_rel:
            rel:
              name: rel_name
              attr: attr_name
    """

    def runTest(self):
        description = self.get_description('name')

        self.assertEqual(TestObject, description.cls)

        self.assertEqual('prototype', description.scope)

        self.assertEqual('test test', description.properties['attr'])

        self.assertEqual('rel_test', description.properties['simple_rel'].name)

        self.assertEqual('rel_name', description.properties['extra_rel'].name)
        self.assertEqual('attr_name', description.properties['extra_rel'].attr)


class DefaultsTest(BaseYAMLConfigTest):
    YAML = """
    objects:
      defaults:
        class: collapsar.tests.objects:TestObject
    """

    def defatuls_test(self):
        description = self.get_description('defaults')

        self.assertEqual({}, description.properties)
        self.assertEqual(CONST.SCOPE.SINGLETON, description.scope)


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
