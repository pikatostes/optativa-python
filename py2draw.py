#!/usr/bin/env python3
"""
py2draw.py — Convert Python code into a draw.io (diagrams.net) flowchart.

Genera un archivo .drawio.xml que representa:
- if, for, while como rombos (condición) con TRUE hacia abajo y FALSE hacia la derecha
- bloques de instrucciones como rectángulos
- operaciones de E/S (print/input/.write) como paralelogramos
- nodos de unión (pequeños círculos) para unir ramas
- para bucles, añade la flecha de retorno desde la unión hacia la condición
El diseño es modular y escalable (funciones emit_*).
"""

import argparse
import ast
import os
import sys
import xml.sax.saxutils as sax

NODE_WIDTH = 240
NODE_HEIGHT = 60
X_GAP = 40
Y_GAP = 100
INDENT_X = 200

MXGRAPH_MODEL_TEMPLATE = '''<mxGraphModel dx="1168" dy="792" grid="1" gridSize="10"
  guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1"
  pageScale="1" pageWidth="850" pageHeight="1100">
  <root>
    <mxCell id="0"/>
    <mxCell id="1" parent="0"/>
{cells}
  </root>
</mxGraphModel>'''

VERTEX_TEMPLATE = '''    <mxCell id="{id}" value="{label}"
      style="{style}" vertex="1" parent="1">
      <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>
    </mxCell>'''

EDGE_TEMPLATE = '''    <mxCell id="{id}"{value_attr} edge="1" parent="1" source="{src}" target="{tgt}"
      style="edgeStyle=orthogonalEdgeStyle;rounded=0;">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>'''


# -------------------------
# Utilities & escaping
# -------------------------

def escape_label(s: str) -> str:
    """Escape a label for XML attribute (escape <,>,& and quotes)."""
    return sax.escape(s).replace('"', "&quot;")


# -------------------------
# AST helpers
# -------------------------

def is_io_call(node: ast.AST) -> bool:
    """Return True if the statement contains input(), print(), or *.write()."""
    for child in ast.walk(node):
        if isinstance(child, ast.Call):
            f = child.func
            if isinstance(f, ast.Name) and f.id in ("input", "print"):
                return True
            if isinstance(f, ast.Attribute) and getattr(f, "attr", "").lower() == "write":
                return True
    return False


def stmt_label(source_lines, node) -> str:
    """Generate a readable one-line label for a statement node."""
    try:
        lineno = getattr(node, "lineno", None)
        end_lineno = getattr(node, "end_lineno", lineno)
        if lineno is None:
            return node.__class__.__name__
        snippet = "".join(source_lines[lineno - 1:end_lineno]).strip()
        snippet = " ".join(snippet.split())
        if len(snippet) > 200:
            snippet = snippet[:197] + "..."
        return escape_label(snippet)
    except Exception:
        return escape_label(node.__class__.__name__)


# -------------------------
# ID / layout management
# -------------------------

class CanvasContext:
    """Hold mutable state while emitting cells: id counter and y-position counter."""
    def __init__(self):
        self._id = 2  # start after 0 and 1 used in model
        self.y_index = 0  # increments to place nodes vertically
        self.cells = []
        self.edges = []

    def new_id(self):
        nid = str(self._id)
        self._id += 1
        return nid

    def place_y(self):
        """Return y coordinate for the next top-level visual node and advance."""
        y = self.y_index * Y_GAP + 20
        self.y_index += 1
        return y

    def add_cell(self, id, label, style, x, y, w=NODE_WIDTH, h=NODE_HEIGHT):
        self.cells.append(VERTEX_TEMPLATE.format(
            id=id, label=label, style=style, x=x, y=y, w=w, h=h
        ))

    def add_edge(self, src, tgt, label=None):
        value_attr = f' value="{escape_label(label)}"' if label else ""
        eid = self.new_id()
        self.edges.append(EDGE_TEMPLATE.format(id=eid, value_attr=value_attr, src=src, tgt=tgt))


# -------------------------
# Vertex creation helpers
# -------------------------

def style_for_shape(shape: str) -> str:
    base = "whiteSpace=wrap;html=1;labelPosition=center;verticalLabelPosition=middle;align=center;"
    if shape == "parallelogram":
        return "shape=parallelogram;" + base
    if shape == "ellipse":
        return "shape=ellipse;" + base
    if shape == "diamond" or shape == "rhombus":
        # draw.io uses 'rhombus' or 'shape=rhombus'; we'll use rhombus
        return "shape=rhombus;" + base
    # default rectangle
    return "rounded=0;" + base


def create_vertex(ctx: CanvasContext, label: str, x: int, y: int, shape="rectangle", w=None, h=None):
    vid = ctx.new_id()
    w = NODE_WIDTH if w is None else w
    h = NODE_HEIGHT if h is None else h
    style = style_for_shape(shape)
    ctx.add_cell(vid, label, style, x, y, w, h)
    return vid


# -------------------------
# Emit primitives & sequences
# -------------------------

