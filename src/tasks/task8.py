import math_util as math_util
from random import choice
from copy import deepcopy
from math import cos, sin, pi

def draw_graph(graph:dict):
    g = r"""   
    \begin{center}
    \begin{tikzpicture}[
    every node/.style={circle, draw, fill=white, minimum size=1cm, align=center},
    node distance=2cm and 2cm,
        ->,                          % Ориентированные рёбра
        >=latex,                     % Стиль стрелок (можно использовать 'stealth' для острых)
        line width=1.2pt,            % Толщина линий
        every edge/.style={          % Стиль всех рёбер
            draw, 
            ->,
            line width=1.2pt,        % Толщина стрелок
            >=stealth,               % Стиль наконечника
            shorten >=2pt,           % Укорачивание стрелки
            shorten <=2pt
        }  
    >=stealth,
    use positioning/.style={right=of #1}  
    ]
    \node (0) {A};
    \node[below=of 0] (4) {E};
    \node[below=of 4] (8) {I};
    \node[below=of 8] (12) {M};
    """

    for x1 in range(1, 4):
        g += fr"\node[right = of {x1-1}] ({x1}) {{{chr(x1+65)}}};" + "\n"
        x2 = x1 + 4
        g += fr"\node[right = of {x2-1}] ({x2}) {{{chr(x2+65)}}};" + "\n"
        x3 = x2 + 4
        g += fr"\node[right = of {x3-1}] ({x3}) {{{chr(x3+65)}}};" + "\n"
        x4 = x3 + 4
        g += fr"\node[right = of {x4-1}] ({x4}) {{{chr(x4+65)}}};" + "\n"
    
    for vertex in graph.keys():
        for neighbourhood_vertex in graph[vertex]:
                g += fr"\draw[->] ({ord(vertex)-65}) -- ({ord(neighbourhood_vertex)-65});" + "\n" 

    g += r"""
    \end{tikzpicture} 
    \end{center}
    """

    return g

def draw_graph_with_labels(graph:dict, ret_time:list, KSS: list):
    g = r"""   
    \begin{center}
    \begin{tikzpicture}[
    every node/.style={circle, draw, fill=white, minimum size=1cm, align=center},
    node distance=2cm and 2cm,
        ->,                          % Ориентированные рёбра
        >=latex,                     % Стиль стрелок (можно использовать 'stealth' для острых)
        line width=1.2pt,            % Толщина линий
        every edge/.style={          % Стиль всех рёбер
            draw, 
            ->,
            line width=1.2pt,        % Толщина стрелок
            >=stealth,               % Стиль наконечника
            shorten >=2pt,           % Укорачивание стрелки
            shorten <=2pt
        }  
    >=stealth,
    use positioning/.style={right=of #1}  
    ]
    """

    colors = ['red', 'green', 'blue', 'cyan', 'magenta', 
              'yellow', 'gray', 'brown', 'lime', 'olive', 'orange', 'pink', 
              'purple', 'lightgray', 'teal', 'violet', 'black', 'white', 'darkgray']

    vertex_colors = dict()
    
    for node in graph.keys():
        vertex_colors[node] = 'white!100'

    for i in range(len(KSS)):
        for node in KSS[i]:
            vertex_colors[node] = colors[i]


    if 'A' in ret_time:
        g += fr"\node[fill={{{vertex_colors['A']}}}] (0) {{ A \\${ret_time.index('A')}$ }};" + "\n"
    else:
        g += fr"\node (0) {{ A \\ ? }};" + "\n"

    if 'E' in ret_time:
        g += fr"\node[fill={{{vertex_colors['E']}}}, below=of 0] (4) {{ E \\${ret_time.index('E')}$ }};" + "\n"
    else:
        g += fr"\node[below=of 0] (4) {{ E \\ ? }};" + "\n" 

    if 'I' in ret_time:
        g += fr"\node[fill={{{vertex_colors['I']}}}, below=of 4] (8) {{ I \\${ret_time.index('I')}$ }};" + "\n"
    else:
        g += fr"\node[below=of 4] (8) {{ I \\ ? }};" + "\n" 

    if 'M' in ret_time:
        g += fr"\node[fill={{{vertex_colors['M']}}}, below=of 8] (12) {{ M \\${ret_time.index('M')}$ }};" + "\n"
    else:
        g += fr"\node[below=of 8] (12) {{ M \\ ? }};" + "\n"      

    for x1 in range(1, 4):
        if chr(x1+65) in ret_time:
            g += fr"\node[fill={{{vertex_colors[chr(x1+65)]}}}, right = of {x1-1}] ({x1}) {{ {chr(x1+65)} \\${ret_time.index(chr(x1+65))}$ }};" + "\n"
        else:
            g += fr"\node[right = of {x1-1}] ({x1}) {{ {chr(x1+65)} \\${"?"}$ }};" + "\n"
        x2 = x1 + 4
        if chr(x2+65) in ret_time:
            g += fr"\node[fill={{{vertex_colors[chr(x2+65)]}}}, right = of {x2-1}] ({x2}) {{ {chr(x2+65)} \\${ret_time.index(chr(x2+65))}$ }};" + "\n"
        else:
            g += fr"\node[right = of {x2-1}] ({x2}) {{ {chr(x2+65)} \\${"?"}$ }};" + "\n"
        x3 = x2 + 4
        if chr(x3+65) in ret_time:
            g += fr"\node[fill={{{vertex_colors[chr(x3+65)]}}}, right = of {x3-1}] ({x3}) {{ {chr(x3+65)} \\${ret_time.index(chr(x3+65))}$ }};" + "\n"
        else:
            g += fr"\node[right = of {x3-1}] ({x3}) {{ {chr(x3+65)} \\${"?"}$ }};" + "\n"
        x4 = x3 + 4
        if chr(x4+65) in ret_time:
            g += fr"\node[fill={{{vertex_colors[chr(x4+65)]}}}, right = of {x4-1}] ({x4}) {{ {chr(x4+65)} \\${ret_time.index(chr(x4+65))}$ }};" + "\n"
        else:
            g += fr"\node[right = of {x4-1}] ({x4}) {{ {chr(x4+65)} \\${"?"}$ }};" + "\n"

    
    for vertex in graph.keys():
        for neighbourhood_vertex in graph[vertex]:
                g += fr"\draw[->] ({ord(vertex)-65}) -- ({ord(neighbourhood_vertex)-65});" + "\n" 

    g += r"""
    \end{tikzpicture} 
    \end{center}
    """

    return g


