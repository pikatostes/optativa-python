print("Piensa en un número del 1 al 100, y yo intentaré adivinarlo.")
print("Cuando te diga un número, responde con:")
print("  'mayor' si tu número es mayor,")
print("  'menor' si tu número es menor,")
print("  'igual' si he acertado.")
print()

minimo = 1
maximo = 100
intentos = 0

while True:
    intento = (minimo + maximo) // 2  # El ordenador hace una "búsqueda binaria"
    intentos += 1
    print(f"¿Es {intento}?")
    
    respuesta = int(input("\n [1] Mayor \n [2] Menor \n [3] Igual \n Respuesta: "))
    
    if respuesta == 1:
        minimo = intento + 1
    elif respuesta == 2:
        maximo = intento - 1
    elif respuesta == 3:
        print(f"¡He adivinado tu número en {intentos} intentos!")
        break
    else:
        print("Por favor, responde solo con 'mayor', 'menor' o 'igual'.")
    
    if minimo > maximo:
        print("Algo no cuadra... ¿seguro que has respondido correctamente?")
        break
