height = int(input("Introduce the height: "))

for i in range(0, height):
    if i == 0:
        print("4")
    elif i == height-1:
        print("4 " * height)
    else:
        print("4" + " " * (i+1) + "4")