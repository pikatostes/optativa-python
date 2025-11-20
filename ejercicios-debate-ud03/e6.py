height = int(input("Introduce the height: "))

for i in range(height):
    if i == 0 or i > int(height/2):
        print("*" + " " * (height) + "*")
    elif i == int(height/2):
        print("*" + " " * (i) + "*" + " " * (i) + "*")
    else:
        print("*" + " " * (i-1) + "*" + " " * (height-(2*i)) + "*" + " " * (i-1) + "*")
        