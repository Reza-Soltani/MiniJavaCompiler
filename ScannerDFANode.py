def make_path(root, string, token):
    node = root
    for i in range(len(string)):
        c = string[i]
        if c not in node.nx:
            node.nx[c] = Node(string + ' ' + str(i))
        node = node.nx[c]


class Node(object):

    def __init__(self, name):
        self.name = name
        self.nx = dict()
        self.ow = None
        self.other = None
        print(self.nx)

    def add_edge(self, param, sink):
        print(self.name, param, sink)
        for c in param:
            if c in self.nx:
                if self.nx[c] != sink:
                    raise Exception('duplicate edge in dfa with different sinks, node name is: {}'.format(self.name))
            else:
                self.nx[c] = sink

    def other_case(self, sink):
        self.ow = sink

    def get_next_node(self, char):
        if char in self.nx:
            return self.nx[char], None
        if self.ow is not None:
            return self.ow, self.other
        return self, None

    def other_token(self, other_token):
        self.other = other_token
