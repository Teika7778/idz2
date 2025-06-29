import math_util as math_util
from math import cos, sin, pi
from copy import deepcopy
from collections import defaultdict

def dfs(graph, edges, visited_edges, node, end, path, paths):

    path.append(node)

    if node == end:
        if  len(visited_edges) == len(edges):
            paths.append(path)
        return
    
    for neighbor in graph[node]:
        if (node[0] + neighbor) not in visited_edges:
            visited_edges.append(node[0]+neighbor)
            dfs(graph, edges, visited_edges, neighbor, end, deepcopy(path), paths)
            del visited_edges[visited_edges.index(node[0] + neighbor)]



def draw_de_bruijn_graph_clean_labels(adjacency_list):
    vertices = list(adjacency_list.keys())
    n = len(vertices)
    
    tikz_code = r"""
    \begin{tikzpicture}[
        every node/.style={circle, draw, fill=white, minimum size=8mm},
        every edge/.style={draw, ->, >=stealth},
        node distance=1.5cm,
        every loop/.style={looseness=8},
        edge node/.style={font=\small, inner sep=1pt, fill=none, draw=none}
    ]
    """
    # Размещаем вершины по кругу
    for i, vertex in enumerate(vertices):
        angle = 2 * pi * i / n
        x = 5 * cos(angle)
        y = 5 * sin(angle)
        tikz_code += f"\\node ({vertex}) at ({x:.2f},{y:.2f}) {{{vertex}}};\n"
    
    # Рисуем рёбра с чистыми текстовыми подписями
    for src, targets in adjacency_list.items():
        for tgt in targets:
            label = src[:2] + tgt[-1]
            if src == tgt:  # Обработка петель
                tikz_code += fr"""
                \draw[->] ({src}) edge[loop] node[edge node, pos=0.2, xshift=2pt] {{{label}}} ();"""
            else:
                tikz_code += fr"""
                \draw[->] ({src}) to node[edge node, pos=0.1, sloped, yshift=5pt] {{{label}}} ({tgt});"""
    
    tikz_code += r"\end{tikzpicture}"
    return tikz_code


def generate_transition_table(nodes, words, edges):
    # Начало LaTeX-таблицы
    table = r"""
    \begin{center}
    \begin{tabular}{|c|c|c|c|}
    \hline
    \textbf{Начало} & \textbf{Конец} & \textbf{Результат} & \textbf{Наличие} \\ 
    \hline
    """
    
    # Генерация строк таблицы
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            if nodes[i][-1] == nodes[j][0]:
                combined = nodes[i][0] + nodes[j]
                exists = "Да" if combined in words else "Нет"
                if combined in words: edges.append(combined)
                
                table += fr"{nodes[i]} & {nodes[j]} & {combined} & {exists} \\ \hline" + "\n"
    
    # Завершение таблицы
    table += r"""
    \end{tabular}
    \end{center}
    """
    return table


def generate_degree_table(adjacency_list):
    # Вычисляем степени вершин
    in_degree = defaultdict(int)
    out_degree = defaultdict(int)
    
    for src, neighbors in adjacency_list.items():
        out_degree[src] = len(neighbors)
        for tgt in neighbors:
            in_degree[tgt] += 1
    
    # Сортируем вершины для красивого отображения
    vertices = sorted(adjacency_list.keys())
    
    # Генерируем LaTeX-таблицу
    latex_table = r"""
    \begin{center}
    \begin{tabular}{|c|c|c|c|}
    \hline
    \textbf{Вершина} & \textbf{Входящая степень} & \textbf{Исходящая степень} & \textbf{Разница входящих и исходящих} \\ 
    \hline
    """

    degree_table = dict()
    
    for vertex in vertices:
        total_degree = in_degree[vertex] - out_degree[vertex]
        degree_table[vertex] = total_degree
        latex_table += fr"{vertex} & {in_degree[vertex]} & {out_degree[vertex]} & {total_degree} \\ \hline" + "\n"
    
    latex_table += r"""
    \end{tabular}
    \end{center}
    """
    return latex_table, degree_table


