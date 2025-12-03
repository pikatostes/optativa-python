height = int(input("Introduzca la altura de la piramide azteca: "))

for i in range(height):
    if i % 2 != 0:
        print(" " * (height - i) + "*" * (i+1) + " " * 4 + "*" * (i+1))
    elif i == 0:
        print(" " * (height - i) + "*" * 6)
    else:
        print(" " * (height - i) + "*" * 6 + ("*" * 4) * (i-(i//2)))