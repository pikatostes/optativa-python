height = int(input("Introduce the height: "))

for i in range(height):
    if i == 0:
        print(" " * (height-i) + "*")
    elif i == float(height / 2):
        print(" " * (height-i) + ("*" + " ") * int(height/2+1))
    elif i == height-1:
        print("*" * (2*height))
    else:
        print(" " * (height-i) + "*" + " " * (2*i - 1) + "*")