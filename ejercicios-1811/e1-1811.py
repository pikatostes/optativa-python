height = int(input("Introduce the height: "))

# Mitad superior
for i in range(height):
    if i == 0:
        print("*")
    else:
        print("*" + " " * i + "*")

# Mitad inferior (sin repetir el vértice central)
for i in range(height - 2, -1, -1):
    if i != 0:
        print("*" + " " * i + "*")
    else:
        print("*")
