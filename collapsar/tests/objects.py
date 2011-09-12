class TestObject(object):
    flag = None

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


class RelTestObject(object):
    pass


class SimpleFactory(object):
    def __call__(self):
        return self._get_object('__call__')

    def get_instance(self):
        return self._get_object('get_instance')

    def _get_object(self, flag):
        obj = TestObject()
        obj.flag = flag
        return obj
