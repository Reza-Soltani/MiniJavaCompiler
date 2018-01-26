from enum import Enum

from tokens import Tokens


class CodeGenerator(object):
    def __init__(self, symbol_table, semantic_stack, memory_manager):
        self.symbol_table = symbol_table
        self.semantic_stack = semantic_stack
        self.memory_manager = memory_manager
        self.program_block = []

    def make_command(self, command, first=None, second=None, third=None):
        row = "(" + command.value + first
        if second is not None:
            row += second
        else:
            return row + ',,)'
        if third is not None:
            row += third
        else:
            return row + ',)'
        return row + ")"

    def set_local_search(self, last_token):
        print('local_search')
        pass

    def reset_local_search(self, last_token):
        pass

    def create_class(self, last_token):
        pass

    def create_extend(self, last_token):
        pass

    def start_scope(self, last_token):
        pass

    def end_scope(self, last_token):
        pass

    def Pid(self, last_token):
        address = last_token[1].address
        self.semantic_stack.push(address)

    def assign(self, last_token):
        command = self.make_command(Commands.ASSIGN, self.semantic_stack[-1], self.semantic_stack[-2])
        self.program_block.append(command)
        self.semantic_stack.pop(2)

    def Cmp_save(self, last_token):
        self.program_block.append("")
        self.semantic_stack.push(len(self.program_block))

    def Int(self, last_token):
        self.semantic_stack.push('#' + last_token[0].value)

    def For(self, last_token):
        command = self.make_command(Commands.ADD, self.semantic_stack[-2], self.semantic_stack[-1], self.semantic_stack[-2])
        self.program_block.append(command)
        command = self.make_command(Commands.JP, self.semantic_stack[-3] - 1)
        self.program_block.append(command)
        command = self.make_command(Commands.JPF, self.semantic_stack[-4], len(self.program_block) + 1)
        self.program_block[self.semantic_stack[-3]] = command
        self.semantic_stack.pop(5)

    def Check_equal(self, last_token):
        pass

    def Check_less(self, last_token):
        pass

    def immediate_integer(self, last_token):
        self.semantic_stack.push('#' + str(last_token[1]))

    def identifier(self, last_token):
        self.semantic_stack.push(last_token[1].address)

    def identifier_name(self, last_token):
        self.semantic_stack.push(last_token[1].name)

    def immediate_bool(self, last_token):
        self.semantic_stack.push(last_token.value)

    def aggregate(self, last_token):
        tmp = self.symbol_table.get_class_table(self.semantic_stack[-2]).get(last_token[1].name).address
        self.semantic_stack.pop(3)
        self.semantic_stack.push(tmp)

    def multi_operation(self, last_token):
        tmp = self.memory_manager.get_variable()
        self.program_block.append(self.make_command(Commands.MULT,
                                                    self.semantic_stack[-2],
                                                    self.semantic_stack[-1],
                                                    tmp))
        self.semantic_stack.pop(2)
        self.semantic_stack.push(tmp)

    def plus_operation(self, last_token):
        tmp = self.memory_manager.get_variable()
        self.program_block.append(self.make_command(Commands.ADD,
                                                    self.semantic_stack[-2],
                                                    self.semantic_stack[-1],
                                                    tmp))
        self.semantic_stack.pop(2)
        self.semantic_stack.push(tmp)

    def minus_operation(self, last_token):
        tmp = self.memory_manager.get_variable()
        self.program_block.append(self.make_command(Commands.SUB,
                                                    self.semantic_stack[-2],
                                                    self.semantic_stack[-1],
                                                    tmp))
        self.semantic_stack.pop(2)
        self.semantic_stack.push(tmp)

    def assign(self, last_token):
        self.program_block.append(self.make_command(Commands.ASSIGN,
                                                    self.semantic_stack[-1],
                                                    self.semantic_stack[-2]))

    def identifier_class(self, last_token):
        pass

    def identifier_boolean(self, last_token):
        pass

    def identifier_int(self, last_token):
        pass

    def identifier_method(self, last_token):
        pass

    def identifier_parametr(self, last_token):
        pass

    def end_parametr(self, last_token):
        pass


class Command(object):
    def __init__(self, command, *parameters):
        self.command = command
        self.parameters = parameters


class Commands(Enum):
    ADD = 'ADD'
    SUB = 'SUB'
    AND = 'AND'
    ASSIGN = 'ASSIGN'
    EQ = 'EQ'
    JPF = 'JPF'
    JP = 'JP'
    LT = 'LT'
    MULT = 'MULT'
    NOT = 'NOT'
    PRINT = 'PRINT'