def emit_statement_node(ctx: CanvasContext, label: str, depth: int, is_io=False):
    """Emit a single statement node (rectangle or parallelogram). Returns node id."""
    x = depth * INDENT_X + X_GAP
    y = ctx.place_y()
    shape = "parallelogram" if is_io else "rectangle"
    return create_vertex(ctx, label, x, y, shape=shape)


def emit_union_node(ctx: CanvasContext, depth: int):
    """Emit the small circle (union) used to join branches."""
    # smaller circle: width and height smaller than NODE_WIDTH
    x = depth * INDENT_X + X_GAP + NODE_WIDTH // 2 - 20
    y = ctx.place_y()
    # use smaller size
    return create_vertex(ctx, "", x, y, shape="ellipse", w=40, h=40)


def emit_condition_node(ctx: CanvasContext, label: str, depth: int):
    """Emit a diamond condition node. Returns node id."""
    x = depth * INDENT_X + X_GAP
    y = ctx.place_y()
    # diamond bigger
    return create_vertex(ctx, label, x, y, shape="diamond", w=200, h=80)


def emit_sequence(ctx: CanvasContext, stmts, source_lines, depth: int):
    """
    Emit a sequence of statements (non-compound at top-level of sequence).
    Returns (first_id, last_id). If stmts is empty returns (None, None).
    Each stmt can be a simple stmt or a compound AST node; dispatch to emit_node.
    """
    first = None
    last = None
    for s in stmts:
        entry, exit = emit_node(ctx, s, source_lines, depth)
        if entry is None:
            continue
        if first is None:
            first = entry
        if last is not None:
            ctx.add_edge(last, entry)  # connect previous to this
        last = exit
    return first, last


# -------------------------
# High-level emitter for AST nodes
# -------------------------

def emit_node(ctx: CanvasContext, node, source_lines, depth: int):
    """
    Given an AST statement node, emit the appropriate subgraph and return (entry, exit) node ids.
    Handles: simple statements, If, For, While, Try, With, Function/Class (as opaque blocks).
    """
    # SIMPLE STATEMENTS (Expr, Assign, Return, etc.)
    if isinstance(node, (ast.Expr, ast.Assign, ast.AnnAssign, ast.AugAssign,
                         ast.Return, ast.Break, ast.Continue, ast.Pass, ast.Raise)):
        label = stmt_label(source_lines, node)
        io = is_io_call(node)
        vid = emit_statement_node(ctx, label, depth, is_io=io)
        return vid, vid

    # FUNCTION / CLASS: treat header as rectangle and then body as nested (but we will show body's nodes in place)
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        header_label = stmt_label(source_lines, node)
        header_id = emit_statement_node(ctx, header_label, depth, is_io=False)
        # connect header -> body sequence (if any)
        body_first, body_last = emit_sequence(ctx, node.body, source_lines, depth + 1)
        if body_first:
            ctx.add_edge(header_id, body_first)
            return header_id, body_last
        return header_id, header_id

    # IF
    if isinstance(node, ast.If):
        cond_label = stmt_label(source_lines, node)
        cond_id = emit_condition_node(ctx, cond_label, depth)

        # TRUE branch (body)
        true_first, true_last = emit_sequence(ctx, node.body, source_lines, depth + 1)

        # FALSE branch (orelse) - could be empty
        false_first, false_last = emit_sequence(ctx, node.orelse, source_lines, depth + 1)

        # union node (join point)
        union_id = emit_union_node(ctx, depth)

        # connect condition true -> body or union if body empty
        if true_first:
            ctx.add_edge(cond_id, true_first, label="TRUE")
            # connect last body -> union
            ctx.add_edge(true_last, union_id)
        else:
            ctx.add_edge(cond_id, union_id, label="TRUE")

        # connect condition false -> orelse first or union
        if false_first:
            ctx.add_edge(cond_id, false_first, label="FALSE")
            ctx.add_edge(false_last, union_id)
        else:
            ctx.add_edge(cond_id, union_id, label="FALSE")

        return cond_id, union_id

    # FOR
    if isinstance(node, ast.For) or isinstance(node, ast.AsyncFor):
        cond_label = stmt_label(source_lines, node)  # show full for header
        cond_id = emit_condition_node(ctx, cond_label, depth)

        # body
        body_first, body_last = emit_sequence(ctx, node.body, source_lines, depth + 1)

        # else body (for .. else)
        else_first, else_last = emit_sequence(ctx, node.orelse, source_lines, depth + 1)

        # create a join/unio node for after the loop
        after_loop_id = emit_union_node(ctx, depth)

        # TRUE -> body (if present) else directly back to condition (rare)
        if body_first:
            ctx.add_edge(cond_id, body_first, label="TRUE")
            # after body, go to a loop-join node which will point back to cond
            loop_join = emit_union_node(ctx, depth + 0)  # small helper join
            ctx.add_edge(body_last, loop_join)
            # loop join -> cond (back)
            ctx.add_edge(loop_join, cond_id)
            # also connect loop_join -> after_loop? Not necessary; false branch handles exit
        else:
            # no body; make cond TRUE loop back
            ctx.add_edge(cond_id, cond_id, label="TRUE")

        # FALSE -> else_first or after_loop
        if else_first:
            ctx.add_edge(cond_id, else_first, label="FALSE")
            ctx.add_edge(else_last, after_loop_id)
        else:
            ctx.add_edge(cond_id, after_loop_id, label="FALSE")

        return cond_id, after_loop_id

    # WHILE
    if isinstance(node, ast.While):
        cond_label = stmt_label(source_lines, node)
        cond_id = emit_condition_node(ctx, cond_label, depth)

        body_first, body_last = emit_sequence(ctx, node.body, source_lines, depth + 1)
        else_first, else_last = emit_sequence(ctx, node.orelse, source_lines, depth + 1)

        after_loop_id = emit_union_node(ctx, depth)

        if body_first:
            ctx.add_edge(cond_id, body_first, label="TRUE")
            # after body, join and go back to cond
            loop_join = emit_union_node(ctx, depth)
            ctx.add_edge(body_last, loop_join)
            ctx.add_edge(loop_join, cond_id)
        else:
            ctx.add_edge(cond_id, cond_id, label="TRUE")

        if else_first:
            ctx.add_edge(cond_id, else_first, label="FALSE")
            ctx.add_edge(else_last, after_loop_id)
        else:
            ctx.add_edge(cond_id, after_loop_id, label="FALSE")

        return cond_id, after_loop_id

    # TRY / WITH / MATCH and others -> attempt to linearize inside
    if isinstance(node, ast.With) or isinstance(node, ast.AsyncWith):
        header = stmt_label(source_lines, node)
        header_id = emit_statement_node(ctx, header, depth, is_io=False)
        body_first, body_last = emit_sequence(ctx, node.body, source_lines, depth + 1)
        if body_first:
            ctx.add_edge(header_id, body_first)
            return header_id, body_last
        return header_id, header_id

    if isinstance(node, ast.Try):
        header_id = emit_statement_node(ctx, "try", depth, is_io=False)
        body_first, body_last = emit_sequence(ctx, node.body, source_lines, depth + 1)
        last = body_last if body_last else header_id
        # handlers
        for handler in node.handlers:
            h_first, h_last = emit_sequence(ctx, handler.body, source_lines, depth + 1)
            if h_first:
                ctx.add_edge(last, h_first)
                last = h_last
        # orelse
        o_first, o_last = emit_sequence(ctx, node.orelse, source_lines, depth + 1)
        if o_first:
            ctx.add_edge(last, o_first)
            last = o_last
        # finally
        f_first, f_last = emit_sequence(ctx, node.finalbody, source_lines, depth + 1)
        if f_first:
            ctx.add_edge(last, f_first)
            last = f_last
        return header_id, last

    # Fallback: unknown node -> single rectangle with its source
    label = stmt_label(source_lines, node)
    vid = emit_statement_node(ctx, label, depth, is_io=is_io_call(node))
    return vid, vid


