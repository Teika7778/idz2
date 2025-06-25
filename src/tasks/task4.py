import math_util as math_util
from copy import deepcopy

def draw_graph(graph:dict):

    g = r"""
    \begin{center}
    \begin{tikzpicture}[
    every node/.style={circle, draw, fill=white, minimum size=1cm},
    node distance=2cm and 2cm,  
    >=stealth,
    use positioning/.style={right=of #1}  
    ]
    """

    nodes = list(graph.keys())

    if 1 in nodes:
        g += r"\node (0) {1};"
    else:
        g += r"\node[opacity=0] (0) {1};"

    if 6 in nodes:
        g += r"\node[below=of 0] (5) {6};"
    else:
        g += r"\node[below=of 0, opacity=0] (5) {6};"


    for x in range(1, 5):


        if x+1 in nodes : g += fr"\node[right = of {x-1}] ({x}) {{{x+1}}};" + "\n"
        else : g += fr"\node[right = of {x-1}, opacity=0] ({x}) {{{x+1}}};" + "\n"
        
        y = x + 5
        if y+1 in nodes : g += fr"\node[right = of {y - 1}] ({y}) {{{y + 1}}};" + "\n"
        else : g += fr"\node[right = of {y - 1}, opacity=0] ({y}) {{{y+1}}};" + "\n"

    for vertex in graph.keys():
        for neighbourhood_vertex in graph[vertex]:
                g += fr"\draw ({vertex-1}) -- ({neighbourhood_vertex-1});" + "\n" 

    g += r"""
    \end{tikzpicture} 
    \end{center}
    """

    return g
     

def make_prufer_code(input_graph:dict, solution: list):

    solution.append(fr"\textbf{{Шаг номер 0}}.Изобразим граф на данным шаге:")
    solution.append(draw_graph(input_graph))

    count = 1

    graph = deepcopy(input_graph)
     
    answ = []

    while (len(graph.keys()) !=  2):
         
        leaf = min([node for node in graph.keys() if len(graph[node]) == 1])
        neighbor = 0

        del graph[leaf]

        for node in graph.keys():
            if leaf in graph[node]:
                neighbor = node
                answ.append(str(node))
                ind = graph[node].index(leaf)
                del graph[node][ind]

        solution.append(fr"\textbf{{Шаг номер {count}}}. \\ Лист с минимальным номером - {leaf}.\\ Его сосед - {neighbor}.\\"
                        fr"Код Прюфера - {" ".join(answ)}\\"
                        fr"Удалим лист и инцидентное ему ребро из графа и изобразим граф на данным шаге:")

        solution.append(draw_graph(graph))

        count += 1


    solution.append(r"В множестве вершин графа осталось всего 2 вершины, поэтому следует прекратить цикл и записать их в код Прюфера:\\")
    answ.append(str(list(graph.keys())[0]))
    answ.append(str(list(graph.keys())[1]))
    solution.append( fr"\textbf{{Ответ: код Прюфера - {' '.join(answ)}}}\\\\")

def make_graph(nums:list , solution:list):

    nodes = list(range(1, len(nums)+3))

    added_nodes = []

    g = dict()

    for vertex in nodes:
        g[vertex] = []

    solution.append(fr"\textbf{{Шаг номер 0}}.Изобразим входные данные: \\")
    solution.append(fr"Список вершин - {" ".join(map(str, nodes))} \\")
    solution.append(fr"Код Прюфера - {" ".join(map(str, nums))} \\")

    for i in range(len(nodes) - 2):

        for vertex in nodes:
            if vertex not in nums:

                solution.append(fr"\textbf{{Шаг номер {i+1}}}. \\"
                        fr"Вершина с наименьшим номером, не входящая в код Прюфера - {vertex}\\"
                        fr"Добавим в граф ребро ({vertex};{nums[0]}) и изобразим граф на данном шаге:\\")
                g[vertex].append(nums[0]) # Добавляем ребро
                solution.append(draw_graph(g))
                added_nodes.append(vertex)
                index =  nodes.index(vertex)
                solution.append(fr"Удлим из последовательности вершин вершину {vertex}, а из кода Прюфера {nums[0]}:\\")
                del nodes[index]
                del nums[0]
                solution.append(fr"Список вершин - {" ".join(map(str, nodes))}\\")
                solution.append(fr"Код Прюфера - {" ".join(map(str, nums))}\\")
                break

    solution.append(r"В коде Прюфера не осталось ни одного элемента, значит нужно соединить две оставшиеся в списке вершин вершины.\\"
                    r"\textbf{Ответ:}\\")
    remaining_verticles = list(set(nodes).difference(set(added_nodes)))
    g[remaining_verticles[0]].append(remaining_verticles[1])

    solution.append(draw_graph(g))


