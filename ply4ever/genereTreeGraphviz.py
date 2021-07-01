import uuid

import graphviz as gv


def printTreeGraph(t):
    graph = gv.Digraph(format='pdf')
    graph.attr('node', shape='circle')
    addNode(graph, t)
    # graph.render(filename='img/graph') #Pour Sauvegarder
    graph.view()  # Pour afficher


def addNode(graph, t):
    myId = uuid.uuid4()

    if type(t) != tuple:
        graph.node(str(myId), label=str(t))
        return myId

    graph.node(str(myId), label=str(t[0]))
    for i in range(1, len(t)):
        graph.edge(str(myId), str(addNode(graph, t[i])), arrowsize='0')

    return myId
