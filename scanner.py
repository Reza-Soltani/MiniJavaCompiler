from settings import buff_length


class Scanner:

    address = None
    buff = list()
    begin = 0
    forward = 0

    def __init__(self, address):
        self.address = address
        self.buff = [' '] * buff_length
        self.buff[-1] = 'EOF'
        self.buff[buff_length / 2 - 1] = 'EOF'

    def get_next_token(self):
        """
        only interface of scanner, gives the next token to parser
        :return: next token
        """

        while True:
            ret = self._check_pattern(self._get_lexeme(self.begin, self.forward))

            if ret[0]:
                self.begin = self.forward
                if not ret[2]:
                    self.begin = self.begin = self.begin + 1
                    if self.buff[self.begin] is 'EOF':
                        self.begin = (self.begin + 1) % buff_length
                return ret[1]

            self.forward += 1
            if self.buff[self.forward] is 'EOF':
                if self.forward is (buff_length / 2 - 1):
                    self._reload_second_half()
                    self.forward += 1
                elif self.forward is (buff_length - 1):
                    self._reload_first_half()
                    self.forward = 0
                else:
                    return 'EOF', None

    def _check_pattern(self, string):
        """
        check for finding some pattern in string
        :param string: lexeme that must be checked for some pattern
        :return: a tuple with two element.
            first element is a boolean that describe does we find a pattern ?
            second element is the token if first element is true and None o.w.
            third element is a boolean that describe will be the last character useful in future?
        """

        pass

    def _get_lexeme(self, begin, forward):
        return self.buff[begin:forward+1]

    def _reload_second_half(self):
        pass

    def _reload_first_half(self):
        pass
