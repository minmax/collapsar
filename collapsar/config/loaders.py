class FSLoader(object):
    MODE = 'rb'

    def __init__(self, file_name):
        self.file_name = file_name

    def get_source(self):
        with open(self.file_name, self.MODE) as file_obj:
            return file_obj.read()


class StringLoader(object):
    def __init__(self, source):
        self.source = source

    def get_source(self):
        return self.source
