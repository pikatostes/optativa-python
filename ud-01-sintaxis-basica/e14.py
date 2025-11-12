try:
    num1 = float(input("Introduzca el primer número: "))
    num2 = float(input("Introduzca el segundo número: "))
except ValueError:
    print("Error. Revise los datos introducidos")
    
suma = num1 + num2
resta = num1 - num2
multiplicacion = num1 * num2
if num2 == 0:
    division = "infinito"
else:
    division = num1 / num2

operaciones = [
    {suma, "suma"},
    {resta, "resta"},
    {multiplicacion, "multiplicación"},
    {division, "división"}
]

for resultado, operacion in operaciones:
    print(f"{operacion}: {resultado}")