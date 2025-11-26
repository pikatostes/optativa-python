height = int(input("Introduce a height: "))

if height == 88:
    print("Heil Hitler")
    exit()
elif height == 1945:
    print("R.I.P. Manin")
    exit()

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