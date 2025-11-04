contador = 0
positivo = 0
negativo = 0

while contador < 100:
    num = int(input("Introduzca un número no nulo: "))
    
    if num < 0:
        negativo += 1
        contador += 1
    else:
        positivo += 1
        contador += 1

print(f"Se introdujero {positivo} positivos y {negativo} negativos")