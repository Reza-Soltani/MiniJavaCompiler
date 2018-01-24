from ScannerDFANode import Node, make_path
from tokens import Tokens

print(Tokens.PLUS_SIGN.value)


class Scanner(object):

    def __init__(self, address):
        self.begin = 0
        self.forward = 0
        self.root = None
        self.source_code = open(address).read()
        self.make_dfa()
        node_and_token = self.root, None
        print(node_and_token[0].name)
        for i in range(len(self.source_code)):
            # if self.source_code[i] == '+':
            #     pass
            node_and_token = node_and_token[0].get_next_node(self.source_code[i])
            print(node_and_token[1])

    def get_next_token(self):
        """
        the only interface of scanner, gives the next token to parser
        :return: next token
        """

    def make_dfa(self):
        self.root = Node('root')

        self.root.add_edge(['\n', '\t', ' ', '\r'], self.root)  # skip space, tab and newline

        equal_first = Node('equal_first')
        equal_second = Node('equal_second')

        # handle +, +=
        first_positive = Node('first_positive')
        positive_equal = Node('positive_equal')
        self.root.add_edge(['+'], first_positive)
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

        make_path('(', Tokens.OPEN_PARENTHESES)
        make_path(')', Tokens.CLOSE_PARENTHESES)
        make_path('{', Tokens.OPEN_BRACKET)
        make_path('}', Tokens.CLOSE_PARENTHESES)
        make_path('&&', Tokens.DOUBLE_AND)
        make_path('public', Tokens.PUBLIC)
        make_path('EOF', Tokens.EOF)
        make_path('class', Tokens.CLASS)
        make_path('void', Tokens.VOID)
        make_path('main', Tokens.MAIN)
        make_path('extends', Tokens.EXTENDS)
        make_path('static', Tokens.STATIC)
        make_path(';', Tokens.SEMICOLON)
        make_path('return', Tokens.RETURN)
        make_path('colon', Tokens.COLON)
        make_path('boolean', Tokens.BOOLEAN)
        make_path('int', Tokens.INT)
        make_path('if', Tokens.IF)
        make_path('else', Tokens.ELSE)
        make_path('for', Tokens.FOR)
        make_path('while', Tokens.WHILE)
        make_path('system.out.println', Tokens.SYSOUT)  # TODO: think about this one!
        make_path('-', Tokens.MINUS_SIGN)
        make_path('*', Tokens.MULTI_SIGN)
        make_path('.', Tokens.DOT)
        make_path('<', Tokens.LESS)


a = Scanner('test1.java')
