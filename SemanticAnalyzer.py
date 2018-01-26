class SemanticAnalyzer(object):
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table

    def set_local_search(self, current_token):
        self.symbol_table.local_search = True
        pass

    def reset_local_search(self, current_token):
        self.symbol_table.local_search = False
        pass

    def create_extend(self, current_token):
        self.symbol_table.extend_flag = True
        pass

    def start_scope(self, current_token):
        self.symbol_table.start_scope(current_token.name)
        pass

    def end_scope(self, current_token):
        self.symbol_table.end_scope()
        pass
