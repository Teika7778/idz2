import math_util as math_util
from random import choice
from copy import deepcopy

def draw_graph(graph: dict, white_vertices: list, gray_vertices: list, black_vertices: list) -> str:
    """Функция для отрисовки графа с раскраской вершин
    
    Args:
        graph: полный список смежностей графа
        white_vertices: список белых вершин (не посещенных)
        gray_vertices: список серых вершин (в очереди)
        black_vertices: список черных вершин (обработанных)
    """
    g = r"""   
    \begin{center}
    \begin{tikzpicture}[
    every node/.style={circle, draw, minimum size=1cm, align=center},
    node distance=2cm and 2cm,  
    >=stealth,
    use positioning/.style={right=of #1}  
    ]
    """
    # Создаем словарь для быстрого определения цвета вершины
    vertex_colors = {}
    for v in white_vertices:
        vertex_colors[v] = "white"
    for v in gray_vertices:
        vertex_colors[v[0]] = "gray!60"
    for v in black_vertices:
        vertex_colors[v[0]] = "black!70"

    

    # Отрисовываем все вершины с соответствующими цветами
    # Вершина 1
    color = vertex_colors.get(1, "white")
    sign = '?' 
    if color == "gray!60":
        for elem in gray_vertices:
            if elem[0] == 1: sign = elem[1]
    if color == "black!70":
        for elem in black_vertices:
            if elem[0] == 1: sign = elem[1]
    g += fr"\node[fill={color}] (0) {{{1}\\${sign}$}};" + "\n"
    
    # Вершина 6
    color = vertex_colors.get(6, "white")
    sign = '?' 
    if color == "gray!60":
        for elem in gray_vertices:
            if elem[0] == 6: sign = elem[1]
    if color == "black!70":
        for elem in black_vertices:
            if elem[0] == 6: sign = elem[1]
    g += fr"\node[below=of 0, fill={color}] (5) {{{6}\\${sign}$}};" + "\n"
    
    # Вершины 2-5 и 7-10
    for x in range(1, 5):
        vertex_num = x + 1
        color = vertex_colors.get(vertex_num, "white")
        sign = '?' 
        if color == "gray!60":
            for elem in gray_vertices:
                if elem[0] == x+1: sign = elem[1]
        if color == "black!70":
            for elem in black_vertices:
                if elem[0] == x+1: sign = elem[1]
        g += fr"\node[right = of {x-1}, fill={color}] ({x}) {{{vertex_num}\\${sign}$}};" + "\n"
        
        y = x + 5
        vertex_num = y + 1
        color = vertex_colors.get(vertex_num, "white")
        sign = '?' 
        if color == "gray!60":
            for elem in gray_vertices:
                if elem[0] == y+1: sign = elem[1]
        if color == "black!70":
            for elem in black_vertices:
                if elem[0] == y+1: sign = elem[1]
        g += fr"\node[right = of {y - 1}, fill={color}] ({y}) {{{vertex_num}\\${sign}$}};" + "\n"

    # Отрисовка ребер из полного списка смежностей
    for v in graph.keys():
        for neighbour in graph[v]:
            if v < neighbour:  # Чтобы не дублировать ребра
                g += fr"\draw ({v-1}) -- ({neighbour-1});" + "\n"

    g += r"""
    \end{tikzpicture}
    \end{center}
    """
    return g



def find_farthest_vertex(graph: dict, vertex: int):

    solution = [] # Сюда следует помещать графы, рисуемые на шагах алгоритма.

    new_graph = deepcopy(graph)

    visited_vertices = set() # Вершины снятые с очереди (черные)

    queue = [] # Вершины находящиеся в очереди (серые)


    max = (vertex, 0)

    queue.append((vertex, 0)) # Кладем в очередь изначальную вершину

    solution.append(draw_graph(graph, new_graph.keys(), queue, visited_vertices)) # Отрисовка

    while (len(visited_vertices) != len(list(graph.keys()))):

        

        top = queue.pop() # Снимаем вершину с очереди
        visited_vertices.add(top) # Красим в черный

        if max[1] < top[1]: # Максимальное расстояние
            max = top
        
        for neighbourhood_vertex in new_graph[top[0]]:
            queue.append((neighbourhood_vertex, top[1] + 1)) # Добавить в очередь всех детей
            top_index = new_graph[neighbourhood_vertex].index(top[0]) 
            visited_vertices.add((new_graph[neighbourhood_vertex].pop(top_index), top[1]))

        solution.append(draw_graph(graph, new_graph.keys(), queue, visited_vertices)) # Отрисовка

    return max, solution
            


def solve(graph: dict):
    solution = []
    mat = math_util.graph_to_adj_matrix(graph)
    # Формулировка задачи
    solution.append(
        fr"Найдите радиус, диаметр и центр данного дерева:.\\"
    )
    # Отрисовка Графа
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


    for vertex in graph.keys():
        for neighbourhood_vertex in graph[vertex]:
                g += fr"\draw ({vertex-1}) -- ({neighbourhood_vertex-1});" + "\n" 

    g += r"""
    \end{tikzpicture}
    \end{center}
    """
    solution.append(g)

    # Решение
    solution.append(r"\textbf{Решение.}")

    solution.append(
        r"Для решения задачи воспользуемся алгоритмом нахождения диметра дерева:\\"
        r"\fbox{Alg} \textit{Алгоритм нахождения диаметра дерева}."
        r"Предлагается такой псевдокод:"
        r"""
        \begin{algorithm}
        \caption{Алгоритм нахождения диаметра дерева}\label{alg:Example}
        \begin{algorithmic}
        \Statex $V$ - множество вершин дерева.\\
        1) $u$ - любая вершина.\\
        2) Найти наиболее удаленную от $u$ вершину $v$. Она будет первым концом диаметра.\\
        3) Найти наиболее удаденную от $v$ вершину $w$. Она будет вторым концом диаметра.\\
        \end{algorithmic}
        \end{algorithm}
        """
    )

    closed_graph = math_util.graph_closure(graph)

    random_vertex = choice(list(closed_graph.keys()))

    solution.append(
        r"Выберем случайную вершину:\\"
        rf"$$u = {random_vertex}$$"
        r"Для поиска наиболее удаленной вершины воспользуемся поиском в ширину, запомная расстояния до посещенных вершин:\\"
        )
    
    res = find_farthest_vertex(closed_graph, random_vertex)

    farthest_vertex = res[0]
    solution += res[1]
    
    return "\n".join(solution)