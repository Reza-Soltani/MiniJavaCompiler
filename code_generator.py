from enum import Enum
from constant import Commands, VaribaleType


class CodeGenerator(object):
    def __init__(self, symbol_table, semantic_stack, memory_manager):
        self.symbol_table = symbol_table
        self.semantic_stack = semantic_stack
        self.memory_manager = memory_manager
        self.program_block = []

    def make_command(self, command, first=None, second=None, third=None):
        row = "(" + command.name + first
        if second is not None:
            row += second
        else:
            return row + ',,)'
        if third is not None:
            row += third
        else:
            return row + ',)'
        return row + ")"

    def Pid(self, current_token):
        address = current_token[1].address
        self.semantic_stack.push(address)

    def assign(self, current_token):
        command = self.make_command(Commands.ASSIGN, self.semantic_stack[-1], self.semantic_stack[-2])
        self.program_block.append(command)
        self.semantic_stack.pop(2)

    def Cmp_save(self, current_token):
        self.program_block.append("")
        self.semantic_stack.push(len(self.program_block))

    def Int(self, current_token):
        self.semantic_stack.push('#' + last_token[0].value)

    def For(self, current_token):
        command = self.make_command(Commands.ADD, self.semantic_stack[-2], self.semantic_stack[-1], self.semantic_stack[-2])
        self.program_block.append(command)
        command = self.make_command(Commands.JP, self.semantic_stack[-3] - 1)
        self.program_block.append(command)
        command = self.make_command(Commands.JPF, self.semantic_stack[-4], len(self.program_block) + 1)
        self.program_block[self.semantic_stack[-3]] = command
        self.semantic_stack.pop(5)

    def Check_equal(self, current_token):
        pass

    def Check_less(self, current_token):
        pass

