
class MemoryManager(object):
    def __init__(self, main_start, temp_start):
        self.pointer = main_start
        self.temp = temp_start
        self.temp_init = temp_start
        self.saved_pc_address = temp_start + 1000
        self.type_dict = dict()

    def get_variable(self, tp):
        start = self.pointer
        self.type_dict[start] = tp
        self.pointer += 4
        if self.pointer >= self.temp_init:
            raise Exception('memory overflow!')
        return start

    def get_temp(self, tp):
        ret = self.temp
        self.type_dict[ret] = tp
        self.temp += 4
        return ret
