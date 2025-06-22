import math_util as math_util

def draw_graph(graph):
    # Определяем порядок вершин в цикле
    cycle_order = ['A', 'B', 'C', 'D', 'F', 'H', 'L', 'K', 'J', 'I', 'G', 'E']
    
    # Проверяем, что все вершины графа учтены
    missing = set(graph.keys()) - set(cycle_order)
    if missing:
        raise ValueError(f"Вершины {missing} не включены в цикл")

    # Создаем TikZ-код
    tikz_code = r"""
    \begin{center}
    \begin{tikzpicture}[
        every node/.style={circle, draw, fill=white, minimum size=10mm},
        node distance=1.5cm and 1.5cm,
        >=stealth,
        font=\small
    ]
    """

    # Позиционируем вершины в 4 столбца
    positions = {
        'A': (0, 0), 'B': (2, 0), 'C': (4, 0), 'D': (6, 0),    
        'E': (0, -2),                                           
        'F': (6, -2), 'H': (6, -4), 'L': (6, -6),              
        'G': (0, -4), 'I': (0, -6), 'J': (2, -6), 'K': (4, -6) 
    }

    # Рисуем вершины
    for node, (x, y) in positions.items():
        tikz_code += f"\\node at ({x},{y}) ({node}) {{{node}}};\n"

    # Рисуем ребра цикла
    for i in range(len(cycle_order)):
        u = cycle_order[i]
        v = cycle_order[(i+1)%len(cycle_order)]
        if v in graph[u]:
            tikz_code += f"\\draw ({u}) -- ({v});\n"

    # Рисуем дополнительные ребра (не входящие в основной цикл)
    drawn_edges = set()
    for u in graph:
        for v in graph[u]:
            if (u, v) not in drawn_edges and (v, u) not in drawn_edges:
                if (u in cycle_order and v in cycle_order and 
                    abs(cycle_order.index(u) - cycle_order.index(v)) != 1 and
                    abs(cycle_order.index(u) - cycle_order.index(v)) != len(cycle_order)-1):
                    tikz_code += f"\\draw ({u}) -- ({v});\n"
                elif not (u in cycle_order and v in cycle_order):
                    tikz_code += f"\\draw ({u}) -- ({v});\n"
                drawn_edges.add((u, v))

    tikz_code += r"""
    \end{tikzpicture}
    \end{center}
    """
    
    return tikz_code


def bfs(graph, node):

    queue = [(node, 0)]
    visited_nodes = {node: 0}

    while (len(visited_nodes) != len(graph.keys())):

        top = queue.pop(0)

        for neighborn in graph[top[0]]:
            if neighborn not in list(visited_nodes.keys()):
                queue.append((neighborn, top[1]+1))
                visited_nodes[neighborn] = top[1] + 1

    return [visited_nodes[key] for key in sorted(visited_nodes)] ## Сортируем по ключам и возращаем значения


def fill_table(graph):

    table = [[] for _ in range(12)]

    i = 0

    for node in sorted(list(graph.keys())):
        table[i] = bfs(graph, node)
        i += 1

    return table

    




def solve(graph: dict):
    solution = []
    # Формулировка задачи
    solution.append(
        fr"Найдите радиус, диаметр и центр данного дерева:\\"
    )
    # Отрисовка Графа
    g = draw_graph(graph)
    solution.append(g)

    # Решение
    solution.append(r"\textbf{Решение.}\\")

    solution.append(r"Для решения задачи построим матрицу расстояний графа. "
            r"В ней на пересечении i-го столбца и j-ой строки будет записано кратчайшее расстояние между i и j. "
            r"Расстояние между вершинами найдем, используя поиск в глубину:"  )

    table = fill_table(graph)

    # Генерация LaTeX-кода для таблицы
    latex_table = r"""
    \begin{center}
    \begin{tabular}{|c|c|c|c|c|c|c|c|c|c|c|c|c|}
    \hline
     & \textbf{A} & \textbf{B} & \textbf{C} & \textbf{D} & \textbf{E} & \textbf{F} & \textbf{G} & \textbf{H} & \textbf{I} & \textbf{J} & \textbf{K} & \textbf{L} \\ 
    \hline
    """

    # Добавляем строки с метками A-L
    labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
    for i, row in enumerate(table):
        latex_table += f"\\textbf{{{labels[i]}}} & " + " & ".join(map(str, row)) + r" \\ \hline" + "\n"

    latex_table += r"""
    \end{tabular}
    \end{center}
    """

    solution.append(latex_table)

    solution.append(r"Эксцентриситетом i-ой вершины будет являтся максимум из чисел, записанных в i-ой строке."
                    r"Найдем эксцентриситеты вершин:")
    
    eccentricity_table = [max(row) for row in table]  # Ваши данные (12 чисел)
    labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']

    latex_ecc_table = r"""
    \begin{center}
    \begin{tabular}{|c|c|}
    \hline
    \textbf{Вершина} & \textbf{Эксцентриситет} \\
    \hline
    """

    for label, value in zip(labels, eccentricity_table):
        latex_ecc_table += f"{label} & {value} \\\\ \\hline\n"

    latex_ecc_table += r"""
    \end{tabular}
    \end{center}
    """

    solution.append(latex_ecc_table)

    solution.append(r"По определению диаметр - максимальный эксцентриситет в графе. Радиус - минимальный эксцентриситет. " \
    r"Центр - вершины с эксцентриситетом равным радиусу. Воспользумся таблицей для поиска этих значений и запишем ответ.\\")

    solution.append(r"\textbf{Ответ.}\\")



    solution.append(fr"Диаметр - {max(eccentricity_table)}, Радиус - {min(eccentricity_table)}, "
                    fr"Центры - {" ".join([chr(i+65) for i in range(12) if eccentricity_table[i] == min(eccentricity_table)])}")

    return "\n".join(solution)
