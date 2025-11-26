height = int(input("Introduce a height: "))


print("#" + "  " * (height - 1) + "#" + "#" * (height * 2))
for i in range(height - 1):
    print("#" + "  " * (height - 1) + "#")
    
print("#" * height * 4)

for i in range(height):
    if i == (height - 1):
        print("#" * (height * 2 + 1) + "  " * (height - 1) + "#")
    else:
        print("  " * (height) + "#" + "  " * (height - 1) + "#")