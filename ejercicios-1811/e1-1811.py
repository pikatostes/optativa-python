height = int(input("Introduce the height: "))

for i in range(0, height):
    if i == 0:
        print(" " * height + " *")
    else:
        print(" " * (height - i) + "*" + " " * i + "*")
    
for j in range(height, -1, -1):
    if j == 0:
        print(" " * height + " *")
    else:
        print(" " * (height-j) + "*" + " " * j + "*")