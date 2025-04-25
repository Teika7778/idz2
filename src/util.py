def get_matrix_latex(matix):
    ret = ""
    ret += r"\begin{pNiceMatrix} "
    for row in matix:
        f = 0
        for elem in row:
            if not f:
                ret += str(elem) + " "
                f = 1
            else:
                ret += " & " + str(elem)
        ret += r"\\ "

    ret += r"\end{pNiceMatrix}"
    return ret


def get_matrix_latex_hightlighted(matix, colored_rows=None, colored_cols=None, colored_cells=None,
                                  color="blue!30", color2="blue!30", color3="blue!30"):
    if colored_cells is None:
        colored_cells = []
    if colored_cols is None:
        colored_cols = []
    if colored_rows is None:
        colored_rows = []
    ret = ""
    ret += r"\begin{pNiceMatrix}"
    n = len(matix)
    m = len(matix[0])
    ret += "[code-before = {\n"
    for row in colored_rows:
        ret += fr"\rectanglecolor{{{color}}}{{{row}-1}}{{{row}-{m}}} "
    for col in colored_cols:
        ret += fr"\rectanglecolor{{{color2}}}{{1-{col}}}{{{m}-{col}}} "
    for cell in colored_cells:
        ret += fr"\cellcolor{{{color3}}}{{{cell[0]}-{cell[1]}}}"
    ret += "}] \n"

    for row in matix:
        f = 0
        for elem in row:
            if not f:
                ret += str(elem) + " "
                f = 1
            else:
                ret += " & " + str(elem)
        ret += r"\\ "

    ret += r"\end{pNiceMatrix}"
    return ret


