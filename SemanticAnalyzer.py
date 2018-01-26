from constant import VariableType


class SemanticAnalyzer(object):
    def __init__(self, symbol_table, memory_manager, semantic_stack):
        self.symbol_table = symbol_table
        self.memory_manager = memory_manager
        self.semantic_stack = semantic_stack

    def set_local_search(self, current_token):
        self.symbol_table.local_search = True

    def reset_local_search(self, current_token):
        self.symbol_table.local_search = False

    def identifier(self, current_token):
        if self.symbol_table.local_search:
            # we know type of current token, we already define this variable in this scope
            if current_token[1].tp is not None:
                raise SemanticError("{} is already define in this scope".format(current_token[1].name))
            else:
                current_token[1].tp = self.semantic_stack.top()
                self.semantic_stack.pop()
                if current_token[1].tp is not VariableType.CLASS:
                    current_token[1].address = self.memory_manager.get_variable()

                if current_token[1].tp is VariableType.METHOD:
                    current_token[1].return_type = self.semantic_stack.top()
                    self.semantic_stack.pop()
        else:
            # we don't know type of current token, we don't define this variable in this scope
            if current_token[1].tp is None:
                raise SemanticError("{} is not define in this scope".format(current_token[1].name))

    def add_row(self, current_token):
        self.semantic_stack.push(current_token[1])
        self.semantic_stack.push(0)

    def identifier_parameter(self, current_token):
        identifier = self.semantic_stack.top()
        type = self.semantic_stack[-2]
        number = self.semantic_stack[-3]
        self.semantic_stack.pop(3)
        self.semantic_stack.push(type)
        self.semantic_stack.push(identifier)
        self.semantic_stack.push(number+1)

    def end_parameter(self, current_token):
        number = self.semantic_stack.top()
        self.semantic_stack.pop()
        list = []

        for i in range(number):
            type = self.semantic_stack[-2]
            address = self.semantic_stack[-1]
            list.append((type, address))

            self.semantic_stack.pop(2)

        self.semantic_stack.top()[1].parametrs = reversed(list)

    def create_extend(self, current_token):
        self.symbol_table.extend_flag = True
        pass

    def start_scope(self, current_token):
        self.symbol_table.start_scope(current_token[1].name)
        pass

    def end_scope(self, current_token):
        self.symbol_table.end_scope()
        pass

    def identifier_int(self, current_token):
        self.semantic_stack.push(VariableType.INT)

    def identifier_boolean(self, current_token):
        self.semantic_stack.push(VariableType.BOOLEAN)

    def identifier_method(self, current_token):
        self.semantic_stack.push(VariableType.METHOD)

    def identifier_class(self, current_token):
        self.semantic_stack.push(VariableType.CLASS)

    def Pid(self, last_token):
        pass

    def assign(self, last_token):
        pass

    def Cmp_save(self, last_token):
        pass

    def Int(self, last_token):
        pass

    def For(self, last_token):
        pass

    def Check_equal(self, last_token):
        pass

    def Check_less(self, last_token):
        pass

    def immediate_integer(self, last_token):
        pass


class SemanticError(Exception):
    pass


