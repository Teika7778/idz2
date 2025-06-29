import math_util as math_util
from random import choice
from copy import deepcopy

def draw_graph(graph: dict, white_vertices: list, gray_vertices: list, black_vertices: list) -> str:
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
    vertex_signs = {}
    for v in white_vertices:
        vertex_colors[v] = "white"
        vertex_signs[v] = '?'
    for v in gray_vertices:
        vertex_colors[v[0]] = "gray!60"
        vertex_signs[v[0]] = v[1]
    for v in black_vertices:
        vertex_colors[v[0]] = "black!60"
        vertex_signs[v[0]] = v[1]

    

    # Отрисовываем все вершины с соответствующими цветами
    # Вершина 1
    color = vertex_colors.get(1, "white")
    sign = vertex_signs.get(1, '?')
    g += fr"\node[fill={color}] (0) {{{1}\\${sign}$}};" + "\n"
    
    # Вершина 6
    color = vertex_colors.get(6, "white")
    sign = vertex_signs.get(6, '?')
    g += fr"\node[below=of 0, fill={color}] (5) {{{6}\\${sign}$}};" + "\n"
    
    # Вершины 2-5 и 7-10
    for x in range(1, 5):
        vertex_num = x + 1
        color = vertex_colors.get(vertex_num, "white")
        sign = vertex_signs.get(vertex_num, '?')
        g += fr"\node[right = of {x-1}, fill={color}] ({x}) {{{vertex_num}\\${sign}$}};" + "\n"
        
        y = x + 5
        vertex_num = y + 1
        color = vertex_colors.get(vertex_num, "white")
        sign = vertex_signs.get(vertex_num, '?')
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

    solution.append(fr"Начнем обход из вершины {vertex}, будем считать расстояние до неё равное 0:\\")

    queue.append((vertex, 0)) # Кладем в очередь изначальную вершину

    solution.append(draw_graph(graph, new_graph.keys(), queue, visited_vertices)) # Отрисовка

    while (len(visited_vertices) != len(list(graph.keys()))):

        

        top = queue.pop(0) # Снимаем вершину с очереди
        visited_vertices.add(top) # Красим в черный

        if max[1] < top[1]: # Максимальное расстояние
            max = top

        if len(new_graph[top[0]]) >= 2:
            solution.append(fr"Посетим белых сосдей вершины {top[0]}, это вершины: ")
        elif len(new_graph[top[0]]) == 1:
            solution.append(fr"Посетим белого соседа вершины {top[0]}, это вершина: ")
        else:
            solution.append(fr"У вершины {top[0]} нет соседей.")
        for neighbourhood_vertex in new_graph[top[0]]:
            queue.append((neighbourhood_vertex, top[1] + 1)) # Добавить в очередь всех детей
            solution.append(fr"{neighbourhood_vertex}   ")
            top_index = new_graph[neighbourhood_vertex].index(top[0]) 
            visited_vertices.add((new_graph[neighbourhood_vertex].pop(top_index), top[1]))

        solution.append(fr"\\")
        if len(new_graph[top[0]]) >= 2:
            solution.append(fr"Запишем под ними обновленное расстояние: {top[1]+1}\\")
        elif len(new_graph[top[0]]) == 1:
            solution.append(fr"Запишем под ней обновленное расстояние: {top[1]+1}\\")

        solution.append(fr"Закрасим вершину {top[0]} в черный.\\")


        solution.append(draw_graph(graph, new_graph.keys(), queue, visited_vertices)) # Отрисовка

    solution.append(fr"Обход дерева окончен. Посещены все вершины.\\")

    solution.append(fr"Наиболее удаленных вершин может быть несколько, выберем любую их них. "
    fr"Наиболее удаленная от изначальной вершины {vertex} - это вершина {max[0]}. \\")

    return max, solution




def draw_diameter(graph: dict, diameter: dict, draw_center=False) -> str:
    g = r"""   
    \begin{center}
    \begin{tikzpicture}[
    every node/.style={circle, draw, minimum size=1cm, align=center},
    node distance=2cm and 2cm,  
    >=stealth,
    use positioning/.style={right=of #1}  
    ]
    """

    if not draw_center:
        # Отрисовываем все вершины с соответствующими цветами
        # Вершина 1
        color = "red" if 1 in list(diameter.keys()) else "white"
        g += fr"\node[fill={color}] (0) {{{1}}};" + "\n"

        # Вершина 6
        color = "red" if 6 in list(diameter.keys()) else "white"
        g += fr"\node[below=of 0, fill={color}] (5) {{{6}}};" + "\n"

        # Вершины 2-5 и 7-10
        for x in range(1, 5):
            vertex_num = x + 1
            color = "red" if x+1 in list(diameter.keys()) else "white"
            g += fr"\node[right = of {x-1}, fill={color}] ({x}) {{{vertex_num}}};" + "\n"

            y = x + 5
            vertex_num = y + 1
            color = "red" if y+1 in list(diameter.keys()) else "white"
            g += fr"\node[right = of {y - 1}, fill={color}] ({y}) {{{vertex_num}}};" + "\n"

    else:

        center = min(diameter.values())

        # Отрисовываем все вершины с соответствующими цветами
        # Вершина 1
        ex = diameter.get(1, '')
        color = 'blue' if ex == center else "red" if 1 in list(diameter.keys()) else "white"
        g += fr"\node[fill={color}] (0) {{{1}\\${ex}$}};" + "\n"

        # Вершина 6
        ex = diameter.get(6, '')
        color = 'blue' if ex == center else "red" if 6 in list(diameter.keys()) else "white"
        g += fr"\node[below=of 0, fill={color}] (5) {{{6}\\${ex}$}};" + "\n"

        # Вершины 2-5 и 7-10
        for x in range(1, 5):
            vertex_num = x + 1
            ex = diameter.get(x+1, '')
            color = 'blue' if ex == center else "red" if x+1 in list(diameter.keys()) else "white"
            g += fr"\node[right = of {x-1}, fill={color}] ({x}) {{{vertex_num}\\${ex}$}};" + "\n"

            y = x + 5
            vertex_num = y + 1
            ex = diameter.get(y+1, '')
            color = 'blue' if ex == center else "red" if y+1 in list(diameter.keys()) else "white"
            g += fr"\node[right = of {y - 1}, fill={color}] ({y}) {{{vertex_num}\\${ex}$}};" + "\n"

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



