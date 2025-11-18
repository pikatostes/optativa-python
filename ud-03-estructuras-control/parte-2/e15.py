try:
    altura = int(input("Introduzca la altura de la pirámide: "))

    if altura <= 0:
        raise ValueError
except ValueError:
    print("Error. Solo se permiten enteros positivos.")
    exit()

for i in range(altura, 0, -1):
    print(" " * (altura - i) + "*" * (2 * i - 1))