from constant import ErrorType
import sys


class ErrorHandler(Exception):
    def __init__(self, scanner):
        self.scanner = scanner

    def rasie_error(self, error_type, error):
        error = error.replace('@', self.scanner.get_last_identifier_name())
        if error_type.value == ErrorType.Semantic.value:
            print('Error in line ' + str(self.scanner.get_line_number()) + ': ' + error)
            sys.exit()
        else:
            print('Error in line ' + str(self.scanner.get_line_number()) + ': ' + error)
