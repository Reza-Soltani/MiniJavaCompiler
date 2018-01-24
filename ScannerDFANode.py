from tokens import Tokens


def make_path(string, root, letter_node, token):
    node = root
    dotorand = False
    for i in range(len(string)):
        c = string[i]
        if c not in node.nx:
            node.nx[c] = Node(string + ' ' + str(i))
        node = node.nx[c]
        if c == '.' or c == '&':
            dotorand = True
        if i + 1 != len(string):
            if dotorand:
                node.other_case(root)
            else:
                node.letter_case(letter_node)
                node.other_case(root)
                node.other_token(Tokens.IDENTIFIER)
    node.other_case(root)
    node.other_token(token)


PANIC_MODE_SCANNER_CHARS = [';', '}', ')']


class Node(object):

    def __init__(self, name):
        self.name = name
        self.nx = dict()
        self.ow = None
        self.other = None
        self.letter_goal = None
        # print(self.nx)

    def letter_case(self, sink):
        self.letter_goal = sink

    def add_edge(self, param, sink):
        # print(self.name, param, sink)
        for c in param:
            if c in self.nx:
                if self.nx[c] != sink:
                    raise Exception('duplicate edge in dfa with different sinks, node name is: {}'.format(self.name))
            else:
                self.nx[c] = sink

    def other_case(self, sink):
        self.ow = sink

    def get_next_node(self, char, root):
        if char in self.nx:
            return self.nx[char], None
        if self.letter_goal is not None and (str.isalpha(char) or str.isdigit(char)):
            return self.letter_goal, None
        if self.ow is not None:
            return self.ow, self.other
        if char in PANIC_MODE_SCANNER_CHARS: # panic mode error handling in dfa
            print('Error: SKIPPED INPUT UNTIL {}'.format(char))
            return root, None
        return self, None

    def other_token(self, other_token):
        self.other = other_token
