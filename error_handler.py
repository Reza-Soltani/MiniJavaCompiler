from constant import ErrorType
import sys


class ErrorHandler(Exception):

    def rasie_error(self, error_type, error):
        if error_type.value == ErrorType.Semantic.value:
            print(error)
            sys.exit()
        else:
            print(error)
