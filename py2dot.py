#!/usr/bin/env python3
"""
py2flow.py
Genera un archivo .dot (Graphviz) que representa un diagrama de flujo
simplificado de un archivo fuente Python.
Limitaciones:
 - No construye un verdadero CFG con análisis de alcance/alcance de variables.
 - Trata sentencias como cajas con el código (usando ast.unparse).
 - Soporta estructuras: sequential, if/elif/else, while, for, try/except.
 - No representa expresiones lambda internamente, ni comprehensions complejas.
 - Los nodos de decisión (if/while) se dibujan como diamantes mediante attribute shape=diamond.
"""

import os
import ast
import sys
from itertools import count

class DotBuilder:
    def __init__(self):
        self.lines = []
        self.node_id = count(1)
        self.add_header()

    def add_header(self):
        self.lines.append('digraph flow {')
        self.lines.append('  rankdir=TB;')
        self.lines.append('  node [shape=rectangle, fontname="Consolas"];')
        self.lines.append('')

    def new_node(self, label, shape=None, style=None):
        nid = f"n{next(self.node_id)}"
        label_esc = label.replace('"', '\\"').replace('\n', '\\l') + '\\l'
        attr = []
        attr.append(f'label="{label_esc}"')
        if shape:
            attr.append(f'shape={shape}')
        if style:
            attr.append(f'style="{style}"')
        self.lines.append(f'  {nid} [{", ".join(attr)}];')
        return nid

    def add_edge(self, a, b, label=None):
        if label:
            self.lines.append(f'  {a} -> {b} [label="{label}"];')
        else:
            self.lines.append(f'  {a} -> {b};')

    def add_footer(self):
        self.lines.append('}')

    def dump(self):
        self.add_footer()
        return "\n".join(self.lines)


