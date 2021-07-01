import sys

import ply.lex as lex

from ply4ever.parse import evalInst
from ply4ever.genereTreeGraphviz import printTreeGraph

reserved = {
    'GET': 'GET'
}

tokens = [
             'ENTITY',
             'NUMBER', 'MINUS', 'CHARS',
             'PLUS', 'TIMES', 'DIVIDE',
             'LPAREN', 'RPAREN',
             'AND', 'OR', "EQUALS", "NAME", "SEMI", "COMA",
             "GREATER", "LOWER"
         ] + list(reserved.values())

# Tokens
t_CHARS = r'".+"'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_AND = r'&'
t_OR = r'\|'
t_SEMI = r';'
t_COMA = r','
t_EQUALS = r'='
t_GREATER = r'>'
t_LOWER = r'<'


def t_ENTITY(t):
    r"""image|text"""
    return t


def t_NAME(t):
    r"""[a-zA-Z_][a-zA-Z0-9_]*"""
    t.type = reserved.get(t.value, "NAME")
    return t


def t_NUMBER(t):
    r"""\d+"""
    t.value = int(t.value)
    return t


def p_expression_number(p):
    """expression : NUMBER"""
    p[0] = p[1]


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
    ('nonassoc', 'AND', 'OR'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS'),
)


def p_start(p):
    """start : statement"""
    # p[0] = p[1]
    print(p[0])
    printTreeGraph(p[0])
    # evalInst(p[1])


def p_entities(p):
    """ENTITIES : ENTITY
    | ENTITIES COMA ENTITY"""
    if len(p) == 2:
        p[0] = ('entity', p[1], 'empty')
    else:
        p[0] = ('entity', p[1], p[3])


def p_statement(p):
    """statement : GET ENTITIES"""
    p[0] = ('GET', p[2], 'empty')


# def p_expression_binop(p):
#     """expression : expression PLUS expression
#                 | expression TIMES expression
#                 | expression MINUS expression
#                 | expression DIVIDE expression
#                 | expression AND expression
#                 | expression OR expression
#                 | expression GREATER expression
#                 | expression LOWER expression
#                 | expression EQUALS expression"""
#     p[0] = (p[2], p[1], p[3])
#
#
def p_expr_uminus(p):
    """expression : MINUS expression %prec UMINUS"""
    p[0] = -p[2]


#
# def p_expression_group(p):
#     """expression : LPAREN expression RPAREN"""
#     p[0] = p[2]
#
#


def p_error(p):
    print("Syntax error at '%s'" % p.value)


# import ply.yacc as yacc
#
# yacc.yacc()


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
