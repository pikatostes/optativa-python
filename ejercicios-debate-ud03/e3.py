height = int(input("Introduce the height: "))

for i in range(height):
    if i == 0:
        print(" " * (height-i-1) + "*")
    elif i == height//2:
        print(" " * (height-i-1) + ("*" + " ") * (height//2+1))
    elif i == height-1:
        print("*" * (2*height))
    else:
        print(" " * (height-i-1) + "*" + " " * (2*i - 1) + "*")