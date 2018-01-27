from constant import Commands, VariableType


def make_command(command, first=None, second=None, third=None):
    row = "( " + command.value + ", " + str(first)
    if second is not None:
        row += ', ' + str(second)
    else:
        return row + ', , )'
    if third is not None:
        row += ', ' + str(third)
    else:
        return row + ', )'
    return row + " )"


class CodeGenerator(object):
    def __init__(self, symbol_table, semantic_stack, memory_manager):
        self.symbol_table = symbol_table
        self.semantic_stack = semantic_stack
        self.memory_manager = memory_manager
        self.program_block = []
        self.program_block.append("")

    def get_current_line(self, current_token):
        self.semantic_stack.push(len(self.program_block))

    def call_method(self, current_token):
        ted = self.semantic_stack[-1]
        self.semantic_stack.pop(1)
        args = self.semantic_stack[-ted:]
        self.semantic_stack.pop(ted)
        if len(args) < len(self.semantic_stack[-1].parameters):
            raise Exception('Expected more arguments')
        if len(args) > len(self.semantic_stack[-1].parameters):
            raise Exception('Expected less arguments')
        for i in range(len(args)):
            self.program_block.append(make_command(Commands.ASSIGN,
                                                   args[i],
                                                   self.semantic_stack[-1].parameters[i]))
        self.program_block.append(make_command(Commands.ASSIGN,
                                               '#' + str(len(self.program_block) + 2),
                                               self.memory_manager.saved_pc_address))
        self.program_block.append(make_command(Commands.JP,
                                               self.semantic_stack[-1].line))
        tmp = self.semantic_stack[-1].address
        self.semantic_stack.pop(1)
        self.semantic_stack.push(tmp)

    def return_assign(self, current_token):
        self.program_block.append(make_command(Commands.ASSIGN,
                                               self.semantic_stack[-1],
                                               self.semantic_stack[-2].address))
        self.semantic_stack.pop(2)
        self.program_block.append(make_command(Commands.JP,
                                               '@' + str(self.memory_manager.saved_pc_address)))

    def end_for(self, current_token):
        self.end_while(current_token)

    def plus_assign(self, current_token):
        self.program_block.append(make_command(Commands.ADD,
                                               self.semantic_stack[-1],
                                               self.semantic_stack[-2],
                                               self.semantic_stack[-2]))
        self.semantic_stack.pop(2)

    def end_while(self, current_token):
        self.program_block.append(make_command(Commands.JP,
                                               self.semantic_stack[-3]))
        self.program_block[self.semantic_stack[-1]] = make_command(Commands.JPF,
                                                                   self.semantic_stack[-2],
                                                                   len(self.program_block))
        self.semantic_stack.pop(3)

    def label(self, current_token):
        self.semantic_stack.push(len(self.program_block))

    def save(self, current_token):
        self.semantic_stack.push(len(self.program_block))
        self.program_block.append('')

    def jpf_save(self, current_token):
        self.save(current_token)
        self.program_block[self.semantic_stack[-2]] = make_command(Commands.JPF,
                                                                   self.semantic_stack[-3],
                                                                   len(self.program_block))
        tmp = self.semantic_stack[-1]
        self.semantic_stack.pop(3)
        self.semantic_stack.push(tmp)

    def jump_here(self, current_token):
        self.program_block[self.semantic_stack[-1]] = make_command(Commands.JP,
                                                                   len(self.program_block))
        self.semantic_stack.pop(1)

    def sys_out(self, current_token):
        self.program_block.append(make_command(Commands.PRINT,
                                               self.semantic_stack[-1]))
        self.semantic_stack.pop(1)

    def and_operation(self, current_token):
        tmp = self.memory_manager.get_temp(VariableType.BOOLEAN)
        self.program_block.append(make_command(Commands.AND,
                                               self.semantic_stack[-2],
                                               self.semantic_stack[-1],
                                               tmp))
        self.semantic_stack.pop(2)
        self.semantic_stack.push(tmp)

    def rel_equal(self, current_token):
        tmp = self.memory_manager.get_temp(VariableType.BOOLEAN)
        self.program_block.append(make_command(Commands.EQ,
                                               self.semantic_stack[-2],
                                               self.semantic_stack[-1],
                                               tmp))
        self.semantic_stack.pop(2)
        self.semantic_stack.push(tmp)

    def rel_less(self, current_token):
        tmp = self.memory_manager.get_temp(VariableType.BOOLEAN)
        self.program_block.append(make_command(Commands.LT,
                                               self.semantic_stack[-2],
                                               self.semantic_stack[-1],
                                               tmp))
        self.semantic_stack.pop(2)
        self.semantic_stack.push(tmp)

    def immediate_integer(self, last_token):
        self.semantic_stack.push('#' + str(last_token[1]))

    def identifier(self, last_token):
        if self.symbol_table.local_search or last_token[1].tp == VariableType.METHOD:
            self.semantic_stack.push(last_token[1])
        else:
            self.semantic_stack.push(last_token[1].address)

    def identifier_name(self, last_token):
        self.semantic_stack.push(last_token[1].name)

    def immediate_bool(self, last_token):
        self.semantic_stack.push(last_token[0].value)

    # def aggregate(self, last_token):
    #     tmp = self.symbol_table.get_class_table(self.semantic_stack[-2]).get(last_token[1].name).address
    #     self.semantic_stack.pop(3)
    #     self.semantic_stack.push(tmp)

    def multi_operation(self, last_token):
        tmp = self.memory_manager.get_temp(VariableType.INT)
        self.program_block.append(make_command(Commands.MULT,
                                               self.semantic_stack[-2],
                                               self.semantic_stack[-1],
                                               tmp))
        self.semantic_stack.pop(2)
        self.semantic_stack.push(tmp)

    def plus_operation(self, last_token):
        tmp = self.memory_manager.get_temp(VariableType.INT)
        self.program_block.append(make_command(Commands.ADD,
                                               self.semantic_stack[-2],
                                               self.semantic_stack[-1],
                                               tmp))
        self.semantic_stack.pop(2)
        self.semantic_stack.push(tmp)

    def minus_operation(self, last_token):
        tmp = self.memory_manager.get_temp(VariableType.INT)
        self.program_block.append(make_command(Commands.SUB,
                                               self.semantic_stack[-2],
                                               self.semantic_stack[-1],
                                               tmp))
        self.semantic_stack.pop(2)
        self.semantic_stack.push(tmp)

    def assign(self, last_token):
        self.program_block.append(make_command(Commands.ASSIGN,
                                               self.semantic_stack[-1],
                                               self.semantic_stack[-2]))
        self.semantic_stack.pop(2)

    def start_main(self, last_token):
        self.program_block[0] = make_command(Commands.JP,
                                             len(self.program_block))

    def output_pb(self):
        with open("output.txt", "w") as result:
            for i in range(len(self.program_block)):
                result.write(str(i) + "\t" + self.program_block[i] + "\n")
