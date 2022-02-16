import ast

import inspect
import networkx

from .fibonacci import *
from .ast_visitor import AstVisitor


def create_fib_ast_tree(target_file='../artifacts/ast.png'):
    create_ast_tree(fibonacci, target_file=target_file)


def create_ast_tree(function, target_file='../artifacts/ast.png'):
    fibonacci_code = inspect.getsource(function)
    module = ast.parse(fibonacci_code)
    ast_tree = networkx.DiGraph()
    visitor = AstVisitor(ast_tree)
    visitor.visit(module)
    networkx.drawing.nx_pydot.to_pydot(ast_tree).write_png(target_file)


if __name__ == "__main__":
    create_fib_ast_tree()