def dfs(graph:dict, node, visited_nodes, ret_time):
     
    visited_nodes.append(node)

    for neighbor in graph[node]:
        if neighbor not in visited_nodes:
            dfs(graph, neighbor, visited_nodes, ret_time)

    ret_time.append(node)


def draw_cond_graph(adjacency_list: dict):
    vertices = list(adjacency_list.keys())
    n = len(vertices)
    
    colors = ['red', 'green', 'blue', 'cyan', 'magenta', 
              'yellow', 'gray', 'brown', 'lime', 'olive', 'orange', 'pink', 
              'purple', 'lightgray', 'teal', 'violet', 'black', 'white', 'darkgray']
    
    tikz_code = r"""
    \begin{tikzpicture}[
        every node/.style={circle, draw, minimum size=1cm},
        every edge/.style={draw, ->, >=stealth},
        node distance=1.5cm,
        every loop/.style={looseness=8}
    ]
    """
    
    # Размещаем вершины по кругу и раскрашиваем
    for i, vertex in enumerate(vertices):
        angle = 2 * pi * i / n
        x = 5 * cos(angle)
        y = 5 * sin(angle)
        color = colors[i % len(colors)]  # Циклически используем цвета
        tikz_code += f"\\node[fill={color}] ({vertex}) at ({x:.2f},{y:.2f}) {{{vertex}}};\n"
    
    # Рисуем рёбра без подписей
    for src, targets in adjacency_list.items():
        for tgt in targets:
            if src == tgt:  # Петля
                tikz_code += fr"\draw[->] ({src}) edge[loop] ();"
            else:
                tikz_code += fr"\draw[->] ({src}) to ({tgt});"
    
    tikz_code += r"\end{tikzpicture}"
    return tikz_code

