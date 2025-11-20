height = int(input("Introduce the height: "))

halfHeight = int(height/2)

for i in range(halfHeight):
    if i == 0:
        print("*" * height)
    else:
        print("*" + " " * i + "*" + " " * (halfHeight-i) + " *")
        
# Mitad inferior (sin repetir el vértice central)
for i in range(halfHeight, -1, -1):
    if i != 0:
        print("*" + " " * i + "*" + " " * (halfHeight-i) + " *")
    else:
        print("*" * height)