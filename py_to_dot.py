import sys
import re

def get_block_type(line):
    """Clasifica una línea según su tipo lógico"""
    line = line.strip()
    if line.startswith(("if ", "elif ", "else", "for ", "while ")):
        return "decision"
    elif re.match(r"print\s*\(.*\)", line) or re.match(r"input\s*\(.*\)", line):
        return "io"
    elif line.startswith("def ") or line.startswith("#") or line == "" or line.startswith("try") or line.startswith("except"):
        return None
    else:
        return "process"

def generate_dot(nodes):
    """Genera el contenido DOT a partir de una lista de nodos"""
    dot = []
    dot.append('digraph G {')
    dot.append('  rankdir=TB;')
    dot.append('  node [fontname="Arial", fontsize=12];')
    dot.append('')

    # Nodos de inicio y fin
    dot.append('  start [shape=ellipse, style=filled, fillcolor=lightgreen, label="Inicio"];')
    dot.append('  end [shape=ellipse, style=filled, fillcolor=lightcoral, label="Fin"];')
    dot.append('')

    # Crear los nodos
    for i, (text, ntype) in enumerate(nodes):
        node_id = f"n{i}"
        label = text.replace('"', '\\"')
        if ntype == "decision":
            shape = "diamond"
            color = "gold"
        elif ntype == "io":
            shape = "parallelogram"
            color = "mediumpurple1"
        else:
            shape = "box"
            color = "lightskyblue"
        dot.append(f'  {node_id} [shape={shape}, style=filled, fillcolor="{color}", label="{label}"];')

    dot.append('')

    # Conexiones
    if nodes:
        dot.append(f'  start -> n0;')
        for i in range(len(nodes) - 1):
            dot.append(f'  n{i} -> n{i+1};')
        dot.append(f'  n{len(nodes)-1} -> end;')
    else:
        dot.append('  start -> end;')

    dot.append('}')
    return "\n".join(dot)

def main():
    if len(sys.argv) < 2:
        print("Uso: python py_to_dot.py archivo.py")
        return

    py_file = sys.argv[1]
    with open(py_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    nodes = []
    for line in lines:
        t = get_block_type(line)
        if t:
            nodes.append((line.strip(), t))

    dot_content = generate_dot(nodes)

    output_file = py_file.replace(".py", ".dot")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(dot_content)

    print(f"✅ Archivo DOT generado: {output_file}")
    print("Puedes renderizarlo con:")
    print(f"  dot -Tpng {output_file} -o diagrama.png")

if __name__ == "__main__":
    main()