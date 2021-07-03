import sys

import ply.lex as lex

from ply4ever.parse import evalScrap
from ply4ever.genereTreeGraphviz import printTreeGraph

showTree = False
reserved = {
    'GET': 'GET',
    'OF': 'OF',
    'WITH': 'WITH',
    'FROM': 'FROM',
    'OR': 'OR',
    'LIMIT': 'LIMIT',
    'AND': 'AND'
}

tokens = [
             'ENTITY',
             'NUMBER', 'CHARS',
             'LPAREN', 'RPAREN',
             "NAME", "SEMI", "COMA"
         ] + list(reserved.values())

# Tokens
t_CHARS = r'"((?!").)*"'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SEMI = r';'
t_COMA = r','


def t_ENTITY(t):
    r"""image|text"""
    return t


def t_NAME(t):
    r"""\*|[a-zA-Z_][a-zA-Z0-9_-]*"""
    t.type = reserved.get(t.value, "NAME")
    return t


def t_NUMBER(t):
    r"""\d+"""
    t.value = int(t.value)
    return t


# Ignored characters
t_ignore = " \t\n\r"


def t_newline(t):
    r"""\n+"""
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer

lex.lex()

precedence = (
    ('left', 'AND', 'OR'),
)


def p_start(p):
    """start : statement"""
    p[0] = p[1]
    if showTree:
        print(p[0])
        printTreeGraph(p[0])
    evalScrap(p[0])


def p_statement(p):
    """statement : GET ENTITIES OF NAMES FROM NAME WITH CONDITIONS LIMIT NUMBER SEMI
    | GET ENTITIES OF NAMES FROM NAME WITH CONDITIONS SEMI
    | GET ENTITIES OF NAMES FROM NAME LIMIT NUMBER SEMI
    | GET ENTITIES OF NAMES FROM NAME SEMI"""
    if len(p) == 12:
        p[0] = ('GET',
                ('ENTITIES', p[2]),
                ('OF', p[4]),
                ('FROM', p[6]),
                ('CONDITIONS', p[8]),
                ('LIMIT', p[10]))
    elif len(p) == 10:
        p[0] = ('GET',
                ('ENTITIES', p[2]),
                ('OF', p[4]),
                ('FROM', p[6]),
                ('LIMIT' if type(p[8]) is int else 'CONDITIONS', p[8]))
    else:
        p[0] = ('GET',
                ('ENTITIES', p[2]),
                ('OF', p[4]),
                ('FROM', p[6]))


def p_entities(p):
    """ENTITIES : ENTITY
    | ENTITIES COMA ENTITY"""
    if len(p) == 2:
        p[0] = ('entity', 'empty', p[1])
    else:
        p[0] = ('entity', p[1], p[3])


def p_names(p):
    """NAMES : NAME
    | NAMES COMA NAME"""
    if len(p) == 2:
        p[0] = ('name', 'empty', p[1])
    else:
        p[0] = ('name', p[1], p[3])


def p_condition(p):
    """CONDITION : CHARS"""
    p[0] = p[1].strip('"')


def p_condition_group(p):
    """CONDITIONS : LPAREN CONDITIONS RPAREN"""
    p[0] = p[2]


def p_condition_binop(p):
    """CONDITIONS : CONDITION
    | CONDITIONS OR CONDITIONS
    | CONDITIONS AND CONDITIONS"""
    if len(p) == 4:
        p[0] = (p[2], p[1], p[3])
    else:
        p[0] = p[1]


def p_error(p):
    print("Syntax error at '%s'" % p.value)


def load_files(yacc):
    if len(sys.argv) >= 2:
        for i in range(1, len(sys.argv)):
            with open(sys.argv[i], 'r') as file:
                content = file.read()
                print("Vescrapper reading :", content)
                yacc.parse(content)


def cli(yacc):
    global showTree
    while True:
        s = input('cmd > ')
        if s == "exit();":
            print("Bye bye !")
            return
        if s == "debugOn();":
            showTree = True
            print("Debug ON !")
        if s == "debugOff();":
            showTree = False
            print("Debug OFF !")
        yacc.parse(s)
