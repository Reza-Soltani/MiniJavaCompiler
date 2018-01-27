from SemanticAnalyzer import SemanticAnalyzer
from SymbolTable import OOPSymbolTable, SymbolTableRow
from code_generator import CodeGenerator
from stack import Stack
from grammer import PARSER_TABLE, TERMINALS, NON_TERMINALS, GRAMMAR, FOLLOW
from scanner import Scanner
from memory_manager import MemoryManager
from error_handler import ErrorHandler
from constant import ErrorType


class Parser(object):
    def __init__(self, file_name):
        self.file_name = file_name
        self.stack = Stack()
        self.stack.push("EOF")
        self.stack.push("Source")
        self.parser_table = PARSER_TABLE
        self.symbol_table = OOPSymbolTable()
        self.semantic_stack = Stack()
        self.memory_manager = MemoryManager(1000, 2000)
        self.scanner = Scanner(file_name, self.symbol_table)
        self.next_token = self.scanner.get_next_token()
        self.top_stack = self.stack.top()
        self.rule_number = None
        self.rule = ""
        self.grammar = GRAMMAR
        self.error_handler = ErrorHandler(self.scanner)
        self.symbol_table.set_error_handler(self.error_handler)
        self.semantic_analyzer = SemanticAnalyzer(self.symbol_table, self.memory_manager, self.semantic_stack, self.error_handler)
        self.code_generator = CodeGenerator(self.symbol_table, self.semantic_stack, self.memory_manager)
        self.current_identifier = None
        self.follow = FOLLOW
        self.non_terminal = 0
        self.must_get = False

    def error_handler_panic_mode(self):
        if self.top_stack in TERMINALS:
            print(self.top_stack)
            self.stack.pop()
            self.must_get = False
            self.error_handler.rasie_error(ErrorType.Pars, "{} is left".format(self.top_stack))
            return

        follow = self.follow[self.top_stack]
        while self.next_token[0].value not in follow and self.next_token[0].value != "EOF":
            self.error_handler.rasie_error(ErrorType.Pars, "{} not allowed to be here!".format(self.next_token[0].value))
            self.next_token = self.scanner.get_next_token()

        if self.non_terminal == 1 and self.next_token[0].value != "EOF":
            self.must_get = False
            return
        if self.next_token[0].value == 'EOF':
            self.error_handler.rasie_error(ErrorType.Pars, "some terminal left")
            self.generate_code()

        self.stack.pop()
        self.must_get = False

    def run(self):
        while True:
            self.top_stack = self.stack.top()

            if self.top_stack in TERMINALS:
                if self.must_get:
                    self.next_token = self.scanner.get_next_token()
                    self.must_get = False
                if self.next_token[0].value == self.top_stack:
                    if self.next_token[0].value == 'EOF':
                        break
                    self.stack.pop()
                    self.must_get = True
                else:
                    self.error_handler_panic_mode()

            elif self.top_stack in NON_TERMINALS:
                if self.must_get:
                    self.next_token = self.scanner.get_next_token()
                    # self.next_token = tmp[0].value
                    # self.current_identifier = tmp[1]
                    self.must_get = False
                if self.next_token[0].value in self.parser_table[self.top_stack]:
                    self.push_rule_to_stack(self.parser_table[self.top_stack][self.next_token[0].value])
                else:
                    self.error_handler_panic_mode()

                self.top_stack = self.stack.top()

            elif self.top_stack.startswith("@"):
                eval('self.semantic_analyzer.%s(self.next_token)' % self.top_stack[1:])
                self.stack.pop()
            elif self.top_stack.startswith("#"):
                eval('self.code_generator.%s(self.next_token)' % self.top_stack[1:])
                self.stack.pop()
        self.generate_code()

    def push_rule_to_stack(self, rule_number):
        self.rule = self.grammar[rule_number]
        rules = self.rule.split(" ")
        self.stack.pop()
        for action in reversed(rules):
            if action in NON_TERMINALS:
                self.non_terminal += 1
            self.stack.push(action)
        self.non_terminal -= 2
        self.stack.pop()

    def generate_code(self):
        self.code_generator.output_pb()
        sys.exit()


if __name__ == '__main__':
    import sys
    Parser(sys.argv[1]).run()
