def logical_matrix_mult(a, b):
    n = len(a)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            temp = 0
            for k in range(n):
                temp |= a[i][k] & b[k][j]
                if temp:
                    break
            result[i][j] = temp
    return result


def graph_to_adj_matrix(graph):
    # Собираем все уникальные узлы
    nodes = set()
    for key in graph:
        nodes.add(key)
        nodes.update(graph[key])
    sorted_nodes = sorted(nodes)
    n = len(sorted_nodes)

    # Создаем словарь для соответствия узла и индекса
    node_index = {node: idx for idx, node in enumerate(sorted_nodes)}

    # Инициализируем матрицу нулями
    adj_matrix = [[0] * n for _ in range(n)]

    # Заполняем матрицу с учетом симметрии
    for node in graph:
        i = node_index[node]
        for neighbor in graph[node]:
            j = node_index[neighbor]
            adj_matrix[i][j] = 1
            adj_matrix[j][i] = 1  # Добавляем обратную связь

    return adj_matrix

def graph_closure(graph: dict): # Функция замыкания списка смежности до полного

    closed_graph = dict()

    for old_vertex in graph.keys():
        if old_vertex not in closed_graph.keys():
            closed_graph[old_vertex] = graph[old_vertex]
        else:
            for vertex in graph[old_vertex]:
                if vertex not in closed_graph[old_vertex]:
                    closed_graph[old_vertex].append(vertex)
        for new_vertex in graph[old_vertex]:
            if new_vertex not in closed_graph.keys():
                closed_graph[new_vertex] = [old_vertex]
            else:
                closed_graph[new_vertex].append(old_vertex)

    return closed_graph



def identity_matrix(n):
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


def matrix_powers(matrix):
    n = len(matrix)
    if any(len(row) != n for row in matrix):
        raise ValueError("Матрица должна быть квадратной")

    powers = [identity_matrix(n)]

    for i in range(1, n + 1):
        current_power = logical_matrix_mult(matrix, powers[i - 1])
        powers.append(current_power)

    return powers


def summ_ar(arr):
    n = len(arr[0])
    zero = [[0 for _ in range(n)] for _ in range(n)]
    for x in range(n):
        for y in range(n):
            for w in range(len(arr)):
                zero[x][y] = zero[x][y] or arr[w][x][y]
    return zero
