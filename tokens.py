from enum import Enum


class Tokens(Enum):
    PLUS_EQUAL = '+='
    PLUS_SIGN = '+'
    EQUAL_SIGN = 3
    EQUAL_EQUAL = 4
    OPEN_PARENTHESES = 5
    CLOSE_PARENTHESES = 6
    OPEN_BRACKET = 7
    CLOSE_BRACKET = 8
    DOUBLE_AND = 9
    PUBLIC = 10
    EOF = 11
    CLASS = 12
    VOID = 'void'
    MAIN = 13
    EXTENDS = 14
    STATIC = 15
    SEMICOLON = 16
    RETURN = 17
    COLON = 18
    BOOLEAN = 19
    INT = 20
    IF = 21
    ELSE = 22
    FOR = 23
    WHILE = 24
    SYSOUT = 25
    MINUS_SIGN = 26
    MULTI_SIGN = 27
    DOT = 28
    LESS = 29
    IDENTIFIER = 30
    INTEGER = 31
    TRUE = 'true'
    FALSE = 'false'