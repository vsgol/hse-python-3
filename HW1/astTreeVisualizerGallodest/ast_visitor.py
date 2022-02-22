import ast
from typing import Tuple

import networkx as nx


class AstVisitor(ast.NodeVisitor):

    def __init__(self, graph: nx.DiGraph):
        self._graph = graph
        self._node_index = 0

    def _get_next_index(self):
        self._node_index += 1
        return self._node_index

    def visit_Module(self, node):
        self.visit(node.body[0])

    def visit_FunctionDef(self, node):
        node_id = self._get_next_index()
        self._graph.add_node(node_id, label=f'Function definition: {node.name}', shape='s', fillcolor='#FFFEC9',
                             style='filled')
        self._graph.add_edge(node_id, self.visit(node.args))
        self._graph.add_edge(node_id, self.visit_Body(node))
        return node_id

    def visit_Return(self, node):
        node_id = self._get_next_index()
        self._graph.add_node(node_id, label='return', shape='s', fillcolor='#FFC9FE', style='filled')
        self._graph.add_edge(node_id, self.visit(node.value))
        return node_id

    def visit_Assign(self, node):
        node_id = self._get_next_index()
        self._graph.add_node(node_id, label='assign', shape='s', fillcolor='#C9E7FF', style='filled')
        self._graph.add_edge(node_id, self.visit_Targets(node))
        self._graph.add_edge(node_id, self.visit(node.value), label='value')
        return node_id

    def visit_Targets(self, node):
        node_id = self._get_next_index()
        self._graph.add_node(node_id, label='targets', fillcolor='#9CA1F0', style='filled')
        for tar in node.targets:
            self._graph.add_edge(node_id, self.visit(tar))
        return node_id

    def visit_For(self, node):
        node_id = self._get_next_index()
        iter_id = self._get_next_index()
        self._graph.add_node(node_id, label='for statement', shape='s', fillcolor='#F5A845', style='filled')
        self._graph.add_node(iter_id, label='iteration', fillcolor='#D6F5A7', style='filled')
        self._graph.add_edge(node_id, iter_id)
        self._graph.add_edge(iter_id, self.visit(node.target), label='target')
        self._graph.add_edge(iter_id, self.visit(node.iter))
        self._graph.add_edge(node_id, self.visit_Body(node))
        return node_id

    def visit_Body(self, node):
        node_id = self._get_next_index()
        self._graph.add_node(node_id, label='body', fillcolor='#DAF0E8', style='filled')
        for item in node.body:
            self._graph.add_edge(node_id, self.visit(item))
        return node_id

    def visit_Expr(self, node):
        node_id = self._get_next_index()
        self._graph.add_node(node_id, label='expression', shape='s', fillcolor='#F5A845', style='filled')
        self._graph.add_edge(node_id, self.visit(node.value))
        return node_id

    def visit_BinOp(self, node):
        node_id = self._get_next_index()
        self._graph.add_node(node_id, label=f'binary operation: \n {node.op.__class__.__name__}', shape='s',
                             fillcolor='#F5A845', style='filled')
        self._graph.add_edge(node_id, self.visit(node.left))
        self._graph.add_edge(node_id, self.visit(node.right))
        return node_id

    def visit_Call(self, node):
        node_id = self._get_next_index()
        self._graph.add_node(node_id, label='call', fillcolor='#DAF0E8', style='filled')
        self._graph.add_edge(node_id, self.visit(node.func))
        for item in node.args:
            self._graph.add_edge(node_id, self.visit(item))
        return node_id

    def visit_Attribute(self, node):
        node_id = self._get_next_index()
        self._graph.add_node(node_id, label=f'attribute \n name: {node.attr}', shape='s', fillcolor='#FFFC9C',
                             style='filled')
        self._graph.add_edge(node_id, self.visit(node.value))
        return node_id

    def visit_Subscript(self, node):
        return self.visit(node.value)

    def visit_Name(self, node):
        node_id = self._get_next_index()
        self._graph.add_node(node_id, label=f'name: {node.id}', shape='s', fillcolor='#B8FFBC', style='filled')
        return node_id

    def visit_List(self, node):
        node_id = self._get_next_index()
        self._graph.add_node(node_id, label='list', fillcolor='#8BFF8B', style='filled')
        for num, item in enumerate(node.elts):
            self._graph.add_edge(node_id, self.visit(item))
        return node_id

    def visit_Tuple(self, node):
        node_id = self._get_next_index()
        self._graph.add_node(node_id, label='tuple', fillcolor='#87F38B', style='filled')
        for num, item in enumerate(node.elts):
            self._graph.add_edge(node_id, self.visit(item))
        return node_id

    def visit_Num(self, node):
        node_id = self._get_next_index()
        self._graph.add_node(node_id, label=f'number \n value: {str(node.n)}', shape='s', fillcolor='#B8FFBC',
                             style='filled')
        return node_id

    def visit_arguments(self, arguments):
        node_id = self._get_next_index()
        self._graph.add_node(node_id, label='arguments', fillcolor='#DAF0E8', style='filled')
        for arg in arguments.args:
            arg_id = self._get_next_index()
            self._graph.add_node(arg_id, label=f'name: {arg.arg}', shape='s', fillcolor='#B8FFBC',
                                 style='filled')
            self._graph.add_edge(node_id, arg_id)
        return node_id