class FlowBuilder(ast.NodeVisitor):
    def __init__(self, src_text):
        self.dot = DotBuilder()
        self.src = src_text
        self.last_nodes = []  # current "tails" where next statements should attach

    def code_of(self, node):
        # Use ast.unparse if available (py3.9+)
        try:
            s = ast.unparse(node)
        except Exception:
            # Fallback naive: try to get source segment
            try:
                s = ast.get_source_segment(self.src, node) or node.__class__.__name__
            except Exception:
                s = node.__class__.__name__
        return s

    def build(self, node):
        # start node
        start = self.dot.new_node("INICIO", shape="ellipse")
        self.last_nodes = [start]
        if isinstance(node, ast.Module):
            self.process_block(node.body)
        else:
            self.visit(node)
        end = self.dot.new_node("FIN", shape="ellipse")
        for tail in self.last_nodes:
            self.dot.add_edge(tail, end)
        return self.dot.dump()

    def process_block(self, stmts):
        for stmt in stmts:
            self.visit(stmt)
        # after block, last_nodes updated

    # Generic: attach a single statement node representing simple stmts
    def generic_simple_stmt(self, node, label=None):
        lab = label if label is not None else self.code_of(node)
        n = self.dot.new_node(lab)
        for tail in self.last_nodes:
            self.dot.add_edge(tail, n)
        self.last_nodes = [n]

    def visit_Expr(self, node):
        self.generic_simple_stmt(node)

    def visit_Assign(self, node):
        self.generic_simple_stmt(node)

    def visit_AugAssign(self, node):
        self.generic_simple_stmt(node)

    def visit_AnnAssign(self, node):
        self.generic_simple_stmt(node)

    def visit_Import(self, node):
    # No hacemos nada, se ignora
        pass

    def visit_ImportFrom(self, node):
    # No hacemos nada, se ignora
        pass

    def visit_Return(self, node):
        s = self.code_of(node)
        n = self.dot.new_node(s)
        for tail in self.last_nodes:
            self.dot.add_edge(tail, n)
        # return ends the flow: no tails continue through
        self.last_nodes = []

    def visit_Break(self, node):
        self.generic_simple_stmt(node)
        # conservatively clear tails; analysis of loop targets is non-trivial
        self.last_nodes = []

    def visit_Continue(self, node):
        self.generic_simple_stmt(node)
        self.last_nodes = []

    def visit_If(self, node: ast.If):
        cond_label = self.code_of(node.test)
        cond_n = self.dot.new_node(cond_label, shape='diamond')
        # conectar condición desde los tails actuales
        for tail in self.last_nodes:
            self.dot.add_edge(tail, cond_n)
        
        # Guardamos prev_tails para join
        prev_tails = self.last_nodes

        # --- Rama True ---
        self.last_nodes = [cond_n]
        self.process_block(node.body)
        true_tails = list(self.last_nodes)
        # Conectar desde cond_n a cada nodo inicial de true branch con etiqueta "True"
        for t in true_tails:
            self.dot.add_edge(cond_n, t, label="True")

        # --- Rama False ---
        if node.orelse:
            self.last_nodes = [cond_n]
            self.process_block(node.orelse)
            false_tails = list(self.last_nodes)
            for f in false_tails:
                self.dot.add_edge(cond_n, f, label="False")
        else:
            # no else: false branch sigue desde cond_n al join
            false_tails = [cond_n]

        # --- Nodo de unión ---
        join = self.dot.new_node("", shape="ellipse")
        for t in true_tails + false_tails:
            if t != cond_n:  # evitamos doble conexión desde cond_n si no hay else
                self.dot.add_edge(t, join)
        self.last_nodes = [join]

    def visit_While(self, node: ast.While):
        cond_label = self.code_of(node.test)
        cond_n = self.dot.new_node(cond_label, shape='diamond')
        
        # Conectar los nodos previos al condicional
        for tail in self.last_nodes:
            self.dot.add_edge(tail, cond_n)
        
        # Nodo de unión al final del while
        join = self.dot.new_node("", shape="ellipse")
        
        # --- Crear subgraph para el cuerpo del while ---
        cluster_id = f"cluster_{next(self.dot.node_id)}"
        self.dot.lines.append(f'  subgraph {cluster_id} {{')
        self.dot.lines.append('    style=dashed;')  # opcional: borde punteado
        self.dot.lines.append('    label="While Body";')
        
        # Procesar el nodo del condicional fuera del subgraph
        self.last_nodes = [cond_n]
        self.process_block(node.body)
        
        self.dot.lines.append('  }')  # cerrar subgraph
        
        # Conectar nodos finales del cuerpo al condicional (loop)
        for t in self.last_nodes:
            self.dot.add_edge(t, cond_n, label="True")
        
        # Rama False: salida al join
        self.dot.add_edge(cond_n, join, label="False")
        
        # Actualizar last_nodes para continuar desde el join
        self.last_nodes = [join]
        
        # Ignorar else por simplicidad
        if node.orelse:
            self.process_block(node.orelse)

    def visit_For(self, node: ast.For):
        # represent for similarly to while
        it_label = f"for {self.code_of(node.target)} in {self.code_of(node.iter)}"
        cond_n = self.dot.new_node(it_label, shape='diamond')
        for tail in self.last_nodes:
            self.dot.add_edge(tail, cond_n)
        self.last_nodes = [cond_n]
        self.process_block(node.body)
        for t in self.last_nodes:
            self.dot.add_edge(t, cond_n)
        exit_n = self.dot.new_node("AfterFor")
        self.dot.add_edge(cond_n, exit_n, label="Done")
        self.last_nodes = [exit_n]
        if node.orelse:
            self.process_block(node.orelse)

    def visit_Try(self, node: ast.Try):
        # Crear nodo "try"
        self.process_block(node.body)
    
        # Crear nodo de unión al final del try
        join = self.dot.new_node("", shape="ellipse")
        for tail in self.last_nodes:
            self.dot.add_edge(tail, join)
        
        # Actualizar last_nodes para continuar desde el join
        self.last_nodes = [join]

    # fallback
    def generic_visit(self, node):
        # For any other node types, try to create a simple node with its code
        if isinstance(node, ast.stmt):
            self.generic_simple_stmt(node)
        else:
            super().generic_visit(node)


def main():
    if len(sys.argv) < 2:
        print("Uso: py2flow.py archivo_entrada.py")
        sys.exit(1)
    
    infile = sys.argv[1]
    # Generar el nombre del archivo de salida en la misma carpeta
    base, _ = os.path.splitext(os.path.basename(infile))
    dir_name = os.path.dirname(os.path.abspath(infile))
    outfile = os.path.join(dir_name, base + ".dot")

    with open(infile, 'r', encoding='utf-8') as f:
        src = f.read()
    
    tree = ast.parse(src, filename=infile)
    fb = FlowBuilder(src)
    dot_text = fb.build(tree)
    
    with open(outfile, 'w', encoding='utf-8') as f:
        f.write(dot_text)
    
    print(f"Generado {outfile}")

if __name__ == "__main__":
    main()
