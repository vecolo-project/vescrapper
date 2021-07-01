import sys

import ply.lex as lex

from ply4ever.parse import evalInst
from ply4ever.genereTreeGraphviz import printTreeGraph

reserved = {
    'GET': 'GET',
    'OF': 'OF',
    'WITH': 'WITH',
    'FROM': 'FROM',
    'OR': 'OR',
    'AND': 'AND'
}

tokens = [
             'ENTITY',
             'NUMBER', 'MINUS', 'CHARS',
             'PLUS', 'TIMES', 'DIVIDE',
             'LPAREN', 'RPAREN',
             "EQUALS", "NAME", "SEMI", "COMA",
             "GREATER", "LOWER"
         ] + list(reserved.values())

# Tokens
t_CHARS = r'"((?!").)*"'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SEMI = r';'
t_COMA = r','
t_EQUALS = r'='
t_GREATER = r'>'
t_LOWER = r'<'


def t_ENTITY(t):
    r"""image|text"""
    return t


def t_NAME(t):
    r"""\*|[a-zA-Z_][a-zA-Z0-9_]*"""
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
    ('nonassoc', 'EQUALS', 'LOWER', 'GREATER'),
    ('left', 'AND', 'OR'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)


def p_start(p):
    """start : statement"""
    p[0] = p[1]
    print(p[0])
    printTreeGraph(p[0])
    # evalInst(p[1])


def p_statement(p):
    """statement : GET ENTITIES OF NAMES FROM NAMES WITH CONDITIONS SEMI"""
    p[0] = ('GET', ('ENTITIES', p[2]), ('OF', p[4]), ('FROM', p[6]), ('CONDITIONS', p[8]))

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
        p[0] = ('names', 'empty', p[1])
    else:
        p[0] = ('names', p[1], p[3])


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
                yacc.parse(file.read())


def cli(yacc):
    while True:
        s = input('cmd (type exit(); to leave) > ')
        if s == "exit();":
            print("Bye bye !")
            return
        yacc.parse(s)
