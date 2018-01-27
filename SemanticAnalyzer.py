from constant import VariableType


class SemanticAnalyzer(object):
    def __init__(self, symbol_table, memory_manager, semantic_stack):
        self.symbol_table = symbol_table
        self.memory_manager = memory_manager
        self.semantic_stack = semantic_stack
        self.method_cnt = 0

    def set_local_search(self, current_token):
        self.symbol_table.local_search = True

    def reset_local_search(self, current_token):
        self.symbol_table.local_search = False

    def remove_last(self, current_token):
        self.semantic_stack.pop(1)

    def remove_prev(self, current_token):
        tmp = self.semantic_stack[-1]
        self.semantic_stack.pop(2)
        self.semantic_stack.push(tmp)

    def identifier(self, current_token):
        if self.symbol_table.local_search:
            # we know type of current token, we have already define this variable in this scope
            if current_token[1].tp is not None:
                raise SemanticError("{} is already defined in this scope.".format(current_token[1].name))
            else:
                current_token[1].tp = self.semantic_stack.top()
                self.semantic_stack.pop()
                if current_token[1].tp is not VariableType.CLASS:
                    current_token[1].address = self.memory_manager.get_variable(current_token[1].tp)

                if current_token[1].tp is VariableType.METHOD:
                    current_token[1].return_type = self.semantic_stack.top()
                    current_token[1].return_address = self.memory_manager.saved_pc_address + self.method_cnt * 4
                    self.method_cnt = self.method_cnt + 1
                    self.semantic_stack.pop()
        else:
            # we don't know type of current token, we didn't define this variable in this scope
            if current_token[1].tp is None:
                raise SemanticError("{} is not defined in this scope.".format(current_token[1].name))

    def add_row(self, current_token):
        self.semantic_stack.push(0)

    def identifier_parameter(self, current_token):
        identifier = self.semantic_stack[-1]
        number = self.semantic_stack[-2]
        self.semantic_stack.pop(2)
        self.semantic_stack.push(identifier)
        self.semantic_stack.push(number + 1)

    def end_parameter(self, current_token):
        current_line = self.semantic_stack.top()
        self.semantic_stack.pop(1)

        number = self.semantic_stack.top()
        self.semantic_stack.pop()
        ls = []

        for i in range(number):
            ls.append(self.semantic_stack[-1].address)

            self.semantic_stack.pop(1)

        self.semantic_stack.top().parameters = list(reversed(ls))
        self.semantic_stack.top().line = current_line

    def create_extend(self, current_token):
        self.symbol_table.extend_flag = True

    def start_scope(self, current_token):
        self.symbol_table.start_scope(current_token[1].name)

    def end_scope(self, current_token):
        self.symbol_table.end_scope()

    def identifier_int(self, current_token):
        self.semantic_stack.push(VariableType.INT)

    def identifier_boolean(self, current_token):
        self.semantic_stack.push(VariableType.BOOLEAN)

    def identifier_method(self, current_token):
        self.semantic_stack.push(VariableType.METHOD)

    def identifier_class(self, current_token):
        self.semantic_stack.push(VariableType.CLASS)

    def set_search_scope(self, current_token):
        self.semantic_stack.push(self.symbol_table.current)
        self.symbol_table.current = self.symbol_table.get_class_table(self.semantic_stack[-2])

    def reset_search_scope(self, current_token):
        tmp = self.semantic_stack[-1]
        self.symbol_table.current = self.semantic_stack[-2]
        self.semantic_stack.pop(3)
        self.semantic_stack.push(tmp)

    def add_zero(self, current_token):
        self.semantic_stack.push(0)

    def save_argument(self, current_token):
        tmp = self.semantic_stack[-1]
        ted = self.semantic_stack[-2] + 1
        self.semantic_stack.pop(2)
        self.semantic_stack.push(tmp)
        self.semantic_stack.push(ted)


class SemanticError(Exception):
    pass