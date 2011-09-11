class TestObject(object):
    def __init__(self, flag=None):
        self.flag = flag


class RelTestObject(object):
    pass


class SimpleFactory(object):
    def __call__(self):
        return TestObject('__call__')

    def get_instance(self):
        return TestObject('get_instance')
