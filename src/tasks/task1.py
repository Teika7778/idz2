import util
import math_util
import itertools
from copy import deepcopy


def solve(matrix):
    original = deepcopy(matrix)
    n = len(matrix)
    ret = []
    ret += [r"Дана матрица смежности $M$ для бинарного отношения:\\"]
    ret += [fr"$$ M = {util.get_matrix_latex(matrix)}$$"]
    ret += [r"Нужно найти транзитивное замыкание этого отношения по алгоритму Уоршелла.\\"]
    ret += [r"\\ \textbf{Решение.}"]
    ret += [r"Переберем все вершины ($k$), найдем пути проходящие через них и достроим недостающие. "
            r"Проиллюстрируем алгоритм на матрице смежности: сначала для каждого $k$ найдем все пары элементов $(i, j)$"
            r", такие что $M[i, k] = 1$ и $M[k, j] = 1$, затем для каждой такой пары положим $M[i,j]=1$.\\"]
    for k in range(n):
        ret += [fr"Для вершины {k + 1}:"]
        ret += [fr"$$  {util.get_matrix_latex_hightlighted(matrix, [k + 1], [k + 1])}"]
        p_in = []
        p_out = []
        for x in range(n):
            if matrix[k][x]:
                p_out.append(x + 1)
            if matrix[x][k]:
                p_in.append(x + 1)
        dots = list(itertools.product(p_in, p_out))
        ret += [
            fr"{util.get_matrix_latex_hightlighted(matrix, p_in, p_out, dots, color='red!20', color2='blue!20', color3='purple!40')} "]
        changed = []
        for dot in dots:
            if matrix[dot[0] - 1][dot[1] - 1] == 0:
                matrix[dot[0] - 1][dot[1] - 1] = 1
                changed.append(dot)
        ret += [fr"{util.get_matrix_latex_hightlighted(matrix, [], [], changed)}$$"]
    ret += [r"\\ \textbf{Ответ.}"]
    ret += [fr"$${util.get_matrix_latex(matrix)}$$"]
    ret += [r"\\ \textbf{Проверка.}"]
    ret += [fr"Возведем матрицу $M$ в ${n}$ логическую степень и найдем логическую сумму:"]
    ret += [fr"$$\sum\limits_{{i=1}}^{{{n}}}M^i = S$$"]
    powers = math_util.matrix_powers(original)
    ret += [fr"$$S = {util.get_matrix_latex(powers[1])}"]
    for x in range(2, n+1):
        ret += [fr" + {util.get_matrix_latex(powers[x])}"]
    ret += [r"$$"]
    ret += [fr"$$S = {util.get_matrix_latex(math_util.summ_ar(powers[1:]))}$$"]
    if math_util.summ_ar(powers[1:]) != matrix:
        raise Exception("Проверка не прошла в задаче 1.")
    else:
        ret += ["Проверка успешна."]
    return "\n".join(ret)