def solve(nums, graph):
    solution = []
    mat = math_util.graph_to_adj_matrix(graph)
    solution.append("а)Постройте код Прюфера для данного дерева:")

    graph = math_util.graph_closure(graph)
    
    solution.append(draw_graph(graph))

    solution.append(fr"б) Постройте дерево по коду Прюфера:\\ {" ".join(map(str, nums))} \\ ")

    solution.append(r"\textbf{Решение. \\ a)}\\")

    solution.append(
    r"Для решения задачи воспользуемся алгоритмом построения кода Прюфера:\\"
    r"\fbox{Alg} \textit{Алгоритм построения кода Прюфера}."
    r"Предлагается такой псевдокод:"
    r"""
    \begin{algorithm}
    \caption{Алгоритм построения кода Прюфера}\label{alg:Prufer}
    \begin{algorithmic}
    \Statex \textbf{Вход}: Дерево $T = (V, E)$ с $n \geq 2$ вершинами
    \Statex \textbf{Выход}: Код Прюфера $P$
    \State $P \gets \emptyset$
    \While{$|V| > 2$}
        \State Найти лист $v \in V$ с наименьшим номером
        \State $u \gets$ единственный сосед $v$ (т.е. $(u,v) \in E$)
        \State $P \gets P \cup \{u\}$
        \State Удалить $v$ из дерева: $V \gets V \setminus \{v\}$
        \State Удалить ребро $(u,v)$: $E \gets E \setminus \{(u,v)\}$
    \EndWhile
    \State \Return $P$
    \end{algorithmic}
    \end{algorithm}
    \\
    """
    )

    solution.append(r"Применим алгоритм к данному графу:\\\\")

    make_prufer_code(graph, solution)

    solution.append(r"\textbf{б)}\\")

    solution.append(
    r"Для решения задачи воспользуемся алгоритмом восстановления дерева по коду Прюфера:\\"
    r"\begin{algorithm}"
    r"\caption{Восстановление дерева по коду Прюфера}"
    r"\begin{algorithmic}"
    r"\Statex \textbf{Вход}: Код Прюфера $K = [k_1, k_2, ..., k_{n-2}]$, число вершин $n$"
    r"\Statex \textbf{Выход}: Множество рёбер $E$ восстановленного дерева"
    r"\State $L \gets [1, 2, ..., n]$ \Comment{Список всех вершин}"
    r"\State $E \gets \emptyset$"
    r"\For{$i \gets 1$ \textbf{to} $n-2$}"
    r"    \State Найти вершину $v_j \in L$ с минимальным номером, где $v_j \notin K$"
    r"    \State $E \gets E \cup \{(v_j, k_i)\}$ \Comment{Добавляем ребро}"
    r"    \State Удалить $v_j$ из $L$"
    r"    \State Удалить $k_i$ из $K$"
    r"\EndFor"
    r"\State Добавить ребро $(L[0], L[1])$ в $E$"
    r"\State \Return $E$"
    r"\end{algorithmic}"
    r"\end{algorithm}\\\\"
    )

    make_graph(nums, solution)

    
    return "\n".join(solution)
