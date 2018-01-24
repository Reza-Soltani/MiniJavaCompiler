from stack import Stack
from grammer import PARSER_TABEL, TERMINALS, NON_TERMINALS
from scanner import Scanner


class parser(object):
    def __init__(self, file_name):
        self.file_name = file_name
        self.stack = Stack()
        self.parser_table = PARSER_TABEL
        self.scanner = Scanner(file_name)
        self.next_token = None
        self.top_stack = None
        self.rule_number = None
        self.rule = ""

    def run(self):
        self.next_token = Scanner.get_next_token()
        if self.top_stack in TERMINALS:
            pass

        elif self.top_stack in NON_TERMINALS:
            if self.next_token in self.parser_table[self.top_stack]:
                pass
            else:
                return "error"



    def push_to_scanner(self, rule):


