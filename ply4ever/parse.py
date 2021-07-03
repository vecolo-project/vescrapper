from googlesearch import search

entities = []
of = []
source = ''
limit = -1
condition = ()


def evalScrap(t):
    global entities, of, source, limit, condition
    entities = evalTuple(t[1][1])
    of = evalTuple(t[2][1])
    source = evalSource(t[3][1])
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
    performSearch()


def evalSource(t):
    return '' if t == '*' else t


def evalTuple(t):
    if type(t[1]) is tuple:
        return [t[2]] + evalTuple(t[1])
    return [t[2]]


def performSearch():
    global entities, of, source, limit, condition
    query = generateQuery()
    print("Generated google search is ", query)
    for result in search(
            query,
            tld="fr",
            num=10 if limit == -1 else limit,
            stop=10 if limit == -1 else limit,
            pause=2):
        print(result)


def evalCondition(condition):
    if type(condition[1]) is tuple:
        return f'("{evalCondition(condition[1])}" {condition[0]} "{condition[2]}")'
    if type(condition) is str:
        return f'"{condition}"'
    return f'("{condition[1]}" {condition[0]} "{condition[2]}")'


def evalOf(of):
    return f'{"|".join(of)}'


def evalEntities():
    global entities
    if 'image' in entities:
        if len(entities) == 1:
            return '("jpeg"|"jpg"|"png"|"gif")'
        else:
            return '("jpeg"|"jpg"|"png"|"gif"|"")'
    else:
        return ''


def generateQuery():
    global of, source, condition
    q = evalEntities()
    if len(condition) > 0:
        q += f'&{evalCondition(condition)}'
    if len(source) > 0:
        q += f' site:{source}.*'
    q += f' intitle:{evalOf(of)}'
    return q
