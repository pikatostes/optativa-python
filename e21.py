contador = 0
negativo = 0

while contador < 100:
    num = int(input("Introduzca un número no nulo: "))
    
    if num < 0:
        negativo += 1
        contador += 1
    else:
        contador += 1

if negativo > 0:
    print("Se introdujo un número negativo")
else:
    print("No se introdujeron números negativos")