def find_diameter(graph: dict, first_diameter_end: int, second_diameter_end, draw_center=False):

    paths = []
    closed_paths = []

    solution = []

    new_graph = deepcopy(graph)

    visited_vertices = set() # Вершины снятые с очереди (черные)

    queue = [] # Вершины находящиеся в очереди (серые)

    max = (first_diameter_end, 0)

    queue.append((first_diameter_end, 0)) # Кладем в очередь изначальную вершину

    paths.append([first_diameter_end])

    while (len(visited_vertices) != len(list(graph.keys()))):

        top = queue.pop() # Снимаем вершину с очереди

        visited_vertices.add(top) # Красим в черный

        if max[1] < top[1]: # Максимальное расстояние
            max = top

        if len(new_graph[top[0]]) == 0:
            closed_paths.append(paths.pop())

        paths_copy = list(deepcopy(paths[-1]))


        for neighbourhood_vertex in new_graph[top[0]]:
            paths.append(paths_copy + [neighbourhood_vertex])
            queue.append((neighbourhood_vertex, top[1] + 1)) # Добавить в очередь всех детей
            top_index = new_graph[neighbourhood_vertex].index(top[0]) 
            visited_vertices.add((new_graph[neighbourhood_vertex].pop(top_index), top[1]))

    for path in closed_paths:
        if path[0] == first_diameter_end and path[-1] == second_diameter_end:
            diameter = dict()
            for vertex in path:
                diameter[vertex] = find_farthest_vertex(graph, vertex)[0][1]
            solution.append(draw_diameter(graph, diameter, draw_center))


    return solution
            


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
    solution.append(r"\textbf{Решение.}\\")

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
        fr"$$u = {random_vertex}$$"
        r"Для поиска наиболее удаленной вершины воспользуемся поиском в ширину"
        r", запомная расстояния до посещенных вершин (подпишем его под номером вершины):\\"
        )
    
    res1 = find_farthest_vertex(closed_graph, random_vertex)

    first_diameter_end = res1[0][0]
    solution += res1[1]

    solution.append(r"\\ \textbf{Был найден первый конец диаметра}. \\"
        fr"$$v = {first_diameter_end}$$"
        fr"\\Чтобы найти второй конец диаметра, нужно найти вершину, наиболее удаленную от {first_diameter_end}. "
        r"Алгоритм нахождения аналогичен.\\")

    res2 = find_farthest_vertex(closed_graph, first_diameter_end)

    second_diameter_end = res2[0][0]
    #solution += res2[1] #Второй раз не приводим алгоритм

    solution.append(fr"Наиболее удаленная от верлшины {first_diameter_end} - это вершина {second_diameter_end}. \\"
    fr"$$w = {second_diameter_end}$$")

    solution.append(r"\\ \textbf{Был найден второй конец диаметра, а значит сам диаметр.} \\"
                    fr"Это путь из вершины {first_diameter_end} в вершину {second_diameter_end}:\\")

    solution += find_diameter(closed_graph, first_diameter_end, second_diameter_end)

    solution.append(r"Для дальнейшего решения задачи докажем утверждение: \\\\"
                    r"\textbf{Утверждение.} Эксцентриситеты вершин дерева не могут быть меньше минимального эксцентриситета вершин диаметра.\\\\"
                    rf"Пусть $v$~--- вершина вне диаметра. Эксцентриситет $v$~--- наибольшее из расстояний до других вершин."
                    r"Найдем путь, соединяющий эту вершину с деревом."
                    rf"Тогда эксцентриситет вершины $v$ будет не меньше, чем сумма длины пути от $v$ до вершины $u$ диаметра и эксцентриситета вершины $u$."
                    r"Утверждение доказано.\\\\"
                    r"\textbf{Следствие.} Центры графа лежат на его диаметре. Чтобы найти центры графа, достаточно найти вершины диаметра с минимальным эксцентриситетом.\\\\"
                    r"Рассчитаем эксцентриситеты вершин диаметра, выделим минимальные из них, они и будут центром графа, а их эксцентриситет - радиусом:\\")
    

    solution += find_diameter(closed_graph, first_diameter_end, second_diameter_end, True)
    
    return "\n".join(solution)



