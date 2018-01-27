import SymbolTable
from ScannerDFANode import Node, make_path
from tokens import Tokens


class Scanner(object):
    SIGN_PLUS = [Tokens.CLOSE_PARENTHESES, Tokens.IDENTIFIER, Tokens.INTEGER, Tokens.TRUE, Tokens.FALSE]

    def __init__(self, address, symbol_table):
        self.begin = 0
        self.forward = 0
        self.root = None
        self.source_code = open(address).read()
        self.make_dfa()
        self.last_token = None
        self.symbol_table = symbol_table
        # node_and_token = self.root, None
        # print(node_and_token[0].name)
        # for i in range(len(self.source_code)):
        #     # if self.source_code[i] == '+':
        #     #     pass
        #     node_and_token = node_and_token[0].get_next_node(self.source_code[i])
        #     print(node_and_token[0].name, node_and_token[1], self.source_code[i])

    def get_next_token(self):
        node_and_token = self.root, None
        self.begin = self.forward
        while True:
            if node_and_token[0].name == 'root':
                self.begin = self.forward
            current_char = self.source_code[self.forward]
            if current_char == '+' and self.last_token in Scanner.SIGN_PLUS:
                current_char = '%'
            if current_char == '-' and self.last_token in Scanner.SIGN_PLUS:
                current_char = '^'
            node_and_token = node_and_token[0].get_next_node(current_char, self.root)
            if node_and_token[1] is not None:
                self.last_token = node_and_token[1]
                return node_and_token[1], self.get_attribute(node_and_token[1])  # TODO: check None value
            self.forward += 1
            if self.forward >= len(self.source_code):
                self.forward -= 1
                if self.last_token == Tokens.EOF:
                    print('Error: no more token after end of file')
                    return None, None
                elif node_and_token[0].name == 'EOF 2':
                    return Tokens.EOF, None
                else:
                    print('Error: no EOF at the end of file')
                    return None, None

    def make_dfa(self):
        self.root = Node('root')

        self.root.add_edge(['\n', '\t', ' ', '\r'], self.root)  # skip space, tab and newline

        equal_first = Node('equal_first')
        equal_second = Node('equal_second')

        # handle +, +=
        first_positive = Node('first_positive')
        positive_equal = Node('positive_equal')
        self.root.add_edge(['%'], first_positive)
        first_positive.other_case(self.root)
        first_positive.other_token(Tokens.PLUS_SIGN)
        first_positive.add_edge(['='], positive_equal)
        positive_equal.other_case(self.root)
        positive_equal.other_token(Tokens.PLUS_EQUAL)

        # =, ==
        self.root.add_edge(['='], equal_first)
        equal_first.other_case(self.root)
        equal_first.other_token(Tokens.EQUAL_SIGN)
        equal_first.add_edge(['='], equal_second)
        equal_second.other_case(self.root)
        equal_second.other_token(Tokens.EQUAL_EQUAL)

        # comments
        comment_first = Node('comment_first')
        comment_skip = Node('comment_skip')
        comment_end = Node('comment_end')
        comment_line = Node('comment_line')
        self.root.add_edge(['/'], comment_first)
        comment_first.add_edge(['*'], comment_skip)
        comment_first.add_edge(['/'], comment_line)
        comment_skip.add_edge(['*'], comment_end)
        comment_skip.other_case(comment_skip)
        comment_end.add_edge(['/'], self.root)
        comment_end.other_case(comment_skip)
        comment_line.add_edge(['\n'], self.root)
        comment_line.other_case(comment_line)


        # identifier and integer nodes
        digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '-']
        digit = Node('digit')
        self.root.add_edge(digits, digit)
        digits.pop()
        digits.pop()
        digit.add_edge(digits, digit)
        digit.other_case(self.root)
        digit.other_token(Tokens.INTEGER)

        letter = Node('letter')
        self.root.letter_case(letter)
        letter.letter_case(letter)
        letter.other_case(self.root)
        letter.other_token(Tokens.IDENTIFIER)

        make_path('(', self.root, letter, Tokens.OPEN_PARENTHESES)
        make_path(')', self.root, letter, Tokens.CLOSE_PARENTHESES)
        make_path('{', self.root, letter, Tokens.OPEN_BRACKET)
        make_path('}', self.root, letter, Tokens.CLOSE_BRACKET)
        make_path('&&', self.root, letter, Tokens.DOUBLE_AND)
        make_path('public', self.root, letter, Tokens.PUBLIC)
        make_path('EOF', self.root, letter, Tokens.EOF)
        make_path('class', self.root, letter, Tokens.CLASS)
        make_path('void', self.root, letter, Tokens.VOID)
        make_path('main', self.root, letter, Tokens.MAIN)
        make_path('extends', self.root, letter, Tokens.EXTENDS)
        make_path('static', self.root, letter, Tokens.STATIC)
        make_path(';', self.root, letter, Tokens.SEMICOLON)
        make_path('return', self.root, letter, Tokens.RETURN)
        make_path(',', self.root, letter, Tokens.COLON)
        make_path('boolean', self.root, letter, Tokens.BOOLEAN)
        make_path('int', self.root, letter, Tokens.INT)
        make_path('if', self.root, letter, Tokens.IF)
        make_path('else', self.root, letter, Tokens.ELSE)
        make_path('for', self.root, letter, Tokens.FOR)
        make_path('while', self.root, letter, Tokens.WHILE)
        make_path('System.out.println', self.root, letter, Tokens.SYSOUT)
        make_path('^', self.root, letter, Tokens.MINUS_SIGN)
        make_path('*', self.root, letter, Tokens.MULTI_SIGN)
        make_path('.', self.root, letter, Tokens.DOT)
        make_path('<', self.root, letter, Tokens.LESS)
        make_path('true', self.root, letter, Tokens.TRUE)
        make_path('false', self.root, letter, Tokens.FALSE)

    def get_attribute(self, token):
      #  print('wtf ' + self.source_code[self.begin:self.forward])
        if token == Tokens.INTEGER:
            return int(self.source_code[self.begin:self.forward])
        elif token == Tokens.IDENTIFIER:
            return self.symbol_table.get(self.source_code[self.begin:self.forward])
        else:
            return None

    def get_line_number(self):
        return self.source_code[:self.forward].count('\n') + 1

    def get_last_identifier_name(self):
        return self.source_code[self.begin:self.forward]
