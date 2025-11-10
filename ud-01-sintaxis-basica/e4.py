num1 = int(input("Introduzca el primer número: "))
num2 = int(input("Introduzca el primer número: "))

add = num1 + num2
substract = num1 - num2
multiply = num1 * num2
divide = num1 / num2

operaciones = [
    {add, "suma"},
    {substract, "resta"},
    {multiply, "multiplicación"},
    {divide, "división"}]

for resultado, operacion in operaciones:
    print(f"El resultado de {operacion} es {resultado}")
    