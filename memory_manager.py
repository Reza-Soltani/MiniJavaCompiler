
class MemoryManager(object):
    def __init__(self, main_start, temp_start):
        self.pointer = main_start
        self.temp = temp_start
        self.temp_init = temp_start

    def get_variable(self):
        start = self.pointer
        self.pointer += 4
        if self.pointer >= self.temp_init:
            raise Exception('memory overflow!')
        return start

    def get_temp(self):
        ret = self.temp
        self.temp += 4
        return ret
