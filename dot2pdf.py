import os
import sys
import subprocess
from PyPDF2 import PdfMerger

def unify_dot_to_pdf(folder_path, output_pdf="unificado.pdf"):
    # 1. Buscar todos los .dot en la carpeta
    dot_files = [f for f in os.listdir(folder_path) if f.endswith(".dot")]
    if not dot_files:
        print("No se encontraron archivos .dot en la carpeta.")
        return
    
    pdf_files = []
    
    for dot_file in dot_files:
        dot_path = os.path.join(folder_path, dot_file)
        pdf_path = os.path.join(folder_path, os.path.splitext(dot_file)[0] + ".pdf")
        # 2. Convertir .dot a .pdf usando Graphviz
        subprocess.run(["dot", "-Tpdf", dot_path, "-o", pdf_path], check=True)
        pdf_files.append(pdf_path)
    
    # 3. Unir todos los PDFs en uno solo
    merger = PdfMerger()
    for pdf in pdf_files:
        merger.append(pdf)
    
    output_path = os.path.join(folder_path, output_pdf)
    merger.write(output_path)
    merger.close()
    
    print(f"PDF unificado generado en: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python unify_dot.py <ruta_carpeta_con_dot>")
        sys.exit(1)
    
    folder = sys.argv[1]
    unify_dot_to_pdf(folder)
