import os
from datetime import date
from typing import List
from astTreeVisualizerGallodest import create_fib_ast_tree


def centre(func):
    def inner(*args, **kwargs):
        content = func(*args, **kwargs)
        return '\n'.join((
            '\\begin{center}',
            '\t' + content.replace('\n', '\n\t'),
            '\\end{center}'
        ))

    return inner


def latex_header(title: str, author: str, date: str) -> str:
    return '\n'.join((
        '\\documentclass[12pt]{article}',
        '\\usepackage[utf8]{inputenc}',
        '\\usepackage[english,russian]{babel}',
        '\\usepackage{{graphicx}}',
        f'\\title{{{title}}}',
        f'\\author{{{author}}}',
        f'\\date{{{date}}}',
        '\\begin{document}',
        '',
        '\\maketitle',
        ''
    ))


def latex_footer() -> str:
    return '\n'.join((
        '',
        '\\end{document}'
    ))


@centre
def latex_table(table: List[list]) -> str:
    def verify(t: List[list]) -> bool:
        return all(
            map(lambda x: len(x) == len(t[0]), t)
        )

    def get_constructor(n: int) -> str:
        return 'c | ' * (n - 1) + 'c'

    if verify(table):
        return '\n'.join((
            '\\begin{tabular} ' + f'{{ {get_constructor(len(table[0]))} }}',
            ' \\\\\n\\hline\n'.join(map(
                lambda row: ' & '.join(map(str, row)), table
            )),
            '\\end{tabular}',
        ))
    else:
        raise ValueError('the matrix must be rectangular')


@centre
def latex_image(path: str, scale: float = 1) -> str:
    return f'\\includegraphics[scale={scale}]{{{path}}}\\\\'


if __name__ == "__main__":
    sample = [
        [1, 2, 3],
        ['a', 'b', 'c'],
        ['$4\\times 3$', '$\Rightarrow $', '12']
    ]

    if not os.path.exists("../artifacts"):
        os.mkdir("../artifacts")
    create_fib_ast_tree()

    with open('../artifacts/file.tex', 'w') as f:
        f.write(
            '\n'.join((
                latex_header("Test LaTeX file", "galloDest", date.today().strftime("%B %d, %Y")),
                latex_table(sample),
                '',
                latex_image('../artifacts/ast.png', scale=0.3),
                latex_footer()
            ))
        )
