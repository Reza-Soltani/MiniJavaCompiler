from constant import VaribaleType


class SemanticAnalyzer(object):
    def __init__(self, symbol_table, memory_manager, semantic_stack):
        self.symbol_table = symbol_table
        self.memory_manager = memory_manager
        self.semantic_stack = semantic_stack

    def set_local_search(self, current_token):
        self.symbol_table.local_search = True
        pass

    def reset_local_search(self, current_token):
        if current_token[1].address is None:
            current_token[1].address = self.memory_manager.get_variable()
            # print("**************", current_token, self.semantic_stack.top().name)
            current_token[1].tp = self.semantic_stack.top()
            self.semantic_stack.pop()
            if current_token[1].tp == VaribaleType.METHOD:
                print("see method", self.semantic_stack[-1])
                current_token[1].return_type = self.semantic_stack[-1]
                self.semantic_stack.pop()
                self.semantic_stack.push(current_token)
                self.semantic_stack.push(0)
        else:
            print("ridiiiiiiiiiiiiiiiiii")
        self.symbol_table.local_search = False
        pass

    def identifier_parametr(self, current_token):
        type = self.semantic_stack.top()
        number = self.semantic_stack[-2]
        self.semantic_stack.pop(2)
        self.semantic_stack.push(type)
        self.semantic_stack.push(current_token)
        self.semantic_stack.push(number+1)

    def end_parametr(self, current_token):
        number = self.semantic_stack.top()
        self.semantic_stack.pop()
        list = []

        for i in range(number):
            if self.semantic_stack[-1][1].address is not None:
                print("bazaaam rididiii")
                return
            type = self.semantic_stack[-2]
            self.semantic_stack[-1][1].tp = type

            self.semantic_stack[-1][1].address = self.memory_manager.get_variable()
            list.append(self.semantic_stack[-1][1])
            self.semantic_stack.pop(2)

        self.semantic_stack.top()[1].parametrs = reversed(list)
        # print("###########", number, self.semantic_stack.top()[1].tp, self.semantic_stack.top()[1].name, self.semantic_stack.top()[1].parametrs)
        self.semantic_stack.pop()
        self.symbol_table.local_search = False

    def create_extend(self, current_token):
        self.symbol_table.extend_flag = True
        pass

    def start_scope(self, current_token):
        self.symbol_table.start_scope(current_token[1].name)
        pass

    def end_scope(self, current_token):
        self.symbol_table.end_scope()
        pass

    def identifier_int(self, last_token):
        self.semantic_stack.push(VaribaleType.INT)

    def identifier_boolean(self, last_token):
        self.semantic_stack.push(VaribaleType.BOOLEAN)

    def identifier_method(self, last_token):
        self.semantic_stack.push(VaribaleType.METHOD)

    def identifier_class(self, last_token):
        self.semantic_stack.push(VaribaleType.CLASS)

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


