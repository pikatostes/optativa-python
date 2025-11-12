num1 = float(input("Introduce el primer número: "))
num2 = float(input("Introduce el segundo número: "))

if num1 == num2:
    print(f"{num1} y {num2} son iguales")
elif num1 > num2:
    print(f"{num1} > {num2}")
elif num2 > num1:
    print(f"{num2} > {num1}")