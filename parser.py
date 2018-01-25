from stack import Stack
from grammer import PARSER_TABEL, TERMINALS, NON_TERMINALS, GRAMMER, FOLLOW
from scanner import Scanner
from code_generator import Genarator


class Parser(object):
    def __init__(self, file_name):
        self.file_name = file_name
        self.stack = Stack()
        self.stack.push("EOF")
        self.stack.push("Source")
        self.non_terminal = 1
        self.parser_table = PARSER_TABEL
        self.scanner = Scanner(file_name)
        self.next_token = self.scanner.get_next_token()[0].value
        self.top_stack = self.stack.top()
        self.rule = ""
        self.grammer = GRAMMER
        self.follow = FOLLOW
        self.code_generator = Genarator()

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
        while True:
            if self.top_stack == 'EOF':
                return
            self.top_stack = self.stack.top()
            if self.top_stack.startswith("#"):
                self.code_generator()

            print(self.stack, self.next_token, self.top_stack)
            if self.top_stack in TERMINALS:
                print("find terminal")
                if self.next_token == self.top_stack:
                    print("match terminal")
                    if self.next_token == 'EOF':
                        break
                    self.stack.pop()
                    self.next_token = self.scanner.get_next_token()[0].value

                else:
                    print("see error")
                    self.error_handler_panic_mode()

            elif self.top_stack in NON_TERMINALS:
                print("find non terminal")
                if self.next_token in self.parser_table[self.top_stack]:
                    print("match non terminal")
                    self.push_rule_to_stack(self.parser_table[self.top_stack][self.next_token])
                else:
                    self.error_handler_panic_mode()

                self.top_stack = self.stack.top()

    def push_rule_to_stack(self, rule_number):
        self.rule = self.grammer[rule_number]
        rules = self.rule.split(" ")
        self.stack.pop()
        print('***** ' + str(rules))
        for action in reversed(rules):
            if action in NON_TERMINALS:
                self.non_terminal += 1
            self.stack.push(action)
        self.non_terminal -= 2
        self.stack.pop()


P = Parser('test1.java').run()