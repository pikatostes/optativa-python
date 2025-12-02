height = int(input("Introduce a height: "))

for i in range(height):
    if i == 0:
        print("#" + "  " * (height - 1) + "#" + "#" * (height * 2))
    elif i == height - 1:
        print("#" * height * 4)
    else:
        print("#" + "  " * (height - 1) + "#")
    
for i in range(height):
    if i == (height - 1):
        print("#" * (height * 2 + 1) + "  " * (height - 1) + "#")
    else:
        print("  " * (height) + "#" + "  " * (height - 1) + "#")