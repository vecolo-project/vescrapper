from googlesearch import search

entities = []
of = []
source = []
limit = -1
condition = ()


def evalScrap(t):
    global entities, of, source, limit, condition
    entities = evalTuple(t[1][1])
    of = evalTuple(t[2][1])
    source = [] if t[3][1] == '*' else [t[3][1]]
    if len(t) == 5:
        if t[4][0] == 'CONDITIONS':
            condition = t[4][1]
            limit = -1
        else:
            limit = t[4][1]
            condition = ()
    elif len(t) == 6:
        condition = t[4][1]
        limit = t[5][1]
    else:
        condition = ()
        limit = -1
    print('ok')


def evalTuple(t):
    if type(t[1]) is tuple:
        return [t[2]] + evalTuple(t[1])
    return [t[2]]


def evalExpr(t):
    if type(t) is not tuple:
        return t
    if t[0] == '&':
        return evalExpr(t[1]) and evalExpr(t[2])
    if t[0] == '|':
        return evalExpr(t[1]) or evalExpr(t[2])
    raise ValueError("Can't parse this ", t)
