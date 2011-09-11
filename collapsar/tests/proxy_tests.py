import sys

if sys.version_info < (2, 7):
    from unittest2 import TestCase
else:
    from unittest import TestCase


from collapsar.proxy import make_proxy


class ProxyTest(TestCase):
    class C(object):
        x = 10

    def runTest(self):
        original = self.C()
        proxy = make_proxy(lambda *a: original)

        self.assertEqual(10, proxy.x)

        proxy.y = 15

        self.assertEqual(15, original.y)

        self.assertTrue(isinstance(proxy, self.C))
