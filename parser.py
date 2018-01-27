from SemanticAnalyzer import SemanticAnalyzer
from SymbolTable import OOPSymbolTable, SymbolTableRow
from code_generator import CodeGenerator
from stack import Stack
from grammer import PARSER_TABLE, TERMINALS, NON_TERMINALS, GRAMMAR, FOLLOW
from scanner import Scanner
from memory_manager import MemoryManager


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
        self.semantic_analyzer = SemanticAnalyzer(self.symbol_table, self.memory_manager, self.semantic_stack)
        self.code_generator = CodeGenerator(self.symbol_table, self.semantic_stack, self.memory_manager)
        self.current_identifier = None
        self.follow = FOLLOW
        self.non_terminal = 0

    def error_handler_panic_mode(self):
        if self.top_stack in TERMINALS:
            self.stack.pop()
            print("yek paiane kam bud")

            return

        follow = self.follow[self.top_stack]
        while self.next_token not in follow and self.next_token != "EOF":
            print(self.next_token, "ezafe bud")
            self.next_token = self.scanner.get_next_token()[0].value

        if self.non_terminal == 1 and self.next_token != "EOF":
            return

        self.stack.pop()
        print("kotah tarin ghaide ro")
        return

    def run(self):
        must_get = False
        while True:
            self.top_stack = self.stack.top()
         #   print(self.semantic_stack)
         #   print(self.stack, self.next_token, self.current_identifier)
         #   input()
        ##    print(self.next_token[0].value)
            if self.top_stack in TERMINALS:
                if must_get:
                    self.next_token = self.scanner.get_next_token()
                    must_get = False
                if self.next_token[0].value == self.top_stack:
                    if self.next_token[0].value == 'EOF':
                        break
                    self.stack.pop()
                    must_get = True
                else:
                    print("see error")
                    # self.error_handler_panic_mode()

            elif self.top_stack in NON_TERMINALS:
                if must_get:
                    self.next_token = self.scanner.get_next_token()
                    # self.next_token = tmp[0].value
                    # self.current_identifier = tmp[1]
                    must_get = False
                if self.next_token[0].value in self.parser_table[self.top_stack]:
                    self.push_rule_to_stack(self.parser_table[self.top_stack][self.next_token[0].value])
                else:
                    print("error")
                    # self.error_handler_panic_mode()

                self.top_stack = self.stack.top()

            elif self.top_stack.startswith("@"):
                eval('self.semantic_analyzer.%s(self.next_token)' % self.top_stack[1:])
                self.stack.pop()
            elif self.top_stack.startswith("#"):
                eval('self.code_generator.%s(self.next_token)' % self.top_stack[1:])
                self.stack.pop()
        self.code_generator.output_pb()

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


Parser('test6.java').run()
