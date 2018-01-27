from constant import VariableType, ErrorType
from error_handler import ErrorHandler


class SemanticAnalyzer(object):
    def __init__(self, symbol_table, memory_manager, semantic_stack):
        self.symbol_table = symbol_table
        self.memory_manager = memory_manager
        self.semantic_stack = semantic_stack
        self.error_handler = ErrorHandler()
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
                self.error_handler.rasie_error(ErrorType.Semantic, "Variable {} is already define in the scope"
                                         .format(current_token[1].name))
            else:
                current_token[1].tp = self.semantic_stack.top()
                self.semantic_stack.pop()

                if current_token[1].tp is VariableType.METHOD:
                    current_token[1].return_type = self.semantic_stack.top()
                    current_token[1].return_address = self.memory_manager.saved_pc_address + self.method_cnt * 4
                    self.method_cnt = self.method_cnt + 1
                    self.semantic_stack.pop()

                if current_token[1].tp is not VariableType.CLASS and current_token[1].tp is not VariableType.METHOD:
                    current_token[1].address = self.memory_manager.get_variable(current_token[1].tp)

                if current_token[1].tp is VariableType.METHOD:
                    current_token[1].address = self.memory_manager.get_variable(current_token[1].return_type)

        else:
            # we don't know type of current token, we didn't define this variable in this scope
            if current_token[1] is None:
                self.error_handler.rasie_error(ErrorType.Semantic, "can't resolve symbol")

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

    def return_assign(self, current_token):
        return_type = self.semantic_stack[-2].return_type.value
        value_type = self.memory_manager.get_tp(self.semantic_stack[-1]).value
        if return_type != value_type:
            self.error_handler.rasie_error(ErrorType.Semantic, 'Incompatible types. \n Required: {} \n Found: {}'.format(return_type, value_type))

    def call_method(self, current_token):
        ted = self.semantic_stack[-1]
        self.semantic_stack.pop(1)
        args = self.semantic_stack[-ted:]

        if len(args) < len(self.semantic_stack[-1 - ted].parameters):
            self.error_handler.rasie_error(ErrorType.Semantic, 'Expected more arguments')
        if len(args) > len(self.semantic_stack[-1 - ted].parameters):
            self.error_handler.rasie_error(ErrorType.Semantic, 'Expected less arguments')

        for i in range(len(args)):
            arg_type = self.memory_manager.get_tp(args[i]).value
            return_type = self.memory_manager.get_tp(self.semantic_stack[-1 -ted].parameters[i]).value
            if arg_type != return_type:
                self.error_handler.rasie_error(ErrorType.Semantic, "Wrong {}st argument type.Found: {}, requierd: {}".format(i+1, arg_type, return_type ))
        self.semantic_stack.push(ted)

    def assign(self, last_token):
        first_type = None
        second_type = None
        if isinstance(self.semantic_stack[-1], str):
            if self.semantic_stack[-1].startswith("#"):
                first_type = VariableType.INT
            else:
                first_type = VariableType.BOOLEAN
        else:
            first_type = self.memory_manager.get_tp(self.semantic_stack[-1])

        if isinstance(self.semantic_stack[-2], str):
            if self.semantic_stack[-2].startswith("#"):
                first_type = VariableType.INT
            else:
                first_type = VariableType.BOOLEAN
        else:
            second_type = self.memory_manager.get_tp(self.semantic_stack[-2])

        if first_type == second_type:
            return
        self.error_handler.rasie_error(ErrorType.Semantic, 'Incompatible types. \n Required: {} \n Found: {}'.format(second_type, first_type))
