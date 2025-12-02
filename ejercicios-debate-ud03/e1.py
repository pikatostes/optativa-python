# Pedimos al usuario la altura (número entero) que define la mitad del rombo
height = int(input("Introduce the height: "))

# --- Mitad superior (desde la punta superior hasta el vértice central) ---
# Recorremos i = 0, 1, ..., height-1 (por la forma en la que funcionan los bucles 'for')
for i in range(height):
    if i == 0:
        # Línea superior: solo un asterisco, desplazado 'height' espacios desde la izquierda
        print(" " * height + "*")
    else:
        # Líneas intermedias de la mitad superior: dos asteriscos con espacios interiores
        # - 'height - i' espacios a la izquierda (para centrar)
        #   El número de espacios se va reduciendo conforme iteramos en el bucle
        # - un asterisco
        # - '2*i - 1' espacios interiores entre los asteriscos
        #   usamos esto debido a la simetría de la figura y le restamos 1 ya que el último espacio lo ocupará el asterisco
        # - el asterisco derecho
        print(" " * (height - i) + "*" + " " * (2 * i - 1) + "*")

# --- Mitad inferior (sin repetir el vértice central) ---
# Recorremos i = height-2, height-3, ..., 0 (descendiendo)
for i in range(height - 2, -1, -1):
    if i != 0:
        # Líneas intermedias de la mitad inferior: misma fórmula que en la parte superior
        print(" " * (height - i) + "*" + " " * (2 * i - 1) + "*")
    else:
        # Última línea inferior: igual que la primera (un solo asterisco centrado)
        print(" " * height + "*")
