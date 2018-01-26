
class MemoryManager(object):
    def __init__(self, start):
        self.pointer = start

    def get_variable(self):
        start = self.pointer
        self.pointer += 4
        return start