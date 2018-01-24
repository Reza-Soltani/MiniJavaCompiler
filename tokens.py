from enum import Enum


class Tokens(Enum):
    PLUS_EQUAL = '+='
    PLUS_SIGN = '+'
    EQUAL_SIGN = '='
    EQUAL_EQUAL = '=='
    OPEN_PARENTHESES = '('
    CLOSE_PARENTHESES = ')'
    OPEN_BRACKET = '{'
    CLOSE_BRACKET = '}'
    DOUBLE_AND = '&&'
    PUBLIC = 'public'
    EOF = 'EOF'
    CLASS = "class"
    VOID = 'void'
    MAIN = 'main'
    EXTENDS = 'extends'
    STATIC = 'static'
    SEMICOLON = ';'
    RETURN = 'return'
    COLON = ','
    BOOLEAN = 'boolean'
    INT = 'int'
    IF = 'if'
    ELSE = 'else'
    FOR = 'for'
    WHILE = 'while'
    SYSOUT = 'System.out.println'
    MINUS_SIGN = '-'
    MULTI_SIGN = '*'
    DOT = '.'
    LESS = '<'
    IDENTIFIER = 'identifier'
    INTEGER = 'integer'
    TRUE = 'true'
    FALSE = 'false'