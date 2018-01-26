from enum import Enum


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


class VaribaleType(Enum):
    BOOLEAN = "BOOLEAN"
    INT = "INT"
    CLASS = "CLASS"
    METHOD = "METHOD"
    NONE = "NONE"
