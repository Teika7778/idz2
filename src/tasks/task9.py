import math_util as math_util


def solve(nums: list, graph: dict):
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
                g += fr"\draw ({vertex}) -- ({neighbourhood_vertex});" + "\n"
                edges.append((vertex, neighbourhood_vertex))


    g += r"""
    \end{tikzpicture}
    \end{center}
    """
    solution.append(g)
    return "\n".join(solution)