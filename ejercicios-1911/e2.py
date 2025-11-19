height = int(input("Introduce the height: "))

# Mitad superior
for i in range((height // 3)+1):
    if i == height // 3:
        print("*" * height)
    else:
        espacios = " " * i
        medio = "*" + " " * ((height // 3) - i)
        print(" " * i + medio * 3)

# Mitad inferior
for i in range((height // 3) - 1, -1, -1):
    espacios = " " * i
    medio = "*" + " " * ((height // 3) - i)
    print(espacios + medio * 3)
