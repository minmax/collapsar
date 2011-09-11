class TestObject(object):
    pass


class RelTestObject(object):
    pass


class SimpleFactory(object):
    def __call__(self):
        return TestObject()