def solve(words: list):

    solution = []

    solution.append(
        fr"При помощи графа де Брюина найдите все слова наименьшей длины, которые содержат подстроки:\\"
        fr"{" ".join(words)}. \\ \\"
    )

    g = dict()

    for word in words:
        first_part = word[:2]
        second_part = word[1:]

        if second_part not in g.keys():
            g[second_part] = []

        if first_part in g.keys():
            g[first_part].append(second_part)
        else:
            g[first_part] = [second_part]

    # Решение
    solution.append(r"\textbf{Решение.}\\")

    solution.append(r"Для решения задачи граф де Брюина. "
            r"Для подсток длины 3 граф будет иметь:\\"
            r"Вершины - уникальные подстроки длины 2 \\"
            r"Ребра - переходы между подстроками.\\"
            r"Найдем уникальные подстроки разбием входных строк на всевозможные подстроки дллины 2:\\"  )
    solution.append(fr"Вершины: {" ".join(list(g.keys()))} \\")
    
    solution.append(r"Для того, чтобы найти ребра, переберем все все пары вершин, начинающиеся и заканчивающиеся одной буквой. "
    r"Если полученная строка находится в исходной последовательности, занчит между соответствующими вершинами нужно провести ребро."
    r" Переберем все найденные вершины: \\")

    nodes = list(g.keys())
    edges = []

    solution.append(generate_transition_table(nodes, words, edges))

    solution.append(r"Изобразим полученный граф:\\\\")

    solution.append(draw_de_bruijn_graph_clean_labels(g))

    solution.append(r"\\\\Найдем в полученной графе Эйлеров путь. Для этого определим степени вершин:")

    letex_table, table = generate_degree_table(g)

    solution.append(letex_table)
    
    start = ''
    end = ''
    for node in table.keys():
        if table[node] == 1: end = node
        if table[node] == -1: start = node

    if (start == '') or (end == ''):
        solution.append(r"Граф не Эйлеров, проверьте условие")
        return solution

    solution.append(r"Как известно, Эйлеров путь соединяет вершину, из которой выходит на 1 больше ребро, чем заходит "
                    r"с вершиной, в которую входит на одно больше ребро, чем выходит. \\ \\")
    
    solution.append(fr"Начальная вершина - {start}, конечная вершина - {end} \\")

    solution.append(r"Найдем все пути между ними, используя модифицированный поиск в глубину: \\ \\")

    solution.append(r"""\fbox{Alg} \textit{Рекурсивный алгоритм поиска всех эйлеровых путей между 2 вершинами (DFS)}.
    Обход следует начинать из стартовой вершины.
    \begin{algorithm}[H]
    \caption{Рекурсивный алгоритм поиска всех эйлеровых путей между 2 вершинами}\label{alg:DFS_Paths}
    \begin{algorithmic}
    \Statex $E_{visited}$ - множество посещенных ребер
    \Statex $E$ - множество всех ребер графа
    \Statex $u$ - конечная вершина
    \Statex $p$ - текущий путь
    \Statex $P$ - множество найденных эйлеровых путей
    \Function{DFS}{$v$, $p$}
        \State $p \gets p \cup \{v\}$ \Comment{Добавляем вершину в путь}
        \If{$v = u$}
            \If{$|E_{visited}| = |E|$} \Comment{Проверяем, является ли путь эйлеровым}
                \State $P \gets P \cup \{p\}$ \Comment{Сохраняем эйлеров путь}
            \EndIf
            \State \Return
        \EndIf
        \For{$w \in G[v]$} \Comment{Перебираем соседей}
            \If{$(v, w) \notin E_{visited}$}
                \State $E_{visited} \gets E_{visited} \cup \{(v, w)\}$ \Comment{Помечаем ребро как посещенное}
                \State $p_{copy} \gets p$ \Comment{Создаем копию пути}
                \State \Call{DFS}{$w$, $p_{copy}$}
                \State $E_{visited} \gets E_{visited} \setminus \{(v, w)\}$ \Comment{Откатываем изменения}
            \EndIf
        \EndFor
    \EndFunction
    \end{algorithmic}
    \end{algorithm}""")

    paths = []

    dfs(g, edges, [], start, end, [], paths)

    solution.append(r"В результате работы алгоритма получим:\\")

    for e in paths:
        solution.append(fr"Путь: {" ".join(e)}\\")

    solution.append(r"\textbf{Ответ:}\\")

    for e in paths:
        s= ''
        for node in e:
            s += node[0]
        s += e[-1][-1]
        solution.append(fr"{s}\\")
    

    return "".join(solution)