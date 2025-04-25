def str_arr(arr):
    return ", ".join([f"({p[0]}, {p[1]})" for p in arr])


def generate_tikz(edges, n):
    tikz_code = []
    tikz_code.append(r"\begin{tikzpicture}[every node/.style={circle, draw, fill=white}]")
    angle_step = 360 / n if n != 0 else 0
    for i in range(n):
        angle = i * angle_step
        tikz_code.append(fr"\node ({i}) at ({angle}:2cm) {{{i}}};")
    # Убираем повторяющиеся ребра и петли
    unique_edges = set()
    for u, v in edges:
        if u != v:
            unique_edges.add((min(u, v), max(u, v)))
    for u, v in unique_edges:
        tikz_code.append(fr"\draw ({u}) -- ({v});")
    tikz_code.append(r"\end{tikzpicture}")
    return "\n".join(tikz_code)


def solve(degrees):
    solution = []

    solution.append(
        fr"Существует ли граф со степенями вершин а) ${','.join(str(x) for x in degrees[0])}$; б) ${','.join(str(x) for x in degrees[1])}$? "
        r"Если существует, то постройте, если нет, то объясните почему.\\"
    )
    solution.append(r"\textbf{Решение.}")
    solution.append(
        r"Для решения поставленной задачи сформулируем теорему:\\ "
        r"\fbox{Тh} Пусть дана последовательность неотрицательных чисел в порядке невозрастания $$s, d_1, \ldots, d_s, "
        r"t_1, \ldots, t_k$$"
        r"Она является графической (то есть числам можно соотнести степени вершин графа) тогда "
        r"и только тогда, когда последовательность $d_1-1, \ldots, d_s-1, t_1, \ldots, t_k$ является графической.\\"
        r"\fbox{Alg} \textit{Алгоритм Гавела — Хакими}. На основе теоремы можно сформулировать и алгоритм для "
        r"построения графа. Предлагается такой псевдокод:"
        r"""
        \begin{algorithm}
        \caption{Алгоритм Гавела — Хакими}\label{alg:Example}
        \begin{algorithmic}
        \Statex $D$ - массив степеней вершин, $D^*$ - массив номеров вершин.
        \Statex $E$ - ребра желаемого графа
        \While{$D$ не содержит отрицательных чисел И $D$ содержит хотя бы одно ненулевое число}
            \State Сортируем массив $D$
            \State $s \gets D_0$
            \State Добавляем в $E$ ребра $(D^*_0, D^*_1), (D^*_0, D^*_2), \ldots, (D^*_0, D^*_s)$
            \State Удаляем $D_0$ из массива
            \State Уменьшаем $D_1$, $D_2$, \ldots, $D_s$ на $1$
        \EndWhile
        \If{$D$ содержит только нули}
            \State $E$ - искомый граф
        \Else
            \State Последовательность $D$ не графическая
        \EndIf

        \end{algorithmic}
        \end{algorithm}
        """
    )
    for num, deg in enumerate(degrees):
        let = 'а)' if num == 0 else 'б)'
        E = []
        solution.append(
            fr"{let} Применим алгоритм:\\"
            fr"Понумеруем вершины, будем хранить массив пар степени и номера:\\")
        verts = []
        for x, y in enumerate(deg):
            verts.append((y, x))
        solution.append(fr"$$D = {str_arr(verts)}$$")
        i = 1
        while any(v[0] != 0 for v in verts) and all(v[0] >= 0 for v in verts):
            verts.sort(reverse=True)
            s = verts[0][0]
            for x in range(1, s + 1):
                E.append((verts[0][1], verts[x][1]))
            solution.append(
                fr"Итерация {i}. Сортируем массив:"
                fr"$$D = {str_arr(verts)}$$"
                fr"Отсюда $s = {s}$. Обновим $E$:"
                fr"$$E = {str_arr(E)}$$"
            )
            verts.pop(0)
            for x in range(0, s):
                verts[x] = (verts[x][0] - 1, verts[x][1])
            solution.append(fr"Итого имеем массив (после изменений):"
                            fr"D = $${str_arr(verts)}$$")
            i += 1

        if all(v[0] >= 0 for v in verts):
            solution.append(fr"\textbf{{Таким образом искомый граф имеет рёбра:}} $${str_arr(E)}$$")
            # Генерация TikZ рисунка
            n = len(deg)
            if n > 0:
                tikz_output = generate_tikz(E, n)
                solution.append(r"\begin{center}")
                solution.append(tikz_output)
                solution.append(r"\end{center}")
        else:
            solution.append(r"\textbf{Таким образом искомый граф не существует} \\")

    solution.append(r"\textbf{Проверка.} Воспользуемся теоремой Эрдёша-Галлаи. \\"
                    r"\fbox{Th} \textit{Теорема Эрдёша — Галлаи}. Пусть последовательность $d = \left\{"
                    r"d_k\right\}^n_{k=1}$"
                    r" удовлетворяет двум критериям (называется \textit{правильной}):")
    solution.append(r"""\begin{align*}
    1&. \ n-1 \geq d_1 \geq d_2 \geq d_3 \geq \ldots \geq d_n \geq 0\\
    2&. \ \sum d_k = 0 \ (\mathrm{mod} \ 2)
    \end{align*}""")
    solution.append(r"""
    Тогда $d$ является графической тогда и только тогда, когда $\forall k: 1 \leq k \leq n-1$ выполняется:
    $$\sum \limits_{i=1}^k d_i \leq k(k-1) + \sum \limits_{i=k+1}^n\min(k, d_i)$$
    Проверим эти условия.
    """)
    for num, deg in enumerate(degrees):
        let = 'а) ' if num == 0 else 'б) '
        solution.append(let)
        deg = sorted(deg, reverse=True)
        n = len(deg)
        solution.append(
            fr"""Проверим последовательность на условия теоремы. Для этого сортируем массив степеней:
$$d = {deg}$$
Проверим $\sum d_i = {sum(deg)} = {sum(deg) % 2}$, $d_1 = {deg[0]}$
""")
        if sum(deg) % 2 == 0 and n-1 >= deg[0]:
            solution.append("Последовательность удовлетворяет всем необходимым условиям для теоремы, "
                            "поэтому применим ее:")
            solution.append(r"\[\begin{aligned}")
            f = 0
            for k in range(1, n):
                solution.append(fr"k = {k}.& \ {sum(deg[0:k])} \leq {k * (k - 1)} "
                                fr"{''.join([(' + ' + str(min(k, deg[i]))) for i in range(k, n)])} = "
                                fr"{k * (k - 1) + sum([min(k, deg[i]) for i in range(k, n)])}\\")
                if sum(deg[0:k]) > k * (k - 1) + sum([min(k, deg[i]) for i in range(k, n)]):
                    f = 1
                    break
            solution.append(r"\end{aligned}\]")
            if f:
                solution.append(fr"Проверка провалена. Последовательность не графическая.\\")
            else:
                solution.append(fr"Проверка пройдена. Последовательность графическая.\\")
        else:
            solution.append(fr"Проверка провалена. Последовательность не графическая.\\")

    return "\n".join(solution)
