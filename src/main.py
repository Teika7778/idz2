import pylatex.config as cf
from pylatex import Document, Command, NoEscape

import tasks.task1 as task1
import tasks.task2 as task2
import tasks.task3 as task3
import tasks.task4 as task4
import tasks.task7 as task7
import tasks.task8 as task8
import tasks.task9 as task9
import tasks.task10 as task10


def addpacks(doc):
    doc.preamble.append(Command('usepackage', 'babel', options='russian'))
    doc.preamble.append(Command('usepackage', 'amsmath'))
    doc.preamble.append(Command('usepackage', 'tempora'))
    doc.preamble.append(Command('usepackage', 'fbox'))
    doc.preamble.append(Command('usepackage', 'tikz'))
    doc.preamble.append(Command('usepackage', 'algorithm'))
    doc.preamble.append(Command('usepackage', 'algpseudocode'))
    doc.preamble.append(Command('usepackage', 'xcolor'))
    doc.preamble.append(Command('usepackage', 'nicematrix'))
    doc.preamble.append(Command('usepackage', 'geometry', options='a4paper, margin=2cm'))
    doc.preamble.append(Command('usetikzlibrary', 'positioning'))


def gen_solution():
    ar = []
    ar.append(task1.solve(
        [[1, 1, 1, 1, 1],
         [1, 0, 0, 0, 0],
         [1, 0, 1, 0, 1],
         [1, 1, 1, 1, 1],
         [1, 0, 0, 1, 1]]))
    ar.append(task2.solve(12, 10))

    ar.append(task3.solve([
        [4, 4, 2, 2, 2, 2, 4],
        [4, 4, 2, 4, 5, 2, 3]
    ]))
    
    ar.append(task4.solve(
        [6, 3, 6, 6, 5, 7, 5, 10],
        {
            1: [2, 10, 8, 6],
            8: [7, 9],
            4: [3, 10],
            5: [10]
        }

    ))

    ar.append(task7.solve(20))

    ar.append(task8.solve(
    {
        'A': ['B', 'E'],
        'B': ['E', 'C'],
        'C': ['B'],
        'D': ['H', 'O', 'F', 'E', 'C'],
        'E': ['F', 'N'],
        'F': ['E'],
        'G': ['F', 'J'],
        'H': ['L'],
        'I': ['E', 'M', 'N'],
        'J': ['F', 'E'],
        'K': ['J', 'G', 'N'],
        'L': [],
        'M': [],
        'N': ['J', 'K'],
        'O': ['D', 'P'],
        'P': []
    }
    ))
    ar.append(task9.solve({

            1: [2, 10, 8, 6],
            8: [7, 9],
            4: [3, 10],
            5: [10]
        }))

    ar.append(task10.solve(
    {
    'A': ['B', 'E'],
    'B': ['A', 'C'],
    'C': ['B', 'D', 'E'],
    'D': ['C', 'E', 'F'],
    'E': ['A', 'C', 'D', 'H', 'L', 'K', 'G'],
    'F': ['D', 'H'],
    'G': ['E', 'I'],
    'H': ['F', 'L', 'E'],
    'I': ['G', 'J'],
    'J': ['I', 'K'],
    'K': ['J', 'E', 'L'],
    'L': ['H', 'K', 'E']
    }
    ))

    return ar


if __name__ == "__main__":
    cf.active = cf.Version1(indent=False)
    solution_raw = gen_solution()
    for i in range(len(solution_raw)):
        solution_raw[i] = fr"\section{{Задача {i + 1}}}" + "\n" + solution_raw[i]

    print("Генерация решения ИДЗ...")
    doc = Document(data=[NoEscape(r"\newpage".join(solution_raw))], document_options="12pt")
    addpacks(doc)
    print("Компиляция LaTeX...")
    doc.generate_pdf("Решение", clean_tex=False)
