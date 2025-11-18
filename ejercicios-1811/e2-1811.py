height = int(input("Introduce the height: "))

for i in range(height):
    if i == 0:
        print("4")
    elif i == height - 1:
        print("4 " * height)
    else:
        print("4" + " " * (2*i - 1) + "4")
