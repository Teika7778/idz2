import math_util as math_util
from copy import deepcopy


def find_farthest_vertex(graph: dict, vertex: int):

    new_graph = math_util.graph_closure(graph)

    visited_vertices = deepcopy(list(new_graph.keys()))
    queue = []

    max = (vertex, 0)

    queue.append((vertex, 0))

    while (len(visited_vertices) != 0):

        top = queue.pop()
        visited_vertices.remove(top[0])

        if max[1] < top[1]:
            max = top
        for neighbourhood_vertex in new_graph[top[0]]:
            queue.append((neighbourhood_vertex, top[1] + 1))
            new_graph[neighbourhood_vertex].remove(top[0])

    return max
            


def solve(graph: dict):
    solution = []
    mat = math_util.graph_to_adj_matrix(graph)
    solution.append(" Дан граф:")
    g = r"""
    \begin{center}
    \begin{tikzpicture}[
    every node/.style={circle, draw, fill=white, minimum size=1cm},
    node distance=2cm and 2cm,  
    >=stealth,
    use positioning/.style={right=of #1}  
    ]
    \node (0) {1};
    \node[below=of 0] (5) {6};
    """
    for x in range(1, 5):
        g += fr"\node[right = of {x-1}] ({x}) {{{x+1}}};" + "\n"
        y = x + 5
        g += fr"\node[right = of {y - 1}] ({y}) {{{y + 1}}};" + "\n"

    
    edges = []

    for vertex in graph.keys():
        for neighbourhood_vertex in graph[vertex]:
            if (vertex, neighbourhood_vertex) not in edges and (neighbourhood_vertex, vertex) not in edges:
                g += fr"\draw ({vertex-1}) -- ({neighbourhood_vertex-1});" + "\n"
                edges.append((vertex, neighbourhood_vertex))

    print(find_farthest_vertex(graph, 1))

    print(find_farthest_vertex(graph, 3))

    print(find_farthest_vertex(graph, 10))

    print(find_farthest_vertex(graph, 7))


    g += r"""
    \end{tikzpicture}
    \end{center}
    """
    solution.append(g)
    return "\n".join(solution)