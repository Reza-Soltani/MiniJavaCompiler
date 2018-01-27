from enum import Enum


class ErrorType(Enum):
    Semantic = 'SEMANTIC'
    Pars = 'PARS'


class Commands(Enum):
    ADD = 'ADD'
    SUB = 'SUB'
    AND = 'AND'
    ASSIGN = 'ASSIGN'
    EQ = 'EQ'
    JPF = 'JPF'
    JP = 'JP'
    LT = 'LT'
    MULT = 'MULT'
    NOT = 'NOT'
    PRINT = 'PRINT'


class VariableType(Enum):
    BOOLEAN = "BOOLEAN"
    INT = "INT"
    CLASS = "CLASS"
    METHOD = "METHOD"
    NONE = "NONE"
