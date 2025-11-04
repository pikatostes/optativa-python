cero = False
positivo = 0
negativo = 0

while cero != True:
    try:
        num = int(input("Introduzca un número no nulo: "))
    except ValueError:
        print("Entrada no válida. Introduzca un número no nulo.")
        continue
    
    if num < 0:
        negativo += 1
    elif num > 0:
        positivo += 1
    elif num == 0:
        cero = True

print(f"Se introdujero {positivo} positivos y {negativo} negativos")