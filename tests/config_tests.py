import sys

if sys.version_info < (2, 7):
    from unittest2 import TestCase
else:
    from unittest import TestCase

from collapsar.const import CONST
from collapsar.config import YAMLConfig, StringLoader, ImproperlyConfigured


EMPTY_YAML = """
objects:
"""

WITHOUT_CLASS_YAML = """
objects:
  name:
    instantiate: true
"""

CLASS_YAML = """
objects:
  name:
    class: %(module)s:TestObject
    scope: prototype
    properties:
      attr: test test
      simple_rel:
        rel: rel_test
      extra_rel:
        rel:
          name: rel_name
          attr: attr_name
  defaults:
    class: %(module)s:TestObject
""" % {
    'module': __name__
}


class TestObject(object):
    pass


class RelTestObject(object):
    pass


class YAMLConfigTest(TestCase):
    def empty_config_test(self):
        self.assertEqual({}, self.get_descriptions(EMPTY_YAML))

    def basic_config_test(self):
        description = self.get_descriptions(CLASS_YAML)['name']

        self.assertEqual(TestObject, description.cls)

        self.assertEqual('prototype', description.scope)

        self.assertEqual('test test', description.properties['attr'])

        self.assertEqual('rel_test', description.properties['simple_rel'].name)

        self.assertEqual('rel_name', description.properties['extra_rel'].name)
        self.assertEqual('attr_name', description.properties['extra_rel'].attr)

    def defatuls_test(self):
        description = self.get_descriptions(CLASS_YAML)['defaults']

        self.assertEqual({}, description.properties)
        self.assertEqual(CONST.SCOPE.SINGLETON, description.scope)

    def condif_without_class_test(self):
        with self.assertRaises(ImproperlyConfigured):
            self.get_descriptions(WITHOUT_CLASS_YAML)

    def get_descriptions(self, source):
        config = YAMLConfig(StringLoader(source))
        return config.get_descriptions()
