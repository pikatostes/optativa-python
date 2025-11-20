height = int(input("Introduce the height: "))

mid = height // 2
line3a = mid - 1
line3b = mid + 1

for i in range(height):
    line = "*"
    for j in range(1, height - 1):

        # Bordes arriba y abajo
        if i == 0 or i == height - 1:
            line += "*"

        # Línea SOLO con bordes
        elif i == mid:
            line += " "

        # Líneas con EXACTAMENTE 3 asteriscos (los bordes + uno interior)
        elif i == line3a or i == line3b:
            if j == i or j == (height - 1 - i):
                line += "*"     # único asterisco interior
            else:
                line += " "

        # Resto: X normal
        elif j == i or j == (height - 1 - i):
            line += "*"
        else:
            line += " "

    line += "*"
    print(line)
