from error_handler import ErrorHandler
from constant import ErrorType


class SymbolTableRow(object):
    def __init__(self, name, address=None, tp=None):
        self.name = name
        self.address = address
        self.tp = tp
        self.return_type = None
        self.parameters = []
        self.line = None

    def __str__(self):
        return 'name is ' + self.name


class SymbolTable(object):
    def __init__(self, name, father=None):
        self.name = name
        self.father = father
        self.table = []

    def local_search(self, name):
        for row in reversed(self.table):
            if row.name == name:
                return row
        self.create(name)
        return self.table[-1]

    def global_search(self, name):
        for row in reversed(self.table):
            if row.name == name:
                return row
        return None

    def create(self, name):
        self.table.append(SymbolTableRow(name))


class OOPSymbolTable(object):
    def __init__(self):
        self.main = SymbolTable('main')
        self.current = self.main
        self.local_search = False
        self.extend_flag = False
        self.classes = dict()
        self.top_scope = None
        self.error_handler = ErrorHandler()

    def get(self, name):
        if self.extend_flag:
            try:
                self.current.father = self.classes[name]
            except:
                self.error_handler.rasie_error(ErrorType.Semantic, "can't resolve symbol")
            # print('father ', self.current.name, name)
            self.extend_flag = False
        if self.local_search:
            return self.current.local_search(name)
        else:
            return self.global_search(name)

    def global_search(self, name):
        sym = self.current
        while True:
            #print(sym.name)
            ret = sym.global_search(name)
            if ret is not None:
                return ret
            if sym.father is not None:
                sym = sym.father
            else:
                break
        return None

    def start_scope(self, name):
        # print('starting scope', name)
        prev = self.current
        self.current = SymbolTable(name, self.current)
        self.current.top_scope = prev
        # print('father ', self.current.name, prev.name)
        self.current.father = prev
        if prev.name == 'main':
            self.classes[name] = self.current

    def end_scope(self):
        # print('end scope ', self.current.name, self.current.top_scope.name)
        self.current = self.current.top_scope

    def get_class_table(self, name):
        return self.classes[name]