# -------------------------
# Top-level build
# -------------------------

def build_cells_from_ast(tree, source_lines):
    ctx = CanvasContext()

    # START node
    start_id = create_vertex(ctx, "INICIO", X_GAP, ctx.place_y(), shape="ellipse")
    # emit top-level sequence
    first, last = emit_sequence(ctx, tree.body, source_lines, depth=0)

    # if there is a first node, connect start -> first, else connect start -> FIN directly later
    if first:
        ctx.add_edge(start_id, first)
    else:
        # create a FIN directly (no statements)
        fin_id = create_vertex(ctx, "FIN", X_GAP, ctx.place_y(), shape="ellipse")
        ctx.add_edge(start_id, fin_id)
        # add cells and edges to model
        return "\n".join(ctx.cells + ctx.edges)

    # FIN node
    fin_id = create_vertex(ctx, "FIN", X_GAP, ctx.place_y(), shape="ellipse")

    # connect last -> fin (if last exists)
    if last:
        ctx.add_edge(last, fin_id)
    else:
        # in case sequence had no last but had first, connect start->fin (rare)
        ctx.add_edge(start_id, fin_id)

    # return xml cells + edges
    return "\n".join(ctx.cells + ctx.edges)


def generate_mxfile(model_xml):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net">
  <diagram name="Page-1">
{model_xml}
  </diagram>
</mxfile>'''


# -------------------------
# Main
# -------------------------

def main():
    parser = argparse.ArgumentParser(description="Convert Python to draw.io diagram.")
    parser.add_argument("input", help="Python file to convert")
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print("File not found:", args.input, file=sys.stderr)
        sys.exit(1)

    source = open(args.input, "r", encoding="utf-8").read()
    source_lines = source.splitlines(keepends=True)

    try:
        tree = ast.parse(source, filename=args.input)
    except SyntaxError as e:
        print("Syntax error:", e, file=sys.stderr)
        sys.exit(2)

    cells = build_cells_from_ast(tree, source_lines)
    model_xml = MXGRAPH_MODEL_TEMPLATE.format(cells=cells)
    mxfile = generate_mxfile(model_xml)

    out_path = os.path.splitext(args.input)[0] + ".drawio.xml"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(mxfile)

    print("Diagrama generado en:", out_path)


if __name__ == "__main__":
    main()