def kosaradgu(graph:dict, solution):

    visited_nodes = []
    ret_time = []

    nodes = list(graph.keys())

    solution.append(r"\textbf{1)}Начнем выполнение обхода в глубину с записью времени выхода вершин. "
    r"Инициализируем списки посещеных вершин и тех, которые ещё требуется посетить:\\"
    fr"Посещеные вершины - {" ".join(visited_nodes)}\\ Не посещёные вершины - {" ".join(nodes)}\\"
    r"Изобразим граф, записав под каждой вершиной время выхода (изначально неизвесто):\\")

    solution.append(draw_graph_with_labels(graph, ret_time, []))

    while len(visited_nodes) != len(nodes):
        unvisited_nodes = list(set(nodes).difference(set(visited_nodes)))
        node = choice(unvisited_nodes)
        solution.append(fr"Посещеные вершины - {" ".join(visited_nodes)}\\ Не посещёные вершины - {" ".join(unvisited_nodes)}\\"
        fr"Выберем случайную вершину из не посещёных - {node}. \\Запустим из нее обход в глубину с записью времени выхода:")
        dfs(graph, node, visited_nodes, ret_time)

        solution.append(draw_graph_with_labels(graph, ret_time, []))

    solution.append(r"\textbf{Были посещены все вершины, обход завершен.\\\\}"
                    r"\textbf{2)}Инвертируем граф:")
    
    inv_graph = dict()
    
    for node in nodes:
        for neighbor in graph[node]:
            if neighbor in inv_graph.keys():
                inv_graph[neighbor].append(node)
            else:
                inv_graph[neighbor] = [node]
        if node not in inv_graph.keys():
            inv_graph[node] = []
            

    solution.append(draw_graph(inv_graph))

    solution.append(r"\textbf{3)}Запустим поиск в глубину в инвертированном графе, начиная с вершин больших номеров.")

    visited_nodes_inv = []
    KSS = []
    ret_time_copy = deepcopy(ret_time)

    while (len(visited_nodes_inv) != len(nodes)):

        node = ret_time[-1]

        solution.append(fr"Необработанные вершины: {" ".join(list(set(nodes).difference(set(visited_nodes_inv))))} \\"
                        fr"Вершина с наибольшим номером среди не обработанных - {node} \\"
                        r"Запустим из этой вершины поиск в глубину. Закрасим все достижимые вершины одним цветом"
                        r" они будут компонентой сильной связности:\\" )

        component = []

        dfs(inv_graph, node, visited_nodes_inv, component)

        KSS.append(component)

        solution.append(draw_graph_with_labels(inv_graph, ret_time_copy, KSS))

        for _ in range(len(component)):
            del ret_time[-1]

    solution.append(r"\textbf{Были посещены все вершины, обход завершен.\\\\}"
                    r"\textbf{4)}Вершины, раскрашенные одним цветом - компоненты сильной связности:\\")
    
    for component in KSS:
        solution.append(fr"{" ".join(component)}\\")

    nodes_with_component = []
    for node in nodes:
        for i in range(len(KSS)):
            if node in KSS[i]:
                nodes_with_component.append((node, i))

    cond_graph = dict()

    for i in range(len(KSS)):
        cond_graph[i] = []

    for i in range(len(KSS)):
        for node in KSS[i]:
            for neighbor in graph[node]:
                if neighbor not in KSS[i]:
                    for elem in nodes_with_component:
                        if elem[0] == neighbor and elem[1] not in cond_graph[i]:
                            cond_graph[i].append(elem[1])

    solution.append(r"\\\textbf{Посик компонент сильной связности завершен. Построим граф конденсации:\\}")

    solution.append(draw_cond_graph(cond_graph))


def solve(graph: dict):

    solution = []
    solution.append("При помощи агоритма Kosaraju найдите компоненты сильной связности данного графа: \\")
    solution.append(draw_graph(graph))
    solution.append("Постройте граф конденсации.\\\\")

    solution.append(r"\textbf{Решение.}\\")
    solution.append(
    r"Для нахождения компонент сильной связности воспользуемся алгоритмом Косараджу:\\"
    r"\fbox{Alg} \textit{Алгоритм Косараджу}."
    r"""
    \begin{algorithm}
    \caption{Алгоритм Косараджу}\label{alg:Kosaraju}
    \begin{algorithmic}[1]
    \Statex \textbf{Вход}: Ориентированный граф $G = (V, E)$
    \Statex \textbf{Выход}: Компоненты сильной связности (КСС) графа $G$
    
    \State Выполнить поиск в глубину (DFS) на $G$, запоминая время выхода вершин
    \State Построить инвертированный граф $G^T = (V, E^T)$, где $E^T = \{(v,u) \mid (u,v) \in E\}$
    \State Выполнить серию DFS на $G^T$ в порядке убывания времени выхода
    \State Каждое дерево обхода в шаге 3 — одна КСС
    \State \Return Найденные КСС
    \end{algorithmic}
    \end{algorithm}
    \\
    """
    )

    solution.append(r"textbf{Пристутим к выполнению алгоритма:}\\")

    kosaradgu(graph, solution)



    return "\n".join(solution)
