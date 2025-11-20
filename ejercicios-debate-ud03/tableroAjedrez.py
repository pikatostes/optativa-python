height = int(input("Introduce el tamaño del tablero: "))

casilla = 3  # tamaño de cada casilla (3x3)

for fila in range(height):
    for subfila in range(casilla):
        linea = ""
        for columna in range(height):
            if (fila + columna) % 2 == 0:
                linea += "*" * casilla
            else:
                linea += "|" * casilla
        print(linea)